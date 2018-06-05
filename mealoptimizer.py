# Meal Optimizer
# Functions for meal planning and optimization

import numpy as np
import json



#------------------------------------------------------------------------------

macro_jf = open( 'macros.json', 'r' )
macro_dict = json.load( macro_jf )



#------------------------------------------------------------------------------

# Calorie targets

def get_macro_weight_targets( cal_amount, percentage_targets ):
    macro_ratio = np.array( percentage_targets ) # should add up to 100
    macro_ratio = macro_ratio / 100
    macro_cals = cal_amount * macro_ratio
    macro_grams = macro_cals / np.array([4,4,9])
    return macro_grams



#------------------------------------------------------------------------------

# Meal optimization using mse error minimization and constraints

def optimize_food_amounts( list_of_foods, pcf_grams_target, initial_food_amounts = 'random', n_iters = 400, alpha = 0.5, verbose = False ):
    
    # Arrange pcf values for all foods in a matrix
    foods_pcf_mat = np.array( [ [ ( macro_dict[food]['protein']      / macro_dict[food]['weight'] ),
                                  ( macro_dict[food]['carbohydrate'] / macro_dict[food]['weight'] ),
                                  ( macro_dict[food]['fat']          / macro_dict[food]['weight'] ) ] \
                              for food in list_of_foods ] )

    foods_pcf_mat = foods_pcf_mat.T
    
    pcf_target = pcf_grams_target
    
    # 'initial_food_amounts' if unused, is randomly initialized, or can be a vector of length equal to
    # number of items in food list
    if initial_food_amounts == 'random':
        wts = np.random.random( len( list_of_foods ) )
    else:
        wts = initial_food_amounts

    for n in range( n_iters ):
        # calculate cost function
        Y = np.dot( foods_pcf_mat, wts )
        YTdiff = Y - pcf_grams_target
        J = 0.5*np.sum( YTdiff ** 2 )

        if verbose:
        	print( "#{} : Cost: {}".format( n+1, J ) )

        # calculate gradient of J wrt wts
        dJdWts = np.dot( YTdiff.T, foods_pcf_mat )

        # Update weights
        wts -= alpha * dJdWts

        # constraints:
        # clip weights to zero and above
        wts = np.maximum( wts, np.zeros( len( list_of_foods ) ) )
    

    return wts



#------------------------------------------------------------------------------

# Meal analysis

def print_meal_analysis( food_list, food_amounts ):

    total_pcf_grams = np.zeros(3)
    total_pcf_cals = np.zeros(3)

    print( "Meal: " )

    for k in range( len( food_list ) ):
        print( '{0} : {1:0.2f} grams'.format( food_list[k], food_amounts[k] ) )

        item_pcf_grams = np.array( [ macro_dict[food_list[k]]['protein'],
                                     macro_dict[food_list[k]]['carbohydrate'],
                                     macro_dict[food_list[k]]['fat'] ] ) * food_amounts[k] / macro_dict[food_list[k]]['weight']

        total_pcf_grams += item_pcf_grams    
        item_pcf_cals = item_pcf_grams * np.array([4,4,9])
        total_pcf_cals += item_pcf_cals


    print( '\nMacronutrient analysis of meal: ' )
    print( '-' * 20 )
    print( 'Protein : {0:.2f} grams'.format( total_pcf_grams[0] ) )
    print( 'Carbohydrates : {0:.2f} grams'.format( total_pcf_grams[1] ) )
    print( 'Fat : {0:.2f} grams'.format( total_pcf_grams[2] ) )


    print( '\nMacronutrient analysis of meal ( in calorie percentages ): ' )
    print( '-' * 20 )
    print( 'Total pcf calories: {0:.2f} Cal'.format( np.sum( total_pcf_cals ) ) )
    print( 'Protein : {0:.2f}%'.format( total_pcf_cals[0] * 100 / np.sum( total_pcf_cals ) ) )
    print( 'Carbohydrates : {0:.2f}%'.format( total_pcf_cals[1] * 100 / np.sum( total_pcf_cals ) ) )
    print( 'Fat : {0:.2f}%'.format( total_pcf_cals[2] * 100 / np.sum( total_pcf_cals ) ) )



#------------------------------------------------------------------------------

# Print all foods in the database i.e. in the macros.json file

def print_foods_in_database():
	food_list_ordered = sorted( [ food for food in macro_dict.keys() ] )
	print( food_list_ordered )
