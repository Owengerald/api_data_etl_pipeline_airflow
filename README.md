# api_data_etl_pipeline_airflow

```markdown
# User Data Processing DAG

This repository contains a data pipeline implemented as a Directed Acyclic Graph (DAG) using Apache Airflow. The pipeline fetches user data from a random user API, transforms it, and loads it into a PostgreSQL database using Docker containers.

## Table of Contents
- ## Introduction
- ## Dependencies
- ## Setup-instructions
- ## Dag-overview
- ## Usage
- ## Contributing
- ## License

## Introduction

This data pipeline uses Apache Airflow to automate the process of fetching user data from an API, transforming the data, and loading it into a PostgreSQL database. The pipeline consists of tasks that handle data extraction, transformation, and loading.

## Dependencies

To run this data pipeline, you'll need the following dependencies:

- Python 3.x
- Apache Airflow
- pandas
- SQLAlchemy
- requests
- Docker

## Setup Instructions

1. Clone this repository to your local machine.
2. Install the required Python dependencies using `pip install -r requirements.txt`.
3. Set up Apache Airflow on your local machine. You can follow the official [Airflow Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation.html).
4. Configure the PostgreSQL database connection details in the DAG script (user_data_dag.py) by replacing the placeholders with your actual database information.
5. Start Apache Airflow's web server and scheduler using the command `airflow webserver -p 8080` and `airflow scheduler`.
6. Access the Airflow web interface at `http://localhost:8080` and enable the `user_data_processing` DAG.
7. The DAG will run daily and automatically fetch, transform, and load user data into the PostgreSQL database.

## DAG Overview

The DAG consists of the following tasks:

1. `extract_data_from_api`: Fetches user data from the API using the `get_api_response_data` function.
2. `transform_data_1`: Transforms the raw API data using the `extract_user_data` function.
3. `transform_data_2`: Creates a JSON representation of the extracted data using the `create_dataframe` function.
4. `load_data_into_postgresql_db`: Loads the JSON data into the PostgreSQL database using the `load_dataframe_to_postgresql` function.

## Usage

1. Follow the setup instructions to configure the environment and start the Apache Airflow web server and scheduler.
2. Access the Airflow web interface and monitor the progress of the DAG.
3. The DAG will run daily according to the specified schedule and automate the data processing tasks.

## Contributing

Contributions are welcome! Feel free to fork this repository, make improvements, and create a pull request.

## License

This project is All Rights Reserved. You may not use, distribute, or reproduce any part of the code or content without explicit permission from the project owner.

```
