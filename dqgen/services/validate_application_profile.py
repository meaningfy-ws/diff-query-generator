import pandas as pd
import great_expectations as ge


def is_valid_ap(application_profile_df: pd.DataFrame):
    expected_columns = ["class", "property", "object property", "modifiable", "language dependent", "property group"]
    gdf = ge.from_pandas(application_profile_df)
    return gdf.expect_table_columns_to_match_set(column_set=expected_columns,
                                                 exact_match=True).success
