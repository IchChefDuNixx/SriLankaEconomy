import json
from os import PathLike
import pandas as pd


def load_sl_events(path: str | PathLike[str]) -> dict[int, dict[str, int | str]]:
    try:
        with open(path, "r") as f:
            data = json.load(f)

        # Convert the keys to integers for convenience
        data = {int(key): value for key, value in data.items()}
        return data

    except Exception as e:
        print(e)
        return {}


# df.xs() may return a pd.Series and .to_frame() doesn't satisfy type checking for some reason
def load_inflation_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = pd.DataFrame(df.xs('Germany', level=1))
    sl = pd.DataFrame(df.xs('Sri Lanka', level=1))
    return {"de": de, "sl": sl}


def load_GDP_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = pd.DataFrame(df.xs('Germany', level=1))
    sl = pd.DataFrame(df.xs('Sri Lanka', level=1))
    return {"de": de, "sl": sl}


def load_happiness_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = pd.DataFrame(df.xs('Germany', level=1))
    sl = pd.DataFrame(df.xs('Sri Lanka', level=1))
    return {"de": de, "sl": sl}


def load_tourism_data(path: str | PathLike[str]) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(path, index_col=[0, 1])
    de = pd.DataFrame(df.xs('Germany', level=1))
    sl = pd.DataFrame(df.xs('Sri Lanka', level=1))
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
