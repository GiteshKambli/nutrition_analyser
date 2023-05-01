import requests
from pprint import pprint
import os
import json

APP_ID = '7d528a91'
APP_KEY = 'ecd4505d32fdf524446f15cd21aaca0f'

params = {
    # check https://developer.edamam.com/edamam-docs-recipe-api#/
    'type': 'public',
    'q' : 'fish',
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

def search_recipe(calories, health, cuisineType, mealType,carbMax, fatMax, sugarMax, proMin, random = True,q = "Vegetables"):
    params = {
    # check https://developer.edamam.com/edamam-docs-recipe-api#/
    'type': 'public',
    'q': q,
    'app_id': APP_ID,
    'app_key': APP_KEY,
    'health': health,
    'cuisineType': cuisineType,
    'mealType': mealType,
    'nutrients[CHOCDF.net]': carbMax,
    'nutrients[FAT]': fatMax,
    'nutrients[SUGAR]': sugarMax,
    'nutrients[PROCNT]': str(proMin) + "+",
    'calories': calories,
    'random': random,
    }
    response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    return data['hits']
    

if __name__ == "__main__":
    # response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
    # response.raise_for_status()
    # data = response.json()
    # print(len(data['hits']))
    # pprint(data['hits'])
    recipes = {}
    
    for query in ['fried','fish','rice','salad']:
        params['q'] = query
        response = requests.get(url='https://api.edamam.com/api/recipes/v2', params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        print(len(data['hits']))
        pprint(data['hits'])
        

        
        for i in data['hits'][:5]:
            recipes[i['recipe']['label']] = {
                'image': i['recipe']['image'],
                'yield': i['recipe']['yield'],
                'calories': i['recipe']['calories'],
                'totalNutrients': i['recipe']['totalNutrients'],
                'digest': i['recipe']['digest'],
            }
        pprint(recipes)
        
    with open(r"D:\Github Repository\nutrition_analyser\food_viser\base\recipes.json",'r') as f:
        data = json.load(f)
    
    data['recipes'].update(recipes)
    
    with open(r"D:\Github Repository\nutrition_analyser\food_viser\base\recipes.json",'w') as f:
        json.dump(data,f,indent = 4)

    
