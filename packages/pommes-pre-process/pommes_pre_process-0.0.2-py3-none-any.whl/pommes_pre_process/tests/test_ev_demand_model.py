import xarray as xr
import numpy as np
import pandas as pd
import pytest

from pommes_pre_process.src.ev_demand_model import (
    pivot_area_hour_day_profile,
    create_consumption_per_million_ev_xarray_dataset,
    extract_time_dimension_from_xarray,
    pivot_season_hour_day_profile,
    calculate_thermal_sensitivity,
    create_area_ev_fleet_xarray,
    compute_total_consumption_to_xarray_dataset,
    extract_total_demand_from_xarray_dataset_and_convert_format,
    sum_exogenous_demand_and_electric_vehicle_demand,
    create_total_consumption_xarray_dataset
)

from pommes_pre_process.src.temperature import (
    ensure_datetime_index,
    create_temperature_xarray,
)

from pommes_pre_process.src.utilities import (
    read_csv_dataset,
    save_xarray_into_csv_file,
    create_demand_xarray,
)

# --------------------------------------------------------
# Importation des fichiers fixtures
# --------------------------------------------------------

@pytest.fixture
def temperature_df():
    return read_csv_dataset("areas_temperatures.csv")

@pytest.fixture
def profile_df():
    return read_csv_dataset("ev_areas_demand_profiles.csv")

@pytest.fixture
def calibration_profile_df():
    return read_csv_dataset("ev_calibration_profile.csv")

@pytest.fixture
def ev_fleet_df():
    return read_csv_dataset("ev_fleets.csv")

@pytest.fixture
def exo_demand_df():
    return read_csv_dataset("demand.csv")

# --------------------------------------------------------
# Fonctions test
# --------------------------------------------------------

def test_create_total_consumption_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        ev_fleet_df
):

    ev_total_demand_xr = create_total_consumption_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        ev_fleet_df,
        15,
        0,
        True,
    )

    print(ev_total_demand_xr)

def test_sum_exogenous_demand_and_electric_vehicle_demand(
        temperature_df,
        calibration_profile_df,
        profile_df,
        ev_fleet_df,
        exo_demand_df):

    temperature_xr = create_temperature_xarray(temperature_df)
    time_df = extract_time_dimension_from_xarray(temperature_xr)
    consumption_xr = create_consumption_per_million_ev_xarray_dataset(
        temperature_df, calibration_profile_df, profile_df, 15, 0, True
    )
    ev_fleet_xr = create_area_ev_fleet_xarray(ev_fleet_df, time_df)

    total_consumption_ev_xr = compute_total_consumption_to_xarray_dataset(
        consumption_xr, ev_fleet_xr
    )

    ev_demand_xr = extract_total_demand_from_xarray_dataset_and_convert_format(
        total_consumption_ev_xr
    )

    exo_demand_xr = create_demand_xarray(exo_demand_df)

    global_demand_xr = sum_exogenous_demand_and_electric_vehicle_demand(
        exo_demand_xr, ev_demand_xr
    )

    print(global_demand_xr)


def test_extract_total_demand_from_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        ev_fleet_df):

    time_df = ensure_datetime_index(pd.DataFrame(temperature_df["time"]))

    consumption_xr = create_consumption_per_million_ev_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        15,
        0,
        True
    )

    ev_fleet_xr = create_area_ev_fleet_xarray(ev_fleet_df, time_df)

    consumption_xr = compute_total_consumption_to_xarray_dataset(
        consumption_xr, ev_fleet_xr
    )

    demand_xr = extract_total_demand_from_xarray_dataset_and_convert_format(
        consumption_xr
    )

    print(demand_xr)


def test_create_total_consumption_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        ev_fleet_df):

    time_df = pd.DataFrame(temperature_df["time"])
    time_df = ensure_datetime_index(time_df)

    consumption_per_mil_xr = create_consumption_per_million_ev_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,
        15,
        0,
        True
    )

    ev_fleet_xr = create_area_ev_fleet_xarray(ev_fleet_df, time_df)

    consumption_xr = compute_total_consumption_to_xarray_dataset(
        consumption_per_mil_xr, ev_fleet_xr
    )


    print(consumption_xr)


def test_create_area_ev_fleet_xarray(
        temperature_df,
        ev_fleet_df):

    time_df = pd.DataFrame(temperature_df["time"])
    time_df = ensure_datetime_index(time_df)

    ev_fleet_xr = create_area_ev_fleet_xarray(ev_fleet_df, time_df)

    print(ev_fleet_xr)


