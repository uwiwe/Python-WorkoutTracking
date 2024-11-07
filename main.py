# Imports
import requests
from datetime import datetime
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Keys
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
USERNAME = os.getenv("USERNAME")
SHEETY_AUTHORIZATION = os.getenv("SHEETY_AUTHORIZATION")

NUTRITIONIX_URL = os.getenv("NUTRITIONIX_URL")
SHEETY_URL = os.getenv("SHEETY_URL")

GENDER = "male"
WEIGHT_KG = 68
HEIGHT_CM = 172
AGE = 18

# NUTRITIONIX API -----------------------------------------------------------------------------------------------------
# POST
# Necessary to authenticate the request
headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

# Input
exercises = input("Tell me which exercises you did:")

parameters = {
    "query": exercises,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(NUTRITIONIX_URL, headers=headers, data=json.dumps(parameters))

if response.status_code == 200:
    result = response.json()
else:
    print(f"Error: {response.status_code}")
    sys.exit("Exiting program")


# SHEETY API -----------------------------------------------------------------------------------------------------
#POST
exercise = result['exercises'][0]
now = datetime.now()

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            'date': now.strftime('%d/%m/%Y'),
            'time': now.strftime('%H:%M:%S'),
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories'],
        }
    }

response = requests.post(SHEETY_URL, headers={'Content-Type': 'application/json', "Authorization": SHEETY_AUTHORIZATION}, data=json.dumps(sheet_inputs))
if response.status_code == 200:
    json_response = response.json()
    print(json_response['workout'])
else:
    print(f"Error: {response.status_code}")

# # GET
# response = requests.get(SHEETY_URL)
# if response.status_code == 200:
#     json_response = response.json()
#     # Do something with the data
#     print(json_response['workouts'])
# else:
#     print(f"Error: {response.status_code}")