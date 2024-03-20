import pandas as pd

CSV_NAME = "data/lehrplan-21-kanton-st-gallen.csv"


def get_compentencies_for_subject_code(
    code: str
) -> pd.DataFrame:
    df_csv = pd.read_csv(CSV_NAME, sep=";", encoding="utf-8")
    return df_csv.query(f'strukturtyp == "Kompetenz" & code.str.contains("{code}")')


df_subj = get_compentencies_for_subject_code("MA")