def test_create_consumption_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df,):

    consumption_xr = create_consumption_per_million_ev_xarray_dataset(
        temperature_df,
        calibration_profile_df,
        profile_df, 15,
        0,
        True
    )

    print(consumption_xr)

def test_import_time_dimension_from_xarray():
    # Créer un DataArray avec une dimension 'time'
    time_coords = pd.date_range("2024-01-01", periods=5, freq="D")
    data = xr.DataArray(
        data=np.random.rand(5),
        dims=["time"],
        coords={"time": time_coords},
    )

    # Appeler la fonction
    result = extract_time_dimension_from_xarray(data)

    # Vérifier le type de retour
    assert isinstance(result, pd.DataFrame), "Le résultat doit être un DataFrame"

    # Vérifier que l'index est nommé 'time'
    assert result.index.name == "time", "L'index du DataFrame doit être nommé 'time'"

    # Vérifier que l'index correspond à la coordonnée 'time'
    pd.testing.assert_index_equal(
        result.index,
        data.coords["time"].to_index(),
        obj="L'index du DataFrame doit correspondre à la coordonnée 'time'",
    )

    # Vérifier que le DataFrame est vide (aucune colonne)
    assert (
        result.empty
    ), "Le DataFrame doit être vide car il ne contient que l'index 'time'"

    # Vérifier le nombre de lignes
    assert len(result) == len(
        time_coords
    ), "Le DataFrame doit avoir autant de lignes que la coordonnée 'time'"


def test_create_pivot_profile_by_area():
    profile_df = read_csv_dataset("ev_areas_demand_profiles.csv")

    pivot_profile = pivot_area_hour_day_profile(profile_df)

    print(pivot_profile)

    return pivot_profile


def test_create_date_time_index_in_temperature_df():
    """
    Test the create_datetimeindex_in_temperature_df function to ensure it correctly
    converts the 'time' column to a datetime index.
    """
    # Create a sample temperature DataFrame
    data = {
        "time": ["2023-01-01 12:00", "2023-01-02 14:00"],
        "temperature": [15.5, 16.7],
    }
    temperature_df = pd.DataFrame(data)

    # Expected DataFrame
    expected_df = pd.DataFrame(
        {"temperature": [15.5, 16.7]},
        index=pd.to_datetime(["2023-01-01 12:00", "2023-01-02 14:00"]),
    )
    expected_df.index.name = "time"

    # Call the function
    result_df = ensure_datetime_index(temperature_df)

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result_df, expected_df)

    print("Test passed successfully.")


def test_pivot_profile_by_season():
    """
    Test the pivot_profile_by_season function to ensure it correctly pivots
    a profile DataFrame into seasons ('summer', 'winter') by hour and weekday.
    """
    # Create a sample DataFrame
    data = {
        "hour": [0, 0, 1, 1],
        "weekday": [1, 1, 2, 2],
        "season": ["summer", "winter", "summer", "winter"],
        "electrical_power_per_million_ev_MW": [10.5, 15.3, 12.7, 18.2],
    }
    profile_df = pd.DataFrame(data)

    # Expected pivoted DataFrame
    expected_df = pd.DataFrame(
        {"summer": [10.5, 12.7], "winter": [15.3, 18.2]},
        index=pd.MultiIndex.from_tuples([(0, 1), (1, 2)], names=["hour", "weekday"]),
    )

    # Assign a name to the column index to match the function's output
    expected_df.columns.name = "season"

    # Call the function
    result_df = pivot_season_hour_day_profile(profile_df)

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result_df, expected_df)

    print("Test passed successfully.")


def test_calculate_thermal_sensitivity():
    """
    Test the calculate_thermal_sensitivity function to ensure it correctly computes
    the thermal sensitivity based on winter and summer consumption profiles.
    """
    # Create a sample pivot profile DataFrame
    data = {"winter": [300, 350, 400], "summer": [200, 250, 300]}
    pivot_profile_df = pd.DataFrame(data)

    # Expected thermal sensitivity
    temperature_threshold = 10
    temperature_minimum = 0
    expected_sensitivity = pd.Series([10.0, 10.0, 10.0])

    # Call the function
    result_sensitivity = calculate_thermal_sensitivity(
        pivot_profile_df, temperature_threshold, temperature_minimum
    )

    # Assert that the result matches the expected Series
    pd.testing.assert_series_equal(result_sensitivity, expected_sensitivity)

    print("Test passed successfully.")
