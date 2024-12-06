import pytest
import pandas as pd

from pommes_pre_process.src.utilities import (
    read_csv_dataset,
    save_xarray_into_csv_file,
    create_demand_xarray,
)

from pommes_pre_process.src.temperature import (
    create_temperature_xarray,
    convert_temperature_xarray_to_export_format,
)

from pommes_pre_process.src.thermal_sensitivity_model import (
    create_thermal_sensitive_demand_xarray,
    decompose_demand_with_thermal_sensitivity,
    compute_thermal_sensitivity, create_thermal_sensitivity_xarray
)

# --------------------------------------------------------
# Importation des fichiers fixtures
# --------------------------------------------------------

@pytest.fixture
def temperature_df():
    return read_csv_dataset("areas_temperatures.csv")

@pytest.fixture
def demand_df():
    return read_csv_dataset("demand.csv")

# --------------------------------------------------------
# Fonctions test
# --------------------------------------------------------

def test_create_thermal_sensitivity_xarray(temperature_df, demand_df):
    temperature_xr = convert_temperature_xarray_to_export_format(create_temperature_xarray(temperature_df))
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitivity_xr = create_thermal_sensitivity_xarray(temperature_xr, demand_xr, 15)

    print(thermal_sensitivity_xr)
    
def test_compute_thermal_sensitivity(temperature_df, demand_df):

    temperature_xr = create_temperature_xarray(temperature_df)
    temperature_xr = convert_temperature_xarray_to_export_format(temperature_xr)
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitivity_xr = compute_thermal_sensitivity(temperature_xr, demand_xr)

    print(thermal_sensitivity_xr)

def test_create_thermal_sensitive_demand_xarray(temperature_df, demand_df):

    temperature_xr = convert_temperature_xarray_to_export_format(create_temperature_xarray(temperature_df))
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitivity_xr = create_thermal_sensitive_demand_xarray(temperature_xr, demand_xr, 15)

    print(thermal_sensitivity_xr)

def test_extract_thermal_sensitivity_part_of_demand(temperature_df, demand_df):
    temperature_xr = create_temperature_xarray(temperature_df)
    temperature_xr = convert_temperature_xarray_to_export_format(temperature_xr)
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitive_demand = create_thermal_sensitive_demand_xarray(temperature_xr, demand_xr, 15)

    print(thermal_sensitive_demand)

def test_decompose_demand_with_thermal_sensitivity(temperature_df, demand_df):


    temperature_xr = convert_temperature_xarray_to_export_format(
        create_temperature_xarray(temperature_df)
    )
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitive_demand_xr = create_thermal_sensitive_demand_xarray(
        temperature_xr, demand_xr, 15
    )

    decomposed_demand_xr = decompose_demand_with_thermal_sensitivity(
        demand_xr, thermal_sensitive_demand_xr
    )

    print(decomposed_demand_xr)

