import xarray as xr
import numpy as np

aggregation_rules = {
    'area': None,
    'link': None,
    'conversion_tech': None,
    'transport_tech': None,
    'hour': None,
    'resource': None,
    'storage_tech': None,
    'year_dec': None,
    'year_inv': None,
    'year_op': None,
    'year_rep': None,
    'conversion': None,
    'carbon': None,
    'transport': None,
    'turpe': None,
    'storage': None,
    'net_import': None,
    'discount_rate': None,
    'year_ref': None,
    'planning_step': None,
    'carbon_tax': None,
    'carbon_goal': None,
    'demand': "sum",
    'conversion_availability': "mean",
    'conversion_emission_factor': "mean",
    'conversion_max_yearly_production': "sum",
    'conversion_ramp_up': "mean",
    'conversion_ramp_down': "mean",
    'conversion_invest_cost': "mean",
    'conversion_fixed_cost': "mean",
    'conversion_variable_cost': "mean",
    'conversion_life_span': "mean",
    'conversion_finance_rate': "mean",
    'conversion_power_capacity_max': "sum",
    'conversion_power_capacity_min': "sum",
    'conversion_power_capacity_investment_max': "sum",
    'conversion_power_capacity_investment_min': "sum",
    'conversion_must_run': "mean",
    'conversion_factor': None,
    'storage_energy_capacity_investment_max': "sum",
    'storage_energy_capacity_investment_min': "sum",
    'storage_power_capacity_investment_max': "sum",
    'storage_power_capacity_investment_min': "sum",
    'storage_invest_cost_energy': "mean",
    'storage_invest_cost_power': "mean",
    'storage_life_span': "mean",
    'storage_fixed_cost_energy': "mean",
    'storage_fixed_cost_power': "mean",
    'storage_finance_rate': "mean",
    'storage_main_resource': None,
    'storage_dissipation': "mean",
    'storage_factor_in': None,
    'storage_factor_out': None,
    'storage_factor_keep': None,
    'spillage_max_capacity': None,
    'spillage_cost': None,
    'load_shedding_max_capacity': None,
    'load_shedding_cost': None,
    'transport_area_from': None,
    'transport_area_to': None,
    'transport_invest_cost': "mean",
    'transport_fixed_cost': "mean",
    'transport_life_span': "mean",
    'transport_finance_rate': "mean",
    'transport_power_capacity_investment_max': "sum",
    'transport_power_capacity_investment_min': "sum",
    'transport_hurdle_costs': "mean",
    'transport_resource': None,
    'net_import_emission_factor': None,
    'net_import_total_emission_factor': None,
    'net_import_import_price': None,
    'net_import_max_yearly_energy_export': "sum",
    'net_import_max_yearly_energy_import': "sum",
    'conversion_end_of_life': "mean",
    'storage_end_of_life': "mean",
    'transport_end_of_life': "mean",
    'conversion_annuity_cost': "mean",
    'transport_annuity_cost': "mean",
    'storage_annuity_cost_power': "mean",
    'storage_annuity_cost_energy': "mean",
    'discount_factor': None,
    'conversion_annuity_perfect_foresight': None,
    'conversion_early_decommissioning': None,
    'storage_annuity_perfect_foresight': None,
    'storage_early_decommissioning': None,
    'transport_annuity_perfect_foresight': None,
    'transport_early_decommissioning': None
}


def first_value_if_identical(values):
    unique_values = np.unique(values)
    unique_values=unique_values.astype('<U20')
    if len(unique_values) == 1:
        return unique_values[0]
    else:
        raise ValueError(f"Values are not identical along dimension 'link'")


