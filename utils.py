import pandas as pd
from enum import Enum


def optimize_dataframe_types(df):
    # Downcast integer columns
    int_cols = df.select_dtypes(include=["int"]).columns
    df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast="signed")

    # Downcast float columns
    float_cols = df.select_dtypes(include=["float"]).columns
    df[float_cols] = df[float_cols].apply(pd.to_numeric, downcast="float")

    # Convert object columns to category where appropriate
    # Adjust this based on your knowledge of the data
    for col in df.select_dtypes(include=["object"]).columns:
        num_unique_values = len(df[col].unique())
        num_total_values = len(df[col])
        if num_unique_values / num_total_values < 0.5:
            df[col] = df[col].astype("category")

    return df


def enum2dict(en: Enum):
    """
    Converts an Enum to a dictionary.

    Args:
        en (Enum): The Enum to convert.

    Returns:
        dict: A dictionary representation of the Enum, where the keys are the member names and the values are the member values.
    """
    return {member.name: member.value for member in en}
