# Project: Build an ML Pipeline for Short-Term Rental Prices in NYC

## Project Description

A property management company renting rooms and properties for short periods of 
time on various rental platforms needs a ML model to estimate the typical price for a given property based 
on the price of similar properties. The company receives new data in bulk every week. The model needs 
to be retrained with the same cadence, necessitating a need for an end-to-end pipeline that can be reused.

## Repository Content Description
Overview of the content in repository:

1)Components: contains components constituting the ML pipeline. See README inside directory

2)cookie-mlflow-step: contains template to quickly generate new component steps to be used with MLFlow. See README inside directory

3)src: contains components constituting the ML pipeline. Each component contains its own conda.yml, MLproject and run.py script.

4)MLproject: an MLproject for the main pipeline

5)conda.yml: defines all dependencies of the conda environment needed for main pipeline

6)config.yaml: configuration file containing parameters for the pipeline. Configuration managed by hydra

7)environment.yml: contains all dependencies for conda environment isolation

8)main.py: drives entire pipeline

9)pipeline graph/wandb end-to-end pipeline graph.png shows entire ML pipeline and its components in graph view. Extracted from wandb

## ML pipeline artifact/experiment tracking
Please find my ML pipeline artifacts and experiment on Weights & Biases: https://wandb.ai/f3bolarinwa/MLOps_nyc_airbnb

## Github Repository for Releases
https://github.com/f3bolarinwa/MLOps_project_ml_pipeline.git

## Running Files
1)Clone git repository on your local machine by executing:
git clone https://github.com/f3bolarinwa/MLOps_project_ml_pipeline.git

2)Navigate to repository on local machine

3)create a conda environment on local machine by executing in terminal:
"conda env create -f environment.yml"

4)activate conda by executing in terminal:
"conda activate nyc_airbnb_dev"

5)Ensure you have a wandb account (for ML model,artifact, experiment tracking). Get your API key from W&B by going to: https://wandb.ai/authorize

6)Login to wandb by executing in terminal:
"wandb login [your API key]"

7)Run first two ML pipeline components by executing in terminal:
mlflow run . -P steps=download,basic_cleaning

8)Go to wandb, examine artifacts. Tag data artifact clean_sample.csv as "reference" for data test/validation

9)Test and validate data by executing:
mlflow run . -P steps=data_check

10)Train ML model by executing:
mlflow run . -P steps=data_split,train_random_forest

11)Conduct hyperparamter optimization by using hydra sweep:
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 -m"

12)Go to wandb and examine runs, metrics and artifacts. Tag best performing model artifact (random_forest_export) as "prod",

13)To test model on unseen test data, execute:
mlflow run . -P steps=test_regression_model

14)Train the model on a new data sample by executing in terminal:
mlflow run https://github.com/f3bolarinwa/MLOps_project_ml_pipeline.git -v 1.0.1 -P hydra_options="etl.sample='sample2.csv'"
