import pandas as pd
import xarray as xr


from pommes_pre_process.src.utilities import create_demand_xarray


def test_create_demand_xarray():
    # Données de test avec toutes les colonnes requises
    data = {
        "area": ["A", "A", "B", "B"],
        "year_op": [2024, 2024, 2024, 2024],
        "resource": ["R1", "R2", "R1", "R2"],
        "hour": [1, 2, 1, 2],
        "demand": [100, 200, 150, 250],
    }
    demand_df = pd.DataFrame(data)

    # Appel de la fonction
    demand_xr = create_demand_xarray(demand_df)

    # Vérifications
    assert isinstance(
        demand_xr, xr.DataArray
    ), "Le résultat doit être un xarray.DataArray"
    assert demand_xr.dims == (
        "area",
        "year_op",
        "resource",
        "hour",
    ), "Les dimensions doivent être correctement définies"
    assert set(demand_xr["area"].values) == {
        "A",
        "B",
    }, "Les zones doivent être correctement incluses"
    assert set(demand_xr["resource"].values) == {
        "R1",
        "R2",
    }, "Les ressources doivent être correctement incluses"
    assert (
        demand_xr.loc["A", 2024, "R1", 1] == 100
    ), "Les données doivent être correctement mappées"
