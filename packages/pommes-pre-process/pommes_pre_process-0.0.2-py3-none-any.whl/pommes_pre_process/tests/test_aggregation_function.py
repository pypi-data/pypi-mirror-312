import xarray as xr
import numpy as np
from pommes_pre_process.src.aggregation import aggregate_data, apply_aggregation_rules, aggregation_rules

def test_aggregate_data():
    # Creating a sample data dataset
    data_array = xr.DataArray(
        data=np.random.rand(11, 8760, 5, 1) * 100000,  # Generating random values for demonstration
        dims=['area', 'hour', 'resource', 'year_op'],
        coords={
            'area': ['FR', 'DE', 'ES', 'BE', 'IT', 'PT', 'CH', 'NL', 'AT', 'Nordic', 'PL_CZ'],
            'hour': np.arange(1, 8761),
            'resource': ['electricity', 'hydrogen', 'natural_gas', 'coal', 'lignite'],
            'year_op': [2050]
        },
        name='data'
    )

    # Define area groups
    area_groups = {
        'Western_Europe': ['FR', 'DE', 'BE', 'NL', 'CH'],
        'Southern_Europe': ['ES', 'IT', 'PT'],
        'Central_Europe': ['AT', 'PL_CZ'],
        'Nordic': ['Nordic']
    }

    # Test aggregation with sum
    aggregated_sum = aggregate_data(data_array, area_groups, dim_to_aggregate='area', aggregation_func='sum')
    print("Aggregated with sum:\n", aggregated_sum)

    # Test aggregation with mean
    aggregated_mean = aggregate_data(data_array, area_groups, dim_to_aggregate='area', aggregation_func='mean')
    print("Aggregated with mean:\n", aggregated_mean)

    # Test aggregation with min
    aggregated_min = aggregate_data(data_array, area_groups, dim_to_aggregate='area', aggregation_func='min')
    print("Aggregated with min:\n", aggregated_min)

    # Test aggregation with max
    aggregated_max = aggregate_data(data_array, area_groups, dim_to_aggregate='area', aggregation_func='max')
    print("Aggregated with max:\n", aggregated_max)

def test_apply_aggregation_rules():
    # Creating a sample data dataset
    data_array = xr.DataArray(
        data=np.random.rand(11, 8760, 5, 1) * 100000,  # Generating random values for demonstration
        dims=['area', 'hour', 'resource', 'year_op'],
        coords={
            'area': ['FR', 'DE', 'ES', 'BE', 'IT', 'PT', 'CH', 'NL', 'AT', 'Nordic', 'PL_CZ'],
            'hour': np.arange(1, 8761),
            'resource': ['electricity', 'hydrogen', 'natural_gas', 'coal', 'lignite'],
            'year_op': [2050]
        },
        name='demand'
    )

    # Creating a sample dataset
    parameters = xr.Dataset({'demand': data_array})

    # Define area groups
    area_groups = {
        'Western_Europe': ['FR', 'DE', 'BE', 'NL', 'CH'],
        'Southern_Europe': ['ES', 'IT', 'PT'],
        'Central_Europe': ['AT', 'PL_CZ'],
        'Nordic': ['Nordic']
    }

    # Apply aggregation rules to the parameters dataset
    aggregated_parameters = apply_aggregation_rules(parameters, aggregation_rules, dim_to_aggregate='area', group_dict=area_groups)
    print("Aggregated parameters:\n", aggregated_parameters)

if __name__ == "__main__":
    print("Testing aggregate_data function:")
    test_aggregate_data()
    print("\nTesting apply_aggregation_rules function:")
    test_apply_aggregation_rules()
