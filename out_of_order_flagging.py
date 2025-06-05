import ast
import pandas as pd
import numpy as np
import re
# from sql_interaction import (
#     get_mssql_pyodbc_conn_from_secret,
#     get_sql_query,
#     read_sql_data)

# def load_cd_data(cd_street_segments_book: str, query_file: str) -> pd.DataFrame:
#     """
#     Load data from SQL Server using a stored query file and connection from secrets manager.

#     Parameters:
#     - cdStreetSegmentsBook: Identifier for the book (e.g., file name or key)
#     - query_file: SQL query filename to be loaded

#     Returns:
#     - A DataFrame containing the result of the executed SQL query.
#     """
#     conn_str = get_mssql_pyodbc_conn_from_secret(secret_id='dev/citydirectory/sqllogin')
#     query = get_sql_query(query_file)
    
#     return read_sql_data(pyodbc_connection_string=conn_str, query=query, query_params=(cd_street_segments_book,))



def get_lis_indices_with_duplicates(words: list[str], is_lettered: bool) -> set[int]:
    """
    Compute the indices of the Longest Non-Strictly Increasing Subsequence (LIS) in the list of words.
    This function allows duplicates (non-strict increasing).

    Parameters:
    - words: List of strings representing street names or words.

    Returns:
    - A set of indices corresponding to the LIS elements in the input list.
    """
    # Initialize DP arrays
    n = len(words)
    dp = [1] * n  # dp[i] = length of LIS ending at index i
    prev = [-1] * n  # prev[i] = index of previous element in LIS ending at i

    if is_lettered:
        words = [item.lower() for item in words]

    # Build the LIS dp table
    for i in range(n):
        for j in range(i):
            # If words[i] continues a non-strict increasing sequence from words[j]
            if words[j] <= words[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # Find the end index of the maximum length LIS
    max_len = max(dp)
    idx = dp.index(max_len)

    # Backtrack to collect indices of LIS elements
    lis_indices = set()
    while idx != -1:
        lis_indices.add(idx)
        idx = prev[idx]

    return lis_indices


def flag_out_of_order_streettext(cd_street_df: pd.DataFrame, book_name: str) -> pd.DataFrame:

    """
    Flag out-of-order street names in the city directory data.
    This function loads street segments data and book sections metadata, processes each section,
    and flags street names that are not in the longest increasing alphabetical sequence.
    Parameters:
    - book_name: The name of the book to process (e.g., 'txdallasandsuburb1967cole')
    Returns:
    - A DataFrame with an additional column 'IsOutOfOrderStreetText' indicating out-of-order street names.
    """

    streets_sections_df = load_cd_data(book_name, 'CdBooks_JSON.sql')
    street_sections = ast.literal_eval(streets_sections_df["StreetsSection"].iloc[0])

    print(f"Loaded {len(cd_street_df)} records from CdStreetSegments and {len(street_sections)} sections from CdBook_JSON.")

    # Process each section of the book individually
    for section in street_sections:
        start = int(section['start'])
        end = int(section['end'])

        # Filter rows within the current section range
        section_df = cd_street_df[(cd_street_df['ImageKey'] >= start) & (cd_street_df['ImageKey'] <= end)].copy()

        section_df["StreetColumnNew"] = np.where(
            section_df["StreetColumn"].isna(),
            section_df["ImageColumn"],
            section_df["StreetColumn"]
        )

        section_df["StreetImageNew"] = np.where(
            section_df["StreetImage"].isna(),
            section_df["ImageKey"],
            section_df["StreetImage"]
        )

        section_df["StreetExtent_ymin"] = section_df["StreetExtent"].apply(lambda x: ast.literal_eval(x)[1] if pd.notnull(x) else None)

        df_sorted = section_df.sort_values(by=["StreetImageNew", "StreetColumnNew" ,'StreetExtent_ymin'])
        df_sorted["original_index"] = df_sorted.index

        numbered = df_sorted[df_sorted['StreetText'].str.fullmatch('^[0-9]+.+')].copy()
        lettered = df_sorted[~df_sorted['StreetText'].str.fullmatch('^[0-9]+.+')].copy()

        if numbered.shape[0] > 0:
            flag_numbered_streets(numbered)

        flag_lettered_streets(lettered)

        df_sorted = pd.concat([numbered, lettered]).sort_values(by=["BookKey", "ImageKey", "ImageColumn"]).reset_index(drop=True)
    
        # Mark as True if the row is NOT in the LIS
        cd_street_df.loc[df_sorted["original_index"], "IsOutOfOrderStreetText"] = df_sorted["IsOutOfOrderStreetText"].values

    return cd_street_df


def flag_lettered_streets(lettered: pd.DataFrame):
    """
    Flag out-of-order lettered streets in the DataFrame.
    This function processes lettered street names and flags those that are not in the longest increasing alphabetical sequence.
    Parameters:
    - lettered: DataFrame containing lettered street names.
    Returns:
    - None: The function modifies the input DataFrame in place.
    """

    street_list = lettered["StreetText"].tolist()

    lis_indices = get_lis_indices_with_duplicates(street_list, True)
    in_lis_values = {street_list[i] for i in lis_indices}
    lettered["IsOutOfOrderStreetText"] = ~lettered["StreetText"].isin(in_lis_values)
    

def flag_numbered_streets(numbered: pd.DataFrame):
    """
    Flag out-of-order numbered streets in the DataFrame.
    This function processes numbered street names and flags those that are not in the longest increasing alphabetical sequence.
    Parameters:
    - numbered: DataFrame containing numbered street names.
    Returns:
    - None: The function modifies the input DataFrame in place.
    """

    numbered[['StreetNum', 'StreetTextResidual']] = numbered['StreetText'].apply(
                lambda x: pd.Series(split_street(x))
            )

    street_list = numbered[["StreetNum", "StreetTextResidual"]].values.tolist()
    lis_indices = get_lis_indices_with_duplicates(street_list, False)
    in_lis_values = {tuple(street_list[i]) for i in lis_indices}
    numbered["StreetPair"] = numbered[["StreetNum", "StreetTextResidual"]].values.tolist()

    # Mark as True if the row is NOT in the LIS
    numbered["IsOutOfOrderStreetText"] = ~numbered["StreetPair"].apply(tuple).isin({tuple(p) for p in in_lis_values})

    # Drop temp columns
    numbered.drop(columns=["StreetPair"], inplace=True)


def split_street(street_text: str):
    match = re.match(r'^(\d+)(.*)', street_text)

    return int(match.group(1)), match.group(2).strip()


if __name__ == "__main__":
    cd_street_df = pd.read_csv('data/txtexarkana1947polkdirect.csv')
    df = flag_out_of_order_streettext(cd_street_df, 'txtexarkana1947polkdirect')
    df.to_csv('combined_letter_number.csv')