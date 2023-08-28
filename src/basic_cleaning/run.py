#!/usr/bin/env python
"""
This file extracts raw data from W&B and applies some basic cleaning, exporting the result to a new artifact

Author: Femi Bolarinwa
Date: August 2023
"""

import argparse
import logging
import wandb
import os
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    '''
    Function performs basic cleaning on raw data extracted from wandb.
    Input: argparse argument described in if __name__ == "__main__".
    Output: none
    '''


    #initializing wandb run
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    #extracting input artifact from wandb
    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    logger.info("reading artifact")
    df = pd.read_csv(artifact_path)

    #removing outliers
    logger.info("cleaning artifact")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    #converting last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv("clean_sample.csv", index=False)

    #logging cleaned data (output artifact) to wandb
    artifact = wandb.Artifact(
         args.output_artifact,
         type=args.output_type,
         description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging artifact")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="name_of_file.csv",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name_of_file.csv",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="basic_cleaning",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="This file has undergone some basic cleaning",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price of rental to include in data",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price of rental to include in data",
        required=True
    )


    args = parser.parse_args()

    go(args)
