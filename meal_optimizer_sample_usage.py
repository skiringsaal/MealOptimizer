# Sample usage of meal_planning script

import meal_planning as mp

mp.print_foods_in_database()

# Make a list of things you want in a meal
food_list = [ 'whole milk','almonds','banana','apple' ]

# Set your target macro ratios ( in percentages )
protein_carb_fat_ratio_percentages = [ 30, 50, 20 ] # must add to 100%

# Set Calorie target
calorie_target = 300 # Cals

# Get protein, carbohydrate and fat amounts in grams for the set calorie target
protein_carb_fat_amounts_gram = mp.get_macro_weight_targets( calorie_target, protein_carb_fat_ratio_percentages )

# Find best combination of the food amounts so that you are as close as possible your target protein, carbohydrate and fat amounts
food_amounts_gram = mp.optimize_food_amounts( food_list, protein_carb_fat_amounts_gram )

# See the actual macro ratio
mp.print_meal_analysis( food_list, food_amounts_gram )