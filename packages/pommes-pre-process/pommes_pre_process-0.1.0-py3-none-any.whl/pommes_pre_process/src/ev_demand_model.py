# ev_demand_model.py

import pandas as pd
import xarray as xr
from typing import List

from pommes_pre_process.src.temperature import create_temperature_xarray
from pommes_pre_process.src.utilities import (
    create_empty_xarray_dataset,
    add_dataarray_to_dataset,
)

# --------------------------------------------------------
# Somme la demande totale et la demande des VE
# --------------------------------------------------------


def sum_exogenous_demand_and_electric_vehicle_demand(
    exo_demand_xr: xr.DataArray, ev_demand_xr: xr.DataArray
) -> xr.DataArray:
    """
    Somme la demande exogène et la demande des véhicules électriques.
    Si ev_demand_xr n'a pas de coordonnées à certains endroits, on utilise uniquement les valeurs de exo_demand_xr.
    :param exo_demand_xr: xr.DataArray
    :param ev_demand_xr: xr.DataArray
    :return: somme : exo_demand_xr + ev_demand_xr : xr.DataArray
    """

    # Vérifier que les dimensions sont compatibles
    if exo_demand_xr.dims != ev_demand_xr.dims:
        raise ValueError("Les dimensions des deux DataArray sont différentes.")

    # Aligner les DataArrays en conservant les coordonnées du premier
    aligned_exo_demand_xr, aligned_ev_demand_xr = xr.align(
        exo_demand_xr, ev_demand_xr, join="left"
    )

    # Remplacer les NaN dans ev_demand_xr par 0 avant la somme
    aligned_ev_demand_xr_filled = aligned_ev_demand_xr.fillna(0)

    total_demand = aligned_exo_demand_xr + aligned_ev_demand_xr_filled

    # Retourner la somme des deux DataArrays alignés
    return total_demand.rename("demand")


# --------------------------------------------------------
# Récupère la demande électrique totale des VE sous le format adéquat.
# --------------------------------------------------------


def extract_total_demand_from_xarray_dataset_and_convert_format(
    consumption_xr: xr.Dataset,
) -> xr.DataArray:
    """
    Transforme la consommation totale des véhicules électriques en un DataArray
    avec les dimensions [area, year_op, resource, hour], en conservant `area`.

    Parameters:
        consumption_xr (xr.Dataset): Dataset contenant `total_ev_consumption`.

    Returns:
        xr.DataArray: DataArray restructuré avec les dimensions [area, year_op, resource, hour].
    """
    # Vérification des données nécessaires
    if "total_ev_consumption" not in consumption_xr.data_vars:
        raise ValueError("La variable 'total_ev_consumption' est absente du Dataset.")
    if "time" not in consumption_xr.coords:
        raise ValueError("La coordonnée 'time' est absente du Dataset.")
    if "area" not in consumption_xr.coords:
        raise ValueError("La coordonnée 'area' est absente du Dataset.")

    # Extraction de `total_ev_consumption` et de ses coordonnées
    demand_xr = consumption_xr["total_ev_consumption"]
    time = demand_xr.coords["time"]

    # Calculer les heures depuis le début de l'année
    hour = (time.dt.dayofyear.data - 1) * 24 + time.dt.hour.data + 1

    # Assignation des nouvelles coordonnées
    demand_xr = demand_xr.assign_coords(
        year_op=("time", time.dt.year.data), hour=("time", hour)
    )

    # Ajouter la dimension 'resource' avec la valeur 'electricity'
    resource = xr.DataArray(["electricity"], dims="resource")
    demand_xr = demand_xr.expand_dims(resource=resource)

    # Réorganiser pour que year_op et hour soient des dimensions séparées
    demand_xr = demand_xr.set_index(time=["year_op", "hour"])

    # "Unstack" de la dimension 'time' pour obtenir 'year_op' et 'hour' comme dimensions séparées
    demand_xr = demand_xr.unstack("time")

    # Réorganiser pour que 'area' soit la première dimension
    demand_xr = demand_xr.transpose("area", "year_op", "resource", "hour").rename(
        "ev_demand"
    )

    return demand_xr


