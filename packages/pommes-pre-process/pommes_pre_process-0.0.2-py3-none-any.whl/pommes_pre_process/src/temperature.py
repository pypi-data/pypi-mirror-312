# temperature.py

import pandas as pd
import xarray as xr
import numpy as np


# --------------------------------------------------------
# Création et modification des DataArray
# --------------------------------------------------------


def create_temperature_xarray(temperature_df: pd.DataFrame) -> xr.DataArray:
    """
    Convertit un DataFrame de températures en un DataArray xarray.
    """
    temperature_df = ensure_datetime_index(temperature_df)

    if not all(col.startswith("temperature_") for col in temperature_df.columns):
        raise ValueError("Les colonnes doivent suivre le format 'temperature_<area>'.")

    areas = [col.split("_", 1)[-1] for col in temperature_df.columns]
    temperature_data = np.column_stack(
        [temperature_df[f"temperature_{area}"].values for area in areas]
    )

    return xr.DataArray(
        temperature_data,
        dims=["time", "area"],
        coords={"time": temperature_df.index, "area": areas},
        name="temperature",
    ).sortby("area")  # DataArray trié par région par ordre alphabétique


def convert_temperature_xarray_to_export_format(
    temperature_xr: xr.DataArray,
) -> xr.DataArray:
    # Vérification des données nécessaires
    if "time" not in temperature_xr.coords:
        raise ValueError("La coordonnée 'time' est absente du DataArray.")
    if "area" not in temperature_xr.coords:
        raise ValueError("La coordonnée 'area' est absente du DataArray.")

    time = temperature_xr.coords["time"]
    # Calculer les heures depuis le début de l'année
    hour = (time.dt.dayofyear.data - 1) * 24 + time.dt.hour.data + 1

    # Assignation des nouvelles coordonnées
    temperature_xr = temperature_xr.assign_coords(
        year_op=("time", time.dt.year.data), hour=("time", hour)
    )

    # Réorganiser pour que year_op et hour soient des dimensions séparées
    temperature_xr = temperature_xr.set_index(time=["year_op", "hour"])

    # "Unstack" de la dimension 'time' pour obtenir 'year_op' et 'hour' comme dimensions séparées
    temperature_xr = temperature_xr.unstack("time")

    # Réorganiser pour que 'area' soit la première dimension
    temperature_xr = temperature_xr.transpose("area", "year_op", "hour")

    return temperature_xr


# --------------------------------------------------------
# Préparation et utilitaires
# --------------------------------------------------------


def ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    S'assure que le DataFrame a un index datetime valide.
    """
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], format="mixed", errors="coerce")
        df.set_index("time", inplace=True)

    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    return df
