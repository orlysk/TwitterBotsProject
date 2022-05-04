import pandas as pd
from typing import List


def merge_dfs_files(files_paths: List[str]) -> pd.DataFrame:
    original_dfs = []
    for file_path in files_paths:
        original_dfs.append(pd.read_csv(file_path))
    merged_df = pd.concat(original_dfs)
    return merged_df