# --------------------------------------------------------
# Création des datasets xarray de consommation
# --------------------------------------------------------

def create_total_consumption_xarray_dataset(
        temperature_df: pd.DataFrame,
        calibration_profile_df: pd.DataFrame,
        area_profile_df: pd.DataFrame,
        ev_fleet_df: pd.DataFrame,
        temperature_threshold: float = 15,
        temperature_minimum: float = 0,
        thermal_sensitivity_activation: bool = True,
) -> xr.Dataset:

    consumption_per_million_xr = create_consumption_per_million_ev_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        area_profile_df,
        temperature_threshold,
        temperature_minimum,
        thermal_sensitivity_activation,
    )

    time_df = extract_time_dimension_from_xarray(create_temperature_xarray(temperature_df))

    area_ev_fleet_xr = create_area_ev_fleet_xarray(ev_fleet_df, time_df)

    ev_total_demand_xr = compute_total_consumption_to_xarray_dataset(
        consumption_per_million_xr,
        area_ev_fleet_xr,
    )

    return ev_total_demand_xr


def compute_total_consumption_to_xarray_dataset(
    consumption_per_million_ev_xr: xr.Dataset, area_ev_fleet_xr: xr.DataArray
) -> xr.Dataset:
    """
    Crée un Dataset contenant la consommation totale d'énergie pour une flotte de véhicules électriques.

    Parameters:
        consumption_per_million_ev_xr (xr.Dataset): Dataset avec la consommation par million de véhicules électriques.
        area_ev_fleet_xr (xr.DataArray): Données sur le nombre de véhicules électriques dans chaque zone.

    Returns:
        xr.Dataset: Dataset mis à jour contenant la consommation totale.
    """
    # Calculer la consommation totale pour chaque zone
    total_ev_consumption_xr = (
        consumption_per_million_ev_xr["total_consumption_per_million_ev"]
        * area_ev_fleet_xr
    ) / 1000000

    # Renommer la DataArray pour plus de clarté
    total_ev_consumption_xr = total_ev_consumption_xr.rename("total_ev_consumption")

    ev_demand_xr = consumption_per_million_ev_xr.copy(deep=True)
    ev_demand_xr.attrs["name"] = "ev_demand"

    # Ajouter les DataArrays au Dataset
    for dataarray in [area_ev_fleet_xr, total_ev_consumption_xr]:
        ev_demand_xr = add_dataarray_to_dataset(
            ev_demand_xr, dataarray
        )


    return ev_demand_xr


def create_consumption_per_million_ev_xarray_dataset(
    temperature_df: pd.DataFrame,
    calibration_profile_df: pd.DataFrame,
    area_profile_df: pd.DataFrame,
    temperature_threshold: float = 15,
    temperature_minimum: float = 0,
    thermal_sensitivity_activation: bool = True,
) -> xr.Dataset:
    """
    Crée un dataset xarray contenant plusieurs DataArray liés à la consommation.
    """

    # Étape 1 : Création des DataArrays
    temperature_xr = create_temperature_xarray(temperature_df)

    time_df = extract_time_dimension_from_xarray(temperature_xr)

    thermal_sensitivity_xr = create_thermal_sensitivity_xarray(
        calibration_profile_df,
        time_df,
        temperature_threshold,
        temperature_minimum,
        thermal_sensitivity_activation,
    )

    non_thermal_sensitive_consumption_xr = (
        create_non_thermal_sensitive_consumption_xarray(area_profile_df, time_df)
    )

    thermal_sensitive_consumption_xr = create_thermal_sensitive_consumption_xarray(
        temperature_xr, thermal_sensitivity_xr, temperature_threshold
    )

    total_consumption_xr = calculate_total_consumption_xarray(
        non_thermal_sensitive_consumption_xr, thermal_sensitive_consumption_xr
    )

    # Étape 2 : Création du dataset et ajout des DataArray
    dataset = create_empty_xarray_dataset("consumption_per_million_ev")

    for dataarray in [
        temperature_xr,
        thermal_sensitivity_xr,
        non_thermal_sensitive_consumption_xr,
        thermal_sensitive_consumption_xr,
        total_consumption_xr,
    ]:
        dataset = add_dataarray_to_dataset(dataset, dataarray)

    return dataset

