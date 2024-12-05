# utilities.py

import xarray as xr
import os
import pandas as pd
import csv

# --------------------------------------------------------
# Gestion des fichiers et lecture/écriture des csv
# --------------------------------------------------------

# Détermine le dossier racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Déclare le chemin vers le dossier "data"
data_path = os.path.join(ROOT_DIR, "data")

# Vérifie si le dossier "data" existe, sinon le crée
if not os.path.exists(data_path):
    os.makedirs(data_path)


def save_xarray_into_csv_file(xarray_file: xr.Dataset, filename: str) -> None:
    """
    Export an xarray Dataset or DataArray to a CSV file.

    This function converts the input xarray object into a pandas DataFrame,
    resets its index to include all dimensions (e.g., time, country),
    and then saves the DataFrame as a CSV file at the specified location.

    Args:
        xarray_file (xarray.Dataset or xarray.DataArray): The xarray object to be exported.
        filename (str): The path where the CSV file will be saved.

    Raises:
        ValueError: If the xarray object cannot be converted to a DataFrame.
        IOError: If there is an issue with writing the CSV file.

    Example:
        >>> ds = xr.Dataset({
        ...     "temperature": (("time", "location"), [[15, 20], [17, 22]]),
        ...     "humidity": (("time", "location"), [[80, 70], [85, 75]]),
        ... }, coords={"time": ["2023-01-01", "2023-01-02"], "location": ["A", "B"]})
        >>> save_xarray_into_csv_file(ds, "output.csv")
    """
    try:
        # Convert to pandas DataFrame
        xarray_to_df = xarray_file.to_dataframe()

        # Reset the index to include dimensions
        xarray_to_df.reset_index(inplace=True)

        save_path = os.path.join(data_path, filename)

        # Vérifie si le fichier existe déjà
        if os.path.exists(save_path):
            raise IOError(
                f"Le fichier {filename} existe déjà dans le dossier {data_path}."
            )

        # Export to CSV
        xarray_to_df.to_csv(save_path, index=False, encoding="utf-8")

        print(f"Xarray exported to {save_path} successfully.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except IOError as ioe:
        print(f"IOError: {ioe}")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_csv_dataset(filename: str) -> pd.DataFrame:
    file_path = os.path.join(data_path, filename)

    # Détecter automatiquement le séparateur
    with open(file_path, "r", encoding="utf-8") as file:
        sample = file.read(1024)  # Lire un échantillon du fichier
        sniffer = csv.Sniffer()
        detected_delimiter = sniffer.sniff(sample).delimiter

    # Charger le fichier CSV avec le séparateur détecté
    return pd.read_csv(file_path, sep=detected_delimiter, encoding="utf-8")


# --------------------------------------------------------
# Gestion des datasets xarray
# --------------------------------------------------------


def create_empty_xarray_dataset(dataset_name: str) -> xr.Dataset:
    """
    Crée un dataset xarray vide.
    """
    return xr.Dataset(attrs={"name": dataset_name})


def add_dataarray_to_dataset(
    dataset: xr.Dataset, dataarray: xr.DataArray
) -> xr.Dataset:
    """
    Ajoute un DataArray à un Dataset.
    """
    if dataarray.name in dataset.data_vars:
        raise ValueError(f"La variable '{dataarray.name}' existe déjà dans le Dataset.")
    dataset[dataarray.name] = dataarray
    return dataset


def create_demand_xarray(demand_df: pd.DataFrame) -> xr.DataArray:
    """
    Convertit un dataframe de demand au format pommes en xr.DataArray
    :param demand_df: pd.DataFrame de demand
    :return: demand_xr: xr.DataArray de demand
    """

    required_columns = ["area", "year_op", "resource", "hour", "demand"]
    if not set(required_columns).issubset(demand_df.columns):
        raise ValueError(
            f"Les colonnes requises {required_columns} ne sont pas toutes présentes dans le DataFrame."
        )

    # Pivoter le DataFrame pour organiser les données dans les dimensions souhaitées
    demand_pivot_df = pivot_demand_dataframe(demand_df)

    # Créer un Dataset xarray à partir du DataFrame pivoté
    demand_ds = demand_pivot_df.set_index(
        ["area", "year_op", "resource", "hour"]
    ).to_xarray()

    return demand_ds["demand"].rename("demand")


def pivot_demand_dataframe(demand_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivote le dataframe de demande
    :param demand_df: pd.DataFrame de demand
    :return: pivoted dataframe : pd.DataFrame
    """
    return demand_df.pivot_table(
        index=["area", "year_op", "resource", "hour"], values="demand"
    ).reset_index()
