import pandas as pd

CSV_NAME = "src/app/data/lehrplan-21-kanton-st-gallen.csv"
DF_CSV = pd.read_csv(CSV_NAME, sep=";", encoding="utf-8")


def get_all_subjects() -> list:
    return list(DF_CSV["code"].dropna().str.split(".").str[0].unique())


def get_compentencies_for_subject_code(
    code: str = ""
) -> pd.DataFrame:
    return DF_CSV.query(f'strukturtyp == "Kompetenz" & code.str.contains("{code}")')


if __name__ == "__main__":
    df_subj = get_compentencies_for_subject_code()
    subjects = get_all_subjects()
