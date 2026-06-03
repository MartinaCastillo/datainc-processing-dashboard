import pandas as pd


REQUIRED_COLUMNS = [
    "name",
    "email",
    "birth_date",
]


class CSVProcessor:

    @staticmethod
    def validate(df):

        missing = [
            col
            for col in REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

    @staticmethod
    def normalize(df):

        # fechas
        if "birth_date" in df.columns:
            df["birth_date"] = (
                pd.to_datetime(
                    df["birth_date"],
                    errors="coerce"
                )
                .dt.strftime("%Y-%m-%dT%H:%M:%S")
            )

        # texto a mayúsculas
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.upper()
            )

        # vacíos -> NULL
        df = df.fillna("NULL")

        return df