def aggregate_transport_resources(transport_resource, link_groups):
    """
    Create a new DataArray for the transport_resource variable for the aggregated links.

    Parameters:
    - transport_resource: xarray.DataArray
        The original transport_resource DataArray with dimensions (link, transport_tech).
    - new_links: xarray.DataArray
        The DataArray containing the new aggregated links.
    - area_groups: dict
        Dictionary defining the area groups. Keys = new groups, values = list of original areas.

    Returns:
    - new_transport_resource: xarray.DataArray
        The aggregated transport_resource DataArray.
    """


    new_links = list(link_groups.keys())
    new_transport_tech = list(transport_resource.coords['transport_tech'].values)
    new_transport_resources = []
    data_vars = {
        'transport_resource': (['link', 'transport_tech'],  np.full((len(new_links), len(new_transport_tech)), "").astype('<U20'))
    }
    coords = {
        'link': new_links,
        'transport_tech': new_transport_tech
    }
    dataset = xr.Dataset(data_vars=data_vars, coords=coords)
    for new_link, old_links in link_groups.items():
        old_areas = transport_resource.sel(link=old_links)
        for tech in old_areas.coords['transport_tech'].values:
            values = [transport_resource.sel(link=old_link, transport_tech=tech).values.flatten().tolist()[0] for old_link in old_links]
            values_without_unknown = [value for value in values if value not in ["unknown","nan",np.nan]]
            if len(values_without_unknown)>0:
                dataset["transport_resource"].loc[{'link': new_link, 'transport_tech': tech}] = values_without_unknown[0]
            else:
                dataset["transport_resource"].loc[{'link': new_link, 'transport_tech': tech}] = "unknown"

    return dataset


def aggregate_data(data_array, group_dict, dim_to_aggregate, aggregation_func='sum'):
    """
    Aggregate data by regrouping according to specified groups.

    Parameters:
    - data_array: xarray.DataArray
        The data to be aggregated, with dimensions including (area, hour, resource, year_op).
    - group_dict: dict
        A dictionary defining the groups. Keys are new group names, values are lists of elements to be aggregated.
    - dim_to_aggregate: str
        The dimension along which to aggregate (e.g., "area" or "hour").
    - aggregation_func: str
        The aggregation function to use ('sum', 'mean', 'min', 'max').

    Returns:
    - aggregated_data: xarray.DataArray
        The aggregated DataArray with the specified dimension replaced by the new groups.
    """
    # Create a new DataArray for storing the aggregated data
    aggregated_data = []
    new_groups = []

    for group_name, elements in group_dict.items():
        # Select the elements to be aggregated

        selected_elements = data_array.sel({dim_to_aggregate: elements})
        # Apply the specified aggregation function
        if aggregation_func == 'sum':
            aggregated_element = selected_elements.sum(dim=dim_to_aggregate,skipna=False)
        elif aggregation_func == 'mean':
            aggregated_element = selected_elements.mean(dim=dim_to_aggregate)
        elif aggregation_func == 'min':
            aggregated_element = selected_elements.min(dim=dim_to_aggregate)
        elif aggregation_func == 'max':
            aggregated_element = selected_elements.max(dim=dim_to_aggregate)
        else:
            raise ValueError(f"Unsupported aggregation function: {aggregation_func}")
        # Append to the aggregated data list
        aggregated_data.append(aggregated_element)
        new_groups.append(group_name)

    # Concatenate all aggregated data along a new dimension
    aggregated_data = xr.concat(aggregated_data, dim=dim_to_aggregate)
    aggregated_data = aggregated_data.assign_coords({dim_to_aggregate: new_groups})

    return aggregated_data

def apply_aggregation_rules(parameters, aggregation_rules, dim_to_aggregate, group_dict,area_group_dict=None):
    """
    Apply aggregation rules to a dataset using the specified dimension and grouping dictionary.

    Parameters:
    - parameters: xarray.Dataset
        The dataset to be aggregated.
    - aggregation_rules: dict
        A dictionary defining the aggregation rules for each variable.
    - dim_to_aggregate: str
        The dimension along which to aggregate (e.g., "area" or "hour").
    - group_dict: dict
        A dictionary defining the groups. Keys are new group names, values are lists of elements to be aggregated.

    Returns:
    - aggregated_dataset: xarray.Dataset
        The aggregated dataset with specified aggregations applied.
    """
    aggregated_data_vars = {}

    for var_name, aggregation_func in aggregation_rules.items():
        if var_name in parameters.data_vars:
            data_var = parameters[var_name]
            if dim_to_aggregate in data_var.dims and aggregation_func is not None:
                aggregated_data_vars[var_name] = aggregate_data(data_var, group_dict, dim_to_aggregate, aggregation_func)
            elif (var_name in ['transport_area_from','transport_area_to']) and dim_to_aggregate=='link':
                tmp_ds = update_transport_area(parameters,link_groups=group_dict,area_groups=area_group_dict)
                aggregated_data_vars[var_name] = tmp_ds[var_name]
            elif (var_name in ['transport_resource']) and dim_to_aggregate=='link':
                aggregated_data_vars[var_name] = aggregate_transport_resources(parameters['transport_resource'], group_dict)["transport_resource"]
            else:
                aggregated_data_vars[var_name] = data_var

    aggregated_dataset = xr.Dataset(aggregated_data_vars)

    return aggregated_dataset

