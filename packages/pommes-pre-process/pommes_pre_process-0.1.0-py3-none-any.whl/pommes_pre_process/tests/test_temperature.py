import pandas as pd
import numpy as np
import xarray as xr
import pytest

from pommes_pre_process.src.temperature import (
    create_temperature_xarray,
    convert_temperature_xarray_to_export_format,
)

from pommes_pre_process.src.utilities import read_csv_dataset, save_xarray_into_csv_file

@pytest.fixture
def temperature_df():
    return read_csv_dataset("areas_temperatures.csv")

def test_create_and_convert_temperature_xarray(temperature_df):
    temperature_xr = create_temperature_xarray(temperature_df)
    print(temperature_xr)
    new_temperature_xr = convert_temperature_xarray_to_export_format(temperature_xr)
    print(new_temperature_xr)

    save_xarray_into_csv_file(new_temperature_xr, 'test_temp.csv')


def test_create_temperature_xarray():
    """
    Test the initialize_xarray_from_area_temperature function by verifying
    the structure, dimensions, and data of the resulting xarray DataArray.
    """
    # Création d'un DataFrame de test
    data = {
        "temperature_FR": [15, 16, 17],
        "temperature_GE": [10, 11, 12],
    }
    index = pd.date_range("2023-01-01", periods=3)
    test_df = pd.DataFrame(data, index=index)

    # Exécution de la fonction à tester
    temperature_xr = create_temperature_xarray(test_df)

    # Assertions sur les dimensions et coordonnées
    assert "time" in temperature_xr.dims, "La dimension 'time' est absente."
    assert "area" in temperature_xr.dims, "La dimension 'area' est absente."
    assert list(temperature_xr.coords["area"].values) == [
        "FR",
        "GE",
    ], "Les coordonnées 'area' ne correspondent pas aux colonnes du DataFrame."
    assert (
        len(temperature_xr.coords["time"]) == 3
    ), "La dimension 'time' est incorrecte."

    # Assertions sur les données
    expected_data = np.array([[15, 10], [16, 11], [17, 12]])
    np.testing.assert_array_equal(
        temperature_xr.values,
        expected_data,
        "Les données de température ne correspondent pas aux attentes.",
    )

    print("Test passed for initialize_xarray_from_area_temperature.")


def test_convert_temperature_xarray_to_export_format():
    # Préparation des données d'entrée
    time = pd.date_range("2024-01-01", periods=3, freq="H")
    areas = ["area1", "area2"]
    data = np.array([[10.0, 15.0], [12.0, 16.0], [14.0, 18.0]])
    temperature_xr = xr.DataArray(
        data,
        dims=["time", "area"],
        coords={"time": time, "area": areas},
        name="temperature",
    )

    # Appel de la fonction
    result = convert_temperature_xarray_to_export_format(temperature_xr)

    # Vérification des dimensions et coordonnées
    assert list(result.dims) == ["area", "year_op", "hour"]
    assert list(result.coords["area"].values) == areas
    assert "year_op" in result.coords
    assert "hour" in result.coords
    assert "time" not in result.coords
    assert np.array_equal(result.coords["year_op"].values, [2024])
    assert np.array_equal(result.coords["hour"].values, [1, 2, 3])
