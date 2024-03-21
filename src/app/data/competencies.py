import pandas as pd

CSV_NAME = "src/app/data/lehrplan-21-kanton-st-gallen.csv"
DF_CSV = pd.read_csv(CSV_NAME, sep=";", encoding="utf-8")
MAPPING = {"MA": "Mathematik", "D": "Deutsch"}
INV_MAPPING = {v: k for k, v in MAPPING.items()}

def get_all_subjects() -> list:
    abbrevs = sorted(list(DF_CSV["code"].dropna().str.split(".").str[0].unique()))[::-1]

    return [MAPPING[abbrev] for abbrev in abbrevs]


def get_compentencies_for_subject_code(
    code: str = ""
) -> pd.DataFrame:
    code = INV_MAPPING.get(code, code)
    return DF_CSV.query(f'strukturtyp == "Kompetenz" & code.str.contains("{code}")')


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop columns where code is not MA or D
    df = df.query('code.str.split(".").str[0] in ["MA", "D"]')

    return df


def get_full_comp_df():
    return DF_CSV


if __name__ == "__main__":
    df_subj = get_compentencies_for_subject_code()
    subjects = get_all_subjects()
    df = clean_data(DF_CSV)
    df.to_csv("src/app/data/lehrplan-21-kanton-st-gallen.csv", sep=";", encoding="utf-8", index=False)