def regroup_links(link_array, area_groups):
    """
    Regroup links based on the new area groups defined.

    Parameters:
    - link_array: xarray.DataArray
        The DataArray representing links between areas.
    - area_groups: dict
        Dictionary defining the area groups. Keys are new group names, values are lists of original areas.

    Returns:
    - new_link_groups: dict
        A dictionary defining the new link groups.
    """
    new_link_groups = {}

    # Invert area_groups to get area to group mapping
    area_to_group = {}
    for group, areas in area_groups.items():
        for area in areas:
            area_to_group[area] = group

    # Regroup links based on area groups
    for link in link_array.values:
        area_from, area_to = link.split('-')

        # Check if both areas exist in the groups
        if area_from in area_to_group and area_to in area_to_group:
            group_from = area_to_group[area_from]
            group_to = area_to_group[area_to]

            # Exclude links within the same group
            if group_from != group_to:
                new_link = f"{group_from}-{group_to}"

                # Add the link to the appropriate group
                if new_link not in new_link_groups:
                    new_link_groups[new_link] = []
                new_link_groups[new_link].append(link)

    return new_link_groups


def map_area_to_group(area, area_groups):
    for group, areas in area_groups.items():
        if area in areas:
            return group
    return 'unknown'


def update_transport_area(transport_area, link_groups, area_groups):

    new_links = list(link_groups.keys())
    new_transport_tech = list(transport_area.coords['transport_tech'].values)
    data_vars = {
        'transport_area_from': (['link', 'transport_tech'],  np.full((len(new_links), len(new_transport_tech)), "").astype('<U20')),
        'transport_area_to': (['link', 'transport_tech'],  np.full((len(new_links), len(new_transport_tech)), "").astype('<U20'))
    }
    coords = {
        'link': new_links,
        'transport_tech': new_transport_tech
    }
    dataset = xr.Dataset(data_vars=data_vars, coords=coords)
    for new_link, old_links in link_groups.items():
        old_areas = transport_area.sel(link=old_links)
        new_area_values = []
        for tech in old_areas.coords['transport_tech'].values:
            tech_areas = old_areas.sel(transport_tech=tech)
            new_areas_from = [map_area_to_group(area, area_groups) for area in tech_areas.transport_area_from]
            new_areas_to = [map_area_to_group(area, area_groups) for area in tech_areas.transport_area_to]
            unique_values = np.unique(list(zip(new_areas_from,new_areas_to)),axis=0)
            if len(unique_values) == 1:
                dataset["transport_area_from"].loc[{'link' : new_link,'transport_tech' : tech}]  = unique_values[0,0]
                dataset["transport_area_to"].loc[{'link' : new_link,'transport_tech' : tech}]  = unique_values[0,1]
            else:
                raise ValueError(f"Conflicting values for link '{new_link}' and transport tech '{tech}'")

    return dataset


def create_aggregation_from_new_area(model_parameters,area_groups):
    '''
    this function creates a new set of parameters from model_parameters with aggregated area described in dictionary area_groups.
    Parameters
    ----------
    model_parameters
    area_groups

    Returns
    -------

    '''

    aggregated_parameters = apply_aggregation_rules(model_parameters, aggregation_rules, dim_to_aggregate='area',
                                                    group_dict=area_groups)
    link_groups = regroup_links(model_parameters.coords['link'], area_groups)
    aggregated_parameters = apply_aggregation_rules(aggregated_parameters, aggregation_rules, dim_to_aggregate='link',
                                                    group_dict=link_groups,    area_group_dict=area_groups)

    aggregated_parameters = aggregated_parameters.where(aggregated_parameters != "unknown", np.nan)
    return aggregated_parameters