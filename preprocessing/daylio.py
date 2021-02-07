import os
import argparse
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def upload_to_S3(s3_url):
    pass


def detect_activity(row, activity_list):
    new_row = row
    mask = [1 if activity in row["activities"] else 0 for activity in activity_list]
    new_row[3:] = mask
    return new_row


def process_raw_csv(csv_path):
    data_df = pd.read_csv(
        csv_path,
        usecols=["full_date", "weekday", "mood", "activities"],
        index_col="full_date",
        parse_dates=True,
    )
    unique_activities = (
        data_df["activities"].str.split(r"\s*\|\s*", expand=True).stack().unique()
    )
    data_df["activities"] = data_df.activities.apply(lambda x: x.split(" | "))
    for activity in unique_activities:
        data_df[activity] = 0
    data_df = data_df.apply(lambda x: detect_activity(x, unique_activities), axis=1)
    data_df.drop(columns="activities", inplace=True)
    data_df = data_df[~data_df.index.duplicated(keep="last")]
    data_df["Exercise"] = data_df[
        [
            "Climbing",
            "Walk",
            "Running",
            "Gym",
            "Swimming",
            "Football",
            "Hiking",
            "Cycling",
            "skate/surf/snow/sand board",
            "Dancing",
        ]
    ].any(axis=1)
    return data_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process raw daylio data")
    parser.add_argument(
        "-p",
        "--path",
        metavar="path",
        type=str,
        help="The path or url to the raw data",
        default=os.getenv("RAW_DAYLIO_PATH"),
    )
    parser.add_argument(
        "-o",
        "--out",
        metavar="out",
        type=str,
        help="The path or url to where to save the processed data as a csv",
        default=os.getenv("DAYLIO_PATH"),
    )
    args = parser.parse_args()

    file_path = args.path
    out_path = args.out
    idata_df = process_raw_csv(file_path)
    idata_df.to_csv(out_path)
    # upload_to_S3(final_df)
