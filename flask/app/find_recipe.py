import pandas as pd
import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext

from flask import Blueprint, g, render_template, url_for, abort

def get_recipe_db():
	if 'recipes1M' not in g:
		g.recipes1M = sqlite3.connect(
			current_app.config['recipes1M'],
			detect_types=sqlite3.PARSE_DECLTYPES)
		g.recipes1M.row_factory = sqlite3.Row

	return g.recipes1M

def close_recipe_db(e=None):
    recipe_db = g.pop('recipes1M', None)

    if recipe_db is not None:
        recipe_db.close()

def find_recipe(ingredients, n = 5):
    """
    Derivation of find_recipe_2 function, but optimized for easier use with a UI. 
    Removed the min_score argument, recipes with most matches are automatically returned.
    Returns at most n recipes in a pandas dataframe contaning
    title, ingredients, instructions, and number of ingredient matches

    ingredients: list of ingredients available
    n: number of desired recipes to output. default set to 5
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
    with sqlite3.connect("../data/recipes1M.db") as conn:
        
        # grab ingredient matches
        query = \
        f"""
        SELECT R.title, R.ingredients, R.instructions
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
    
    for i in range(len(ingredients), 0, -1):

      if (df["Score"] >= i).any() == True:
        return (df[df["Score"] >= i]).sample(n = n)
    
    # if we get this far, there were no recipes found
    data = [["No matching recipes!", "", ""]]
    df = pd.DataFrame(data, columns = ["title", "ingredients", "instructions"])

    return df