# --------------------------------------------------------
# Création des DataArray
# --------------------------------------------------------


def create_thermal_sensitivity_xarray(
    calibration_profile_df: pd.DataFrame,
    time_df: pd.DataFrame,
    temperature_threshold: float,
    temperature_minimum: float,
    thermal_sensitivity_activation: bool,
) -> xr.DataArray:
    """
    Génère un DataArray pour la sensibilité thermique.
    """
    sensitivity_profile_df = calculate_and_add_thermal_sensitivity_in_profile(
        calibration_profile_df,
        temperature_threshold,
        temperature_minimum,
        thermal_sensitivity_activation,
    )

    merged_profile_df = merge_hour_day_profile_with_time_df(
        sensitivity_profile_df, time_df, ["thermal_sensitivity"]
    )

    return xr.DataArray(
        merged_profile_df["thermal_sensitivity"],
        dims=["time"],
        coords={"time": time_df.index},
        name="thermal_sensitivity",
    )


def create_non_thermal_sensitive_consumption_xarray(
    area_profile_df: pd.DataFrame, time_df: pd.DataFrame
) -> xr.DataArray:
    """
    Crée un DataArray pour la consommation non thermique.
    """
    area_pivot_profile_df = pivot_area_hour_day_profile(area_profile_df)
    merged_profile_df = merge_hour_day_profile_with_time_df(
        area_pivot_profile_df, time_df, area_pivot_profile_df.columns.tolist()
    )

    return xr.DataArray(
        merged_profile_df.values,
        dims=["time", "area"],
        coords={"time": time_df.index, "area": area_pivot_profile_df.columns},
        name="non_thermal_sensitive_consumption",
    ).sortby("area")  # DataArray trié par région par ordre alphabétique


def create_thermal_sensitive_consumption_xarray(
    temperature_xr: xr.DataArray,
    thermal_sensitivity_xr: xr.DataArray,
    temperature_threshold: float,
) -> xr.DataArray:
    """
    Calcule la consommation sensible à la température.
    """
    temp_diff = temperature_threshold - temperature_xr
    condition = temperature_xr <= temperature_threshold

    sensitive_consumption = xr.where(condition, temp_diff * thermal_sensitivity_xr, 0)

    return xr.DataArray(
        sensitive_consumption,
        dims=["time", "area"],
        coords=temperature_xr.coords,
        name="thermal_sensitive_consumption",
    ).sortby("area")  # DataArray trié par région par ordre alphabétique


def calculate_total_consumption_xarray(
    non_thermal_xr: xr.DataArray, thermal_xr: xr.DataArray
) -> xr.DataArray:
    """
    Calcule la consommation totale pour un million de véhicules électriques.
    """
    aligned_non_thermal, aligned_thermal = xr.align(
        non_thermal_xr, thermal_xr, join="exact"
    )
    total_consumption = aligned_non_thermal + aligned_thermal

    return total_consumption.rename("total_consumption_per_million_ev")


def create_area_ev_fleet_xarray(
    area_ev_fleet_df: pd.DataFrame,
    time_df: pd.DataFrame,
) -> xr.DataArray:
    """
    Calcule le nombre de véhicule électrique par année par région
    :param area_ev_fleet_df:
    :param time_df:
    :return: xr.DataArray avec le nombre de véhicules électriques par année par région
    """

    area_ev_fleet_pivot_df = pivot_area_year_profile(area_ev_fleet_df)

    merged_profile_df = merge_year_profile_with_time_df(
        area_ev_fleet_pivot_df, time_df, area_ev_fleet_pivot_df.columns.tolist()
    )

    return xr.DataArray(
        merged_profile_df.values,
        dims=["time", "area"],
        coords={"time": time_df.index, "area": area_ev_fleet_pivot_df.columns},
        name="number_of_ev",
    ).sortby("area")  # DataArray trié par région par ordre alphabétique


