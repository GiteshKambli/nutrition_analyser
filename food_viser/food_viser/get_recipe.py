import requests
from pprint import pprint
import os
import json
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

params = {
    # check https://developer.edamam.com/edamam-docs-recipe-api#/
    'type': 'public',
    'q': 'fish',
    'app_id': APP_ID,
    'app_key': APP_KEY,
    'ingr': '200',  # no. of ingredients 'MIN-MAX'
    # 'diet': '',
    'health': 'alcohol-free',
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


def search_recipe(calories, health, cuisineType, mealType, carbMax, fatMax, sugarMax, proMin, ing_no = 20, diet='balanced',
                  random=True, q="Vegetables"):

    params = {
        # check https://developer.edamam.com/edamam-docs-recipe-api#/
        'type': 'public',
        'q': q,
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'health': health,
        'diet': diet,
        'cuisineType': cuisineType,
        'mealType': mealType,
        'nutrients[CHOCDF.net]': carbMax,
        'nutrients[FAT]': fatMax,
        'nutrients[SUGAR]': sugarMax,
        'nutrients[PROCNT]': str(proMin) + "+",
        'calories': calories,
        'random': random,
        'ingr': ing_no
    }
    response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    recipes = {}

    for recipe in data['hits']:
        name = recipe['recipe']['label']
        recipes[name] = {}
        recipes[name]['image'] = recipe['recipe']['image']
        recipes[name]['url'] = recipe['recipe']['url']
        recipes[name]['yield'] = recipe['recipe']['yield']
        recipes[name]['ingredientLines'] = recipe['recipe']['ingredientLines']
        recipes[name]['calories'] = float(recipe['recipe']['calories'])/int(recipe['recipe']['yield'])
        recipes[name]['fats'] = float(recipe['recipe']['totalNutrients']['FAT']['quantity'])/int(recipe['recipe']['yield'])
        recipes[name]['carbs'] = float(recipe['recipe']['totalNutrients']['CHOCDF']['quantity'])/int(recipe['recipe']['yield'])
        recipes[name]['sugar'] = float(recipe['recipe']['totalNutrients']['SUGAR']['quantity'])/int(recipe['recipe']['yield'])
        recipes[name]['protein'] = float(recipe['recipe']['totalNutrients']['PROCNT']['quantity'])/int(recipe['recipe']['yield'])
        recipes[name]['url'] = recipe['recipe']['url']
        recipes[name]['shareAs'] = recipe['recipe']['totalNutrients']['PROCNT']['quantity']

    return recipes

def find_nearest(user_recipes, recipes):


if __name__ == "__main__":
    # response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
    # response.raise_for_status()
    # data = response.json()
    # print(len(data['hits']))
    # pprint(data['hits'])
    recipes = {}
    ab = search_recipe(calories = 2000, health = "alcohol-free", cuisineType= "American", mealType = "Breakfast", carbMax= 1000, fatMax = 1000, sugarMax= 1000, proMin = 20)
    pprint(ab)
    # for query in ['fried', 'fish', 'rice', 'salad']:
    #     params['q'] = query
    #     response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
    #     response.raise_for_status()
    #     data = response.json()
    #     print(len(data['hits']))
    #     pprint(data['hits'])

    #     for i in data['hits'][:5]:
    #         recipes[i['recipe']['label']] = {
    #             'image': i['recipe']['image'],
    #             'yield': i['recipe']['yield'],
    #             'calories': i['recipe']['calories'],
    #             'totalNutrients': i['recipe']['totalNutrients'],
    #             'digest': i['recipe']['digest'],
    #         }
    #     pprint(recipes)

    # with open(r"recipes2.json", 'r') as f:
    #     data = json.load(f)

    # data['recipes'].update(recipes)

    # with open(r"recipes2.json", 'w') as f:
    #     json.dump(data, f, indent=4)
