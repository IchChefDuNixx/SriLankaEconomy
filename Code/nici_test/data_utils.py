from os import PathLike
import pandas as pd


def load_inflation_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, delimiter=';', index_col=0)
    de = df[['Germany']].rename(columns={'Germany': 'Inflation'})
    sl = df[['Sri_Lanka']].rename(columns={'Sri_Lanka': 'Inflation'})
    return {"de": de, "sl": sl}


def load_GDP_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de": de, "sl": sl}


def load_happiness_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = df.xs('Germany', level=1)
    sl = df.xs('Sri Lanka', level=1)
    return {"de": de, "sl": sl}


def load_tourism_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    sl = df.xs('Sri Lanka', level=1)
    de = df.xs('Germany', level=1)
    return {"sl": sl, "de": de}


def load_data(
    inflation_path: str | PathLike[str],
    GDP_path: str | PathLike[str],
    happiness_path: str | PathLike[str],
    tourism_path: str | PathLike[str]
) -> dict[str, dict[str, pd.DataFrame]]:
    data = {
        'inflation': load_inflation_data(inflation_path),
        'GDP': load_GDP_data(GDP_path),
        'happiness': load_happiness_data(happiness_path),
        'tourism': load_tourism_data(tourism_path)
    }
    return data
