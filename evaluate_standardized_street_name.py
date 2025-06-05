import pandas as pd
import re

def merge_standardized_street_segment(standardized_df: pd.DataFrame,
                                      street_segment_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges standardized street names with street segments to enrich the data.

    Args:
        standardized_df (pd.DataFrame): standardized street names with identifiers.
        street_segment_df (pd.DataFrame): street segment data with street text and identifiers.

    Returns:
        pd.DataFrame: A DataFrame containing merged street segments with standardized street names.
    """

    # Join standardized_df with streetSegments on STREET_SEGMENT_ID = ID
    street_text_df = pd.merge(
        standardized_df,
        street_segment_df,
        left_on='STREET_SEGMENT_ID',
        right_on='ID'
    )

    return street_text_df


def get_street_segment_aliases(street_text_df: pd.DataFrame,
                               intersections_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges street segments with intersection data to enrich the street segment information.

    Args:
        street_text_df (pd.DataFrame): Street segments with text and standardized street names.
        intersections_df (pd.DataFrame): Intersection data with street names and cross streets.

    Returns:
        pd.DataFrame: A DataFrame containing enriched street segments with intersection data.
    """

    street_text_df["StreetText_lower"] = street_text_df["StreetText"].str.lower()
    intersections_df["StreetText_lower"] = intersections_df["StreetText"].str.lower()
    intersections_df["CrossText_lower"] = intersections_df["CrossText"].str.lower()
    # First join with cd_intersections: match on BookKey and StreetText
    join_street_text_intersection_df = pd.merge(
        street_text_df,
        intersections_df,
        how='left',
        left_on=['BookKey','ImageKey','ImageColumn',"StreetText_lower"],
        right_on=['BookKey','ImageKey','ImageColumn',"StreetText_lower"],
        suffixes=('', '_x1'),
    )

    join_street_text_intersection_df = join_street_text_intersection_df.drop_duplicates()

    # Second join with cd_intersections again to simulate joining b.CrossText = c.StreetText
    final_join = pd.merge(
        join_street_text_intersection_df,
        intersections_df,
        left_on=['BookKey','ImageKey','ImageColumn', 'CrossText_lower'],
        right_on=['BookKey','ImageKey','ImageColumn', 'StreetText_lower'],
        how = 'left',
        suffixes=('', '_x2')
    )

    final_join = final_join.drop_duplicates()

    # Drop unnecessary columns
    drop_columns = ['StreetText_lower_x2','StreetText_lower',
                     'CrossText_lower_x2','CrossText_lower']
    final_join.drop(columns=drop_columns,inplace=True)

    return final_join



def generate_street_alias_lookup(segment_intersection_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a DataFrame with each street segment ID and its potential aliases.

    Returns:
        pd.DataFrame with columns:
            - ID
            - potential_street_alias (set of normalized CrossText_x2 values)
            - potential_street_alias_with_st (same values with " st" appended)
    """

    # Ensure lowercase and stripped spaces for matching
    segment_intersection_df['CrossText_x2_clean'] = segment_intersection_df['CrossText_x2'].fillna('').str.lower().str.strip()

    # Group by segment ID and aggregate aliases into sets
    alias_df = segment_intersection_df.groupby('ID').agg({
        'CrossText_x2_clean': lambda x: set(x)
    }).reset_index()

    # Add "st" version
    alias_df['potential_street_alias'] = alias_df['CrossText_x2_clean']
    alias_df['potential_street_alias_with_st'] = alias_df['CrossText_x2_clean'].apply(
        lambda s: set(alias + ' st' for alias in s)
    )

    # Drop the intermediate clean column
    alias_df.drop(columns=['CrossText_x2_clean'], inplace=True)

    return alias_df



def evaluate_street_text(row: pd.Series,street_col: str, street_infill_col: str, potential_street_alias: set, potential_street_alias_with_st: set) -> pd.Series:
    """
    Evaluates the street text and fills the method based on conditions.
    Args:
        row (pd.Series): A row of the DataFrame containing street text and other attributes.
        potential_street_alias (pd.Series): A row of the Dataframe containing street alias.
        potential_street_alias_with_st (pd.Series): A row of the Dataframe containing street alias with st
    Returns:
        pd.Series: The updated row with the fill method.
    """

    street_text = str(row[street_col]).lower().strip() if pd.notna(row[street_col]) else ''

    stdr_street_components = [
        row.get('STDR_PREFIX_DIRECTION', ''),
        row.get('STDR_PREFIX_TYPE', ''),
        row.get('STDR_STREET_NAME', ''),
        row.get('STDR_SUFFIX_TYPE', ''),
        row.get('STDR_SUFFIX_DIRECTION', '')
    ]

    # Filter out NaNs and empty strings, then join with space
    strd_street_name = ' '.join(str(c) for c in stdr_street_components if pd.notna(c) and str(c).strip()).strip()

    # Split the input into parts
    parts = street_text.strip().split()

    street_text_coalesce_prefix=None
    street_text_coalesce_suffix_with_st=None
    if (pd.notna(row['STDR_PREFIX_DIRECTION']) or pd.notna(row['STDR_SUFFIX_DIRECTION'])) and len(parts) > 1:
        # Prefix format: "W 3RD"
        street_text_coalesce_prefix = parts[-1] + " " + " ".join(parts[:-1])
        # Suffix format: "3RD ST W"
        street_text_coalesce_suffix_with_st  = " ".join(parts[:-1]) + " st" + " " + parts[-1]

    fill_method = pd.NA
    if street_text == strd_street_name.lower():
        fill_method = 'Step1'
    elif street_text + ' st' == strd_street_name.lower():
        row[street_infill_col] = strd_street_name
        fill_method = 'Step2'
    elif strd_street_name.lower() in potential_street_alias:
        fill_method = 'Step3'
    elif strd_street_name.lower() in potential_street_alias_with_st:
        row[street_infill_col] = strd_street_name
        fill_method = 'Step4'

    # ("3RD W")  ----->  ("W 3RD ST"). ("3RD ST W").
    elif (
        (street_text_coalesce_prefix and street_text_coalesce_suffix_with_st) and
        (
            street_text_coalesce_prefix + ' st' == strd_street_name.lower() or
            street_text_coalesce_suffix_with_st == strd_street_name.lower())
        ):
        fill_method = 'Step5'
        row[street_infill_col] = strd_street_name

    # ("3RD W")  ----->  ("W 3RD").
    elif (street_text_coalesce_prefix and street_text_coalesce_prefix == strd_street_name.lower()):
        fill_method = 'Step6'
        row[street_infill_col] = strd_street_name

    row['Fill_method'] = fill_method

    return row

    


if __name__ == '__main__':

    BOOK_KEY = 'txabilene1909johnfworleydire'
    ROOT_PATH = '/home/prashantksi200/Desktop/pythonLearning/'

    # File paths
    CD_INTERSECTIONS_FILE_PATH = f'{ROOT_PATH}/{BOOK_KEY}_intersections.csv'
    STANDARDIZED_FILE_PATH = f'{ROOT_PATH}/{BOOK_KEY}_transformed.parquet'
    STREETSEGMENTS_FILE_PATH = f'{ROOT_PATH}/{BOOK_KEY}.csv'

    # Load the data
    standardized_parquet_df = pd.read_parquet(STANDARDIZED_FILE_PATH, columns=['STREET_SEGMENT_ID', 'STDR_STREET_NAME', 'STDR_SUFFIX_TYPE','STDR_PREFIX_DIRECTION','STDR_PREFIX_TYPE','STDR_SUFFIX_DIRECTION'])
    intersections_csv_df = pd.read_csv(CD_INTERSECTIONS_FILE_PATH, usecols=['ImageKey','ImageColumn','BookKey', 'StreetText', 'CrossText'])
    street_segment_csv_df = pd.read_csv(STREETSEGMENTS_FILE_PATH, usecols=['ID', 'ImageKey','ImageColumn','BookKey', 'StreetText', 'StreetTextLBX'])

    # Clean and merge the data
    merged_street_text_df = merge_standardized_street_segment(standardized_parquet_df, street_segment_csv_df)
    segment_intersection_df = get_street_segment_aliases(merged_street_text_df, intersections_csv_df)

    potential_street_alias = set(segment_intersection_df['CrossText_x2'].fillna('').str.lower().unique())
    potential_street_alias_with_st = set((segment_intersection_df['CrossText_x2'].fillna('').str.lower() + ' st').str.strip().unique())
    # Apply the evaluation logic to each row

    def coalesce_street_text(row: pd.Series) -> str:
        """
        Coalesce the street text from two columns into one
        Convert to lowercase and strip whitespace
        Handle NaN values
        """
        street_x = str(row['StreetText']).lower().strip() if pd.notna(row['StreetText']) else ''
        street_y = str(row['StreetTextLBX']).lower().strip() if pd.notna(row['StreetTextLBX']) else ''
        
        return street_y if street_y else street_x

    segment_intersection_df['preprocessed_street_text'] = segment_intersection_df.apply(
                                                                coalesce_street_text, axis=1)

    USER_COL = "preprocessed_street_text"
    STREET_FILL_COL = "street_infill_col"

    alias_lookup_df = generate_street_alias_lookup(segment_intersection_df)

    # Left-merge with the full street segments DataFrame (merged_street_text_df)
    merged_df_with_aliases = pd.merge(
            merged_street_text_df,
            alias_lookup_df,
            how='left',
            on='ID'
    )

    segment_intersection_df = segment_intersection_df.apply(
                evaluate_street_text,
                axis=1,
                args=(USER_COL, STREET_FILL_COL, potential_street_alias,
                       potential_street_alias_with_st))

    print(segment_intersection_df['Fill_method'].value_counts())
    segment_intersection_df.to_csv('segment_intersection_df_1953_eval.csv', index=False)