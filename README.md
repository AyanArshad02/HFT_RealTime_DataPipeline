# HFT Real-Time Data Pipeline

This project implements an MLOps framework utilizing ZenML for automating the real-time processing of stock data. The pipeline ingests, processes, and stores financial data, applying various data transformations and handling missing values, followed by feature engineering.

## Overview
The pipeline is composed of several steps:

1. Fetch Data: Fetch stock data for a given ticker symbol.
2. Ingest Data: Process the raw data and prepare it for further processing.
3. Handle Missing Values: Identify and handle any missing values in the stock data.
4. Feature Engineering: Generate new features based on the stock data.
5. Store Processed Data: Store the processed data in a PostgreSQL database.

## Setup

### Prerequisites:

- Python 3.x
- ZenML
- PostgreSQL (for storing processed data)
- A virtual environment (for managing dependencies)

### Installation:
Clone the repository and install the necessary dependencies:
```
git clone https://github.com/AyanArshad02/HFT_RealTime_DataPipeline.git
cd HFT_RealTime_DataPipeline
pip install -r requirements.txt
```

### Setting up the Virtual Environment:
If you're using Conda, create a virtual environment:
```
conda create --name myenv python=3.8
conda activate myenv
```

### Database Setup:
Configure PostgreSQL with the necessary parameters to store processed stock data. You can modify the database connection settings in utils/config.py.

## Running the Pipeline
To run the pipeline manually:
```
python pipelines/run_pipeline.py
```

This will execute the entire data pipeline, from data ingestion to storing the processed data.

## Automating the Pipeline
To automate the pipeline to run daily at 10 PM, use the provided setup_daily_pipeline.sh script. It will set up a cron job for you:

```
bash setup_daily_pipeline.sh
```
The cron job will run the pipeline every day at 10 PM, using the specified virtual environment. Logs will be stored in pipeline_cronjob.log.

## Folder Structure
1. src: Contains the core functionality, including data ingestion, feature engineering, and data storage.
2. steps: Defines individual steps in the ZenML pipeline.
3. pipelines: Contains the pipeline definition and logic for the data pipeline.
4. setup.py: For packaging the project.
5. setup_daily_pipeline.sh: A script to schedule the pipeline to run daily.


## ZenML Integration
ZenML is used to manage and orchestrate the steps of the pipeline. Each step is defined using the @step decorator, and the entire pipeline is orchestrated using the @pipeline decorator.

## Conclusion
This pipeline allows for automated, real-time processing of stock data, leveraging ZenML for MLOps workflow automation. You can easily extend the pipeline by adding more steps or integrating additional data sources.
