import pandas as pd


class Excel:
    def __init__(self, sheet_path: str, sheet_name: str | None = None) -> None:
        self._df = pd.read_excel(sheet_path, sheet_name=sheet_name)

    @property
    def data(self) -> pd.DataFrame:
        return self._df  # type: ignore

    @property
    def values_list(self) -> list:
        return list(self._df.values)  # type: ignore
