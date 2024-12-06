import pathlib
from importlib import resources
import polars as pl


def get_instances_metadata_path() -> pathlib.Path:
    """Get the path to the instances metadata CSV file."""
    return resources.files("miplib_benchmark") / "data" / "instances.csv"

def load_instances_metadata() -> pl.DataFrame:
    """Load the instances metadata as a pandas DataFrame."""
    path = get_instances_metadata_path()
    df = pl.read_csv(path)
    df = df.rename({
        "InstanceInst.": "instance_name",
        "StatusStat.": "difficulty",
        "VariablesVari.": "n_variables",
        "BinariesBina.": "n_binary_variables",
        "IntegersInte.": "n_integer_variables",
        "ContinuousCont.": "n_continuous_variables",
        "ConstraintsCons.": "n_constraints",
        "Nonz.Nonz.": "n_nonzero_coefficients",
        "SubmitterSubm.": "submitter",
        "GroupGrou.": "group",
        "ObjectiveObje.": "best_known_objective_value",
        "TagsTags.": "tags",
    })
    return df

