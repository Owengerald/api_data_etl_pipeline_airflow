from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from prompt_toolkit import output

import pandas as pd
from sqlalchemy import create_engine
import requests

# DECLARING VARIABLES
api_url = "https://randomuser.me/api/?results=200" # 200 records


# DEFINING FUNCTIONS

# extracting raw API data
def get_api_response_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Error: Unable to fetch data from the API")
        return []
    


# Transforming data 1
def extract_user_data(user_instances):
    extracted_data = []
    for user in user_instances:
        user_data = {
            "First Name": user["name"]["first"],
            "Last Name": user["name"]["last"],
            "Gender": user["gender"],
            "Email": user["email"],
            "Date of Birth": user["dob"]["date"][:10],  # Extract YYYY-MM-DD from full date
            "Country": user["location"]["country"],
            "Street Address": user["location"]["street"]["name"],
            "City": user["location"]["city"],
            "State": user["location"]["state"],
            "Postcode": user["location"]["postcode"],
            "Phone": user["phone"],
            "Cell": user["cell"]
        }
        extracted_data.append(user_data)
    return extracted_data



# Transforming data 2
def create_dataframe(extracted_data):
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(extracted_data, dtype=object)
    return df.to_json(orient='records')





# Loading data to database
def load_dataframe_to_postgresql(df):
    # Create a connection to the PostgreSQL database
    database_url = "postgresql://username:password@host:port/database"
    engine = create_engine(database_url)
    table_name = "user_data"
    df_json = pd.read_json(df)

    # Load the DataFrame into the database
    df_json.to_sql(table_name, con=engine, if_exists='append', index=False)



# Defining default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


# Creating DAG instance
with DAG(
    'user_data_processing_v4',
    default_args=default_args,
    schedule_interval='@daily',  # Run daily
    start_date=datetime(2023, 8, 1, 0, 0),  # Start from August 1, 2023, at midnight
    catchup=False
) as dag:
# Defininng tasks

    task1 = PythonOperator(
        task_id = "extract_data_from_api",
        python_callable = get_api_response_data,
        op_args = [api_url],
    )

    task2 = PythonOperator(
        task_id = "transform_data_1",
        python_callable = extract_user_data,
        op_args = [task1.output],
    )


    task3 = PythonOperator(
        task_id = "transform_data_2",
        python_callable = create_dataframe,
        op_args = [task2.output],
    )


    task4 = PythonOperator(
        task_id = "load_data_into_postgresql_db",
        python_callable = load_dataframe_to_postgresql,
        op_args = [task3.output],
    )


    # set task dependencies
    task1 >> task2 >> task3 >> task4
