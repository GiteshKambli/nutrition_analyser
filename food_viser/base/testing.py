from get_recipe import search_recipe

recipes = search_recipe(calories = 2000,
                        health = 'alcohol-free',
                        cuisineType = 'American', 
                        mealType = 'Dinner',
                        carbMax = 1000,
                        fatMax = 1000,
                        sugarMax= 1000,
                        proMin = 20,
                        random = True,
                        q = "Chicken")

print(recipes)
print(len(recipes))