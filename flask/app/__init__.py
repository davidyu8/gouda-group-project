from flask import Flask, g, render_template, request

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from .find_recipe import find_recipe
from .generators import generate_recipe_GRU

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main_better.html')

@app.route('/generator/', methods=['POST', 'GET'])
def generator():
    if request.method == 'GET':
        return render_template('generator.html')
    else:
        input_ingredient = request.form['ingredients']
        generated_recipe = generate_recipe_GRU(seed=input_ingredient, length=500, temperature=0.8).split('•')
        return render_template('generator.html', ingredient=input_ingredient,generated_recipe=generated_recipe)

@app.route('/recipe_finder/', methods=['POST', 'GET'])
def recipe_finder():
    if request.method == 'GET':
        return render_template('recipe_finder.html')
    else:
        
        input_ingredients = request.form['ingredients'].split(',')

        recipe = find_recipe(input_ingredients, 1)
        title = recipe['title'].iloc[0]
        recipe_ingredients = recipe['ingredients'].iloc[0][1:-1]
        ingredients_list = []
        for i in recipe_ingredients.split('",'):
            ingredients_list.append(i.replace('"',''))
        
        instructions = recipe['instructions'].iloc[0][1:-1]
        instructions_list = []
        for j in instructions.split('",'):
            instructions_list.append(j.replace('"',''))
        
        return render_template('recipe_finder.html', 
                                ingredients=input_ingredients, 
                                title=title, 
                                recipe_ingredients=ingredients_list, 
                                instructions=instructions_list)

# Sessions and logging in

app.secret_key = b'h\x13\xce`\xd9\xde\xbex\xbd\xc3\xcc\x07\x04\x08\x88~'


