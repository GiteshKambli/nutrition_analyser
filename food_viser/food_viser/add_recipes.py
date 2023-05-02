import ast
from pprint import pprint

from get_recipe import search_recipe

if __name__ == '__main__':
    recipe_dict = dict([(0, 'Crispy Fried Onions and Nori Topping Recipe'), (1, 'Fried Noodles'), (2, 'Fried Halloumi Cheese'), (3, 'Fried Onion And Jalapeno Bison Burger Recipe'), (4, 'Southern-fried chicken tacos'), (5, 'Deep Fried Fish Bones'), (6, 'Burnt-Scallion Fish'), (7, 'Curry-Crusted Fish'), (8, 'Fish in Coconut Sauce'), (9, 'Homemade fish fingers'), (10, 'Essentials: Rice'), (11, 'Rice Cereal Bars'), (12, 'Rice-Milk Rice Pudding'), (13, 'Cooked Basmati Rice'), (14, 'Rainbow rice'), (15, 'Steak & Chips Salad'), (16, 'Zuni-Inspired Grilled Chicken Salad'), (17, 'Shrimp Salad'), (18, 'Buffalo Chicken Salad')])
    pprint(recipe_dict)
    # weight = 86
    # height = 180
    # gender = 'male'
    # age = 20
    # activity_level = 'high'
    # goal = 'gain'
    # bmi = weight / (height/100)**2
    #
    # if gender == 'male':
    #     bmr = 10 * weight + 6.25 * height - 5 * age + 5
    #     body_fat = 1.20 * bmi + 0.23 * age - 16.2
    # else:
    #     bmr = 10 * weight + 6.25 * height - 5 * age - 161
    #     body_fat = 1.20 * bmi + 0.23 * age - 5.4
    #
    # activity_factor = 1
    #
    # if activity_level.lower() == 'sedentary':
    #     activity_factor = 0.8
    # elif activity_level.lower() == 'light':
    #     activity_factor = 1
    # elif activity_level.lower() == 'moderate':
    #     activity_factor = 1.2
    # elif activity_level.lower() == 'high':
    #     activity_factor = 1.4
    #
    # calorie_intake = round(bmr * activity_factor)
    #
    # if goal.lower() == 'lose':
    #     calorie_intake -= 300
    # if goal.lower() == 'gain':
    #     calorie_intake += 300
    #
    # cal_per_dish = calorie_intake / 3
    #
    # print(f'calorie per serve = {cal_per_dish}')
    #
    # cal_per_dish = calorie_intake / 3
    # carb_max = cal_per_dish / 8
    # min_pro = weight * 2.2 * 0.8 / 4
    # fat_max = cal_per_dish * 0.25 / 9
    # sug_max = cal_per_dish / 40
    #
    # print(f'calorie per serve = {cal_per_dish}')
    #
    # recipes = search_recipe(
    #     calories=cal_per_dish,
    #     health='dairy-free',
    #     cuisineType='American',
    #     mealType='dinner',
    #     carbMax=carb_max,
    #     fatMax=fat_max,
    #     sugarMax=sug_max,
    #     proMin=min_pro,
    #     diet='high-protein',
    #     q='chicken'
    # )
    # pprint(recipes)
