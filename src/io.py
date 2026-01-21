"""I/O helpers for loading Online Retail II data."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd


SHEET_FALLBACKS: List[str] = ["Year 2009-2010", "Year 2010-2011"]


def _normalize_sheet_names(xls: pd.ExcelFile) -> Dict[str, str]:
    return {name.strip(): name for name in xls.sheet_names}


def load_raw_transactions(path: str | Path) -> pd.DataFrame:
    """Load Online Retail II Excel data, concatenating sheets if needed."""

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    xls = pd.ExcelFile(file_path)
    sheet_map = _normalize_sheet_names(xls)

    available_sheets = [sheet_map[name] for name in SHEET_FALLBACKS if name in sheet_map]
    if not available_sheets:
        available_sheets = xls.sheet_names

    frames = [pd.read_excel(xls, sheet_name=sheet) for sheet in available_sheets]
    return pd.concat(frames, ignore_index=True)
