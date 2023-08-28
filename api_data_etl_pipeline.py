
import pandas as pd
import requests
from sqlalchemy import create_engine


# get api response data

def get_api_response_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print("Error: Unable to fetch data from the API")
        return []


api_url = "https://randomuser.me/api/?results=200" # 200 records

response_data = get_api_response_data(api_url)




# extracting user data

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

user_data = extract_user_data(response_data)



# creating dataframe

def create_dataframe(user_data):
    df = pd.DataFrame(user_data)
    return df

df = create_dataframe(user_data)



# Loading dataframe to database

def load_dataframe_to_postgresql(df, table_name, database_url):
    # Creating a connection to the PostgreSQL database
    engine = create_engine(database_url)

    # Load the DataFrame into the database
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
database_url = 'postgresql://username:password@host:port/database'
table_name = 'user_data'

load_dataframe_to_postgresql(df, table_name, database_url)



