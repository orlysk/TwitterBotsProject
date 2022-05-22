import pandas as pd
from typing import List


def merge_dfs_files(files_paths: List[str]) -> pd.DataFrame:
    original_dfs = []
    for file_path in files_paths:
        current_df = pd.read_csv(file_path)
        current_df = current_df[current_df['account_id'].notna()]
        current_df = current_df.astype({"account_id": "int64"})
        original_dfs.append(current_df)
    merged_df = pd.concat(original_dfs, ignore_index=True)
    return merged_df
