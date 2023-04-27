import requests
from pprint import pprint
from dotenv import load_dotenv
import os

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

params = {
    # check https://developer.edamam.com/edamam-docs-recipe-api#/
    # 'type': 'public',
    # 'q': 'chicken',
    # 'app_id': APP_ID,
    # 'app_key': APP_KEY,
    # 'ingr': '',  # no. of ingredients 'MIN-MAX'
    # 'diet': '',
    # 'health': '',
    # 'cuisineType': '',
    # 'mealType': '',
    # 'dishType': '',
    # 'calories': '',
    # 'time': '',
    # 'excluded': '',
    # 'calories': '',
    # 'nutrients[CHOCDF]': '',  # carbohydrates
    # 'nutrients[FAT]': '',
    # 'nutrients[SUGAR]': '',
    # 'nutrients[PROCNT]': '',
}

headers = {
    "Accept": "application/json"
}

response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
response.raise_for_status()
data = response.json()
print(len(data['hits']))
pprint(data['hits'])