# --------------------------------------------------------
# Calcul de la thermosensibilité
# --------------------------------------------------------


def calculate_and_add_thermal_sensitivity_in_profile(
    default_profile_df: pd.DataFrame,
    temperature_threshold: float,
    temperature_minimum: float,
    thermal_sensitivity_activation: bool,
) -> pd.DataFrame:
    """
    Importe la thermosensibiltié calculée dans le dataframe de calibration
    :param default_profile_df:
    :param temperature_threshold:
    :param temperature_minimum:
    :param thermal_sensitivity_activation:
    :return: pivot_profile_df: avec ajout de la colonne "thermal_sensitivity"
    """

    pivot_profile_df = pivot_season_hour_day_profile(default_profile_df)

    pivot_profile_df["thermal_sensitivity"] = calculate_thermal_sensitivity(
        pivot_profile_df,
        temperature_threshold,
        temperature_minimum,
        thermal_sensitivity_activation,
    )

    return pivot_profile_df


def calculate_thermal_sensitivity(
    pivot_profile_df: pd.DataFrame,
    temperature_threshold: float,
    temperature_minimum: float,
    thermal_sensitivity_activation: bool = True,
) -> pd.Series:
    """
    Calcule la thermosensibilité comme différence entre la consommation hiver et été sur un delta de températures
    """
    if "winter" not in pivot_profile_df or "summer" not in pivot_profile_df:
        raise ValueError("The DataFrame must contain 'winter' and 'summer' columns.")
    if temperature_threshold <= temperature_minimum:
        raise ValueError(
            "Temperature threshold must be greater than temperature minimum."
        )

    if thermal_sensitivity_activation:
        # Calculate temperature range
        temp_range = temperature_threshold - temperature_minimum

        # Calculate thermal sensitivity
        thermal_sensitivity = (
            pivot_profile_df["winter"] - pivot_profile_df["summer"]
        ) / temp_range
    else:
        thermal_sensitivity = 0

    return thermal_sensitivity


# --------------------------------------------------------
# Préparation et utilitaires
# --------------------------------------------------------


def extract_time_dimension_from_xarray(dataarray: xr.DataArray) -> pd.DataFrame:
    """
    Extrait la dimension temporelle d'un DataArray xarray.
    """
    time_df = dataarray.coords["time"].to_dataframe()
    return time_df.set_index("time")


def merge_hour_day_profile_with_time_df(
    profile_df: pd.DataFrame, time_df: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    """
    Fusionne un profil pivoté avec un DataFrame de temps.
    """
    time_df = time_df.copy()
    time_df["hour"] = time_df.index.hour
    time_df["weekday"] = time_df.index.weekday + 1

    merged_df = time_df.merge(profile_df[columns], on=["hour", "weekday"], how="left")
    return merged_df.drop(columns=["hour", "weekday"])


def merge_year_profile_with_time_df(
    profile_df: pd.DataFrame, time_df: pd.DataFrame, columns: List[str]
) -> pd.DataFrame:
    """
    Fusionne un profil pivoté avec un DataFrame de temps.
    """
    time_df = time_df.copy()
    time_df["year"] = time_df.index.year
    merged_df = time_df.merge(profile_df[columns], on=["year"], how="left")

    return merged_df.drop(columns=["year"])


def pivot_area_hour_day_profile(profile_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivote un profil semainier horaire par zones.
    """
    return profile_df.pivot(
        index=["hour", "weekday"],
        columns="area",
        values="electrical_power_per_million_ev_MW",
    )


def pivot_area_year_profile(profile_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivote un profil par années par zones.
    """
    return profile_df.pivot(index=["year"], columns="area", values="total_number_of_ev")


def pivot_season_hour_day_profile(profile_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivote un profil semainier horaire par saisons.
    """
    return profile_df.pivot(
        index=["hour", "weekday"],
        columns="season",
        values="electrical_power_per_million_ev_MW",
    )
