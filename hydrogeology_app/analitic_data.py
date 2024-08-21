import pandas as pd
from typing import Dict, Text

EQUIVALENT_WEIGHTS_DICT = {
    "Sulfatos (mg/L)": -2 / 96.06,
    "Sodio (mg/L)": 1 / 22.99,
    "Potasio (mg/L)": 1 / 39.1,
    "Nitratos (mg/L)": -1 / 62,
    "Magnesio (mg/L)": 2 / 24.31,
    "Cloruros (mg/L)": -1 / 35.45,
    "Carbonato (mg/L)": -2 / 60.01,
    "Calcio (mg/L)": 2 / 40.08,
    "Bicarbonato (mg/L)": -1 / 61.01,
}


def calculate_meq_table(
    data, dict_rename: Dict, column_parameter: Text, column_value: Text
) -> pd.DataFrame:
    """
    Calculate a table of milliequivalents (meq/L) from input data, applying renaming, 
    pivoting, and unit conversion.

    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing the data to be analyzed.
    dict_rename : dict
        A dictionary mapping original parameter names to their new names, used to rename 
        the values in `column_parameter`.
    column_parameter : str
        The name of the column in the DataFrame that contains the parameters to be 
        analyzed and renamed.
    column_value : str
        The name of the column in the DataFrame that contains the values corresponding 
        to the parameters in `column_parameter`.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with the pivoted data, with columns for each parameter in 
        milliequivalents per liter (meq/L), and additional columns for total cations, 
        total anions, and the percentage error between them.
        
    The resulting DataFrame includes the following calculated columns:
        - "Total Cationes (meq/L)": Sum of calcium, magnesium, sodium, and potassium.
        - "Total Aniones (meq/L)": Sum of chlorides, sulfates, carbonate, bicarbonate, and nitrates.
        - "Error %": The percentage error between the total cations and total anions.

    Notes:
    ------
    - Parameters in `column_parameter` that are not present in `dict_rename` are removed 
      from the DataFrame.
    - Missing columns after renaming are filled with zeros.
    - The function assumes the existence of a global dictionary `EQUIVALENT_WEIGHTS_DICT` 
      that provides conversion factors from mg/L to meq/L for each parameter.
    """
    df_analysis = data.copy()
    df_analysis[column_parameter] = df_analysis[column_parameter].replace(dict_rename)
    index_ = df_analysis.columns.tolist()
    index_.remove(column_parameter)
    index_.remove(column_value)
    df_analysis[index_] = df_analysis[index_].fillna("--")
    df_pivot = pd.pivot_table(
        data=df_analysis,
        values=column_value,
        columns=column_parameter,
        index=index_,
        aggfunc="mean",
    ).reset_index()

    for pivot_column in df_pivot.drop(columns=index_).columns:
        if pivot_column not in dict_rename.values():
            df_pivot.drop(columns=pivot_column, inplace=True)

    for column_param in dict_rename.values():
        if not column_param in df_pivot.columns:
            df_pivot[column_param] = 0

    for key_rename, column_name in dict_rename.items():
        if "null_" in key_rename:
            df_pivot[column_name] = 0

    for key_rename, column_name in dict_rename.items():
        df_pivot[column_name] = df_pivot[column_name].fillna(0)

    for col_param, weight in EQUIVALENT_WEIGHTS_DICT.items():
        df_pivot[col_param.replace("mg/L", "meq/L")] = df_pivot[col_param].apply(
            lambda x: 0 if pd.isna(x) else x * weight
        )
    df_pivot["Total Cationes (meq/L)"] = (
        df_pivot["Calcio (meq/L)"]
        + df_pivot["Magnesio (meq/L)"]
        + df_pivot["Sodio (meq/L)"]
        + df_pivot["Potasio (meq/L)"]
    )
    df_pivot["Total Aniones (meq/L)"] = (
        df_pivot["Cloruros (meq/L)"]
        + df_pivot["Sulfatos (meq/L)"]
        + df_pivot["Carbonato (meq/L)"]
        + df_pivot["Bicarbonato (meq/L)"]
        + df_pivot["Nitratos (meq/L)"]
    )
    df_pivot["Error %"] = (
        (df_pivot["Total Cationes (meq/L)"] + df_pivot["Total Aniones (meq/L)"])
        * 100
        / (df_pivot["Total Cationes (meq/L)"] - df_pivot["Total Aniones (meq/L)"])
    )
    df_pivot["Error %"] = df_pivot["Error %"].apply(abs)
    return df_pivot
