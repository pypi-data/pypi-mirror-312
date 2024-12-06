# thermal_sensitivity_model.py

import xarray as xr

from pommes_pre_process.src.utilities import (
    create_empty_xarray_dataset,
    add_dataarray_to_dataset,
)

# --------------------------------------------------------
# Création des xarrays de demande thermosensible et decomposée
# --------------------------------------------------------

def create_thermal_sensitive_demand_xarray(
    temperature_xr: xr.DataArray, demand_xr: xr.DataArray, temperature_threshold: float
) -> xr.DataArray:
    """
    Calcule la partie thermosensible de la demande
    :param temperature_xr: DataArray contenant les températures par zone et par heure
    :param demand_xr: DataArray contenant les demandes d'énergie par zone, ressource et heure
    :param temperature_threshold: Seuil de température pour calculer la demande thermique
    :return: DataArray contenant la demande thermosensible.
    """

    thermal_sensitivity_xr = create_thermal_sensitivity_xarray(temperature_xr, demand_xr, temperature_threshold)

    thermal_sensitive_demand_xr = (temperature_threshold - temperature_xr) * thermal_sensitivity_xr

    return thermal_sensitive_demand_xr.rename('thermal_sensitive_demand_xr')


def decompose_demand_with_thermal_sensitivity(
    demand_xr: xr.DataArray, thermal_sensitivity_demand_xr: xr.DataArray
) -> xr.Dataset:
    """
    Calcule un DataArray avec la demande non thermosensible et retourne un Dataset avec la demande totale
    et sa décomposition.
    :param demand_xr:
    :param thermal_sensitivity_demand_xr:
    :return:
    """
    non_thermal_sensitive_demand_xr = demand_xr - thermal_sensitivity_demand_xr

    non_thermal_sensitive_demand_xr = non_thermal_sensitive_demand_xr.rename(
        "non_thermal_sensitive_demand_xr"
    )

    decomposed_demand_xr = create_empty_xarray_dataset("decomposed_demand")

    for dataarray in [
        demand_xr,
        thermal_sensitivity_demand_xr,
        non_thermal_sensitive_demand_xr,
    ]:
        decomposed_demand_xr = add_dataarray_to_dataset(decomposed_demand_xr, dataarray)

    return decomposed_demand_xr

def create_thermal_sensitivity_xarray(
        temperature_xr : xr.DataArray,
        demand_xr : xr.DataArray,
        temperature_threshold: float,
) -> xr.DataArray:
    """
    Calcule la thermosensiblité de la demande calculée sur l'heure et l'année.
    :param temperature_xr: DataArray contenant les températures par zone et par heure
    :param demand_xr: DataArray contenant les demandes d'énergie par zone, ressource et heure
    :param temperature_threshold: Seuil de température pour calculer la demande thermique
    :return: DataArray contenant la thermosensibilité.
    """

    # Identifier les dates où la température est sous le seuil
    cold_condition =  temperature_xr <= temperature_threshold

    # Calcule de la thermosensibilité selon l'axe des heures
    thermal_sensitivity_xr = xr.where(cold_condition,
                                      compute_thermal_sensitivity(temperature_xr,demand_xr), 0)

    return thermal_sensitivity_xr.rename('thermal_sensitivity_xr')

# --------------------------------------------------------
# Calcule des coefficients de thermosensibilité
# --------------------------------------------------------

def compute_thermal_sensitivity(temperature_xr: xr.DataArray,
                                demand_xr : xr.DataArray) -> xr.DataArray:
    """
    Calcule la sensibilité thermique (pente) entre la température et la demande pour chaque groupe.
    :param temperature_demand_xr: DataArray contenant la température et la demande pour chaque zone/ressource/heure
    :return: Sensibilité thermique sous forme d'un tableau numpy
    """

    # Calculer la covariance entre température et demande
    covariance = xr.cov(temperature_xr, demand_xr, dim = ['hour','year_op'])  # Covariance entre les deux variables

    # Calculer la variance de la température
    temperature_variance = temperature_xr.var(dim = ['hour', 'year_op'])

    # Calculer la sensibilité thermique (pente)
    thermal_sensitivity = abs(covariance / temperature_variance)

    return thermal_sensitivity

