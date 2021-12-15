import pandas as pd
import great_expectations as ge

EXPECTED_COLUMNS = ["class", "property", "object property", "property group", "preview property",
                    "preview object property"]


def is_valid_ap(application_profile_df: pd.DataFrame):
    """
    Check if the application profile file meets the expectations
    :param application_profile_df:
    :return:
    """
    gdf = ge.from_pandas(application_profile_df)
    return gdf.expect_table_columns_to_match_set(column_set=EXPECTED_COLUMNS,
                                                 exact_match=True).success


def validate_application_profile(application_profile_df: pd.DataFrame):
    """
    Validating an application profile file
    :param application_profile_df:
    :return:
    """
    if not is_valid_ap(application_profile_df=application_profile_df):
        raise ValueError(f"The chosen application profile is not valid. Make sure it contains the following "
                         f"values {','.join(EXPECTED_COLUMNS)}")
