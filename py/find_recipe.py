# Defines the recipe finder function, which queries the recipes1M.db database.

import pandas as pd
import sqlite3

def find_recipe(ingredients, filepath, min_score = 1):
    """
    Find recipes that have the minimum number of specified ingredients.

    Parameters:
        ingredients (list): list of ingredients to search for
        filepath: the location of the recipes1M database
        min_score (int): minimum number of ingredients that need to match
    
    Returns:
        df: a pandas DataFrame that contains all of the recipes satisfying the
        given requirements.
    """

    # ensure that the ingredients are passed as a list
    if type(ingredients) != list:
        raise TypeError("Ingredients must be contained in a list.")
     
    # create a variable to contain the WHERE statement for the SQL query
    where_statement = ""

    # Iterate accross the ingredients and add each one to the WHERE statement
    for i in ingredients:
        where_statement += f"R.ingredients LIKE '%{i}%' OR "
    
    # open up dataset, automatically close
    with sqlite3.connect(filepath) as conn:
        
        # grab ingredient matches
        query = \
        f"""
        SELECT R.title, R.ingredients, R.url
        FROM recipes R
        WHERE {where_statement[:-3]}
        """

         # query database
        df = pd.read_sql_query(query, conn)
        
    # reset the Score column every time the function is called
    df["Score"] = 0
    
    # iterate through list of input ingredients
    for ingr in ingredients: 
        # increment score by 1 every time the matching ingredient name is found in a recipe
        df["Score"] += df['ingredients'].apply(lambda x: ingr in x)
    
    # return matching recipes
    return df[df["Score"] >= min_score]