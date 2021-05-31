from flask import Flask, g, render_template, request

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from .housewares import housewares_bp, close_hw_db
from .auth import auth_bp, close_auth_db, init_auth_db_command
from .find_recipe import find_recipe
from .generators import generate_recipe_GRU


# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page (fancy)

@app.route('/')
def main():
    return render_template('main_better.html')

# Show url matching

@app.route('/hello/')
def hello():
    return render_template('hello.html')

@app.route('/hello/<name>/')
def hello_name(name):
    return render_template('hello.html', name=name)

# Page with form

@app.route('/ask/', methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        return render_template('ask.html')
    else:
        try:
            return render_template('ask.html', name=request.form['name']) #, student=request.form['student'])
        except:
            return render_template('ask.html')

# File uploads and interfacing with complex Python

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            image = request.files['image']
            img = plt.imread(image)
            if img.shape != (28, 28, 3):
                raise Exception('invalid size')

            img = (img[:,:,0] + img[:,:,1] + img[:,:,2])/3
            img = 255*img/np.max(img)
            img = 255 - img

            img = img.reshape((1, 28, 28))
            model = tf.keras.models.load_model('mnist_model')

            d = np.argmax(model.predict(img))

            return render_template('submit.html', digit=d)
        except:
            return render_template('submit.html', error=True)

@app.route('/generator/', methods=['POST', 'GET'])
def generator():
    if request.method == 'GET':
        return render_template('generator.html')
    else:
        input_ingredient = request.form['ingredients']
        #input_temp = request.form['temperature']
        generated_recipe = generate_recipe_GRU(1, seed=input_ingredient, length=500, temperature=0.8).split('•')
        return render_template('generator.html', ingredient=input_ingredient,generated_recipe=generated_recipe)

@app.route('/recipe_finder/', methods=['POST', 'GET'])
def recipe_finder():
    if request.method == 'GET':
        return render_template('recipe_finder.html')
    else:
        
        input_ingredients = request.form['ingredients'].split(',')
        title = find_recipe(input_ingredients, 1)['title'].iloc[0]
        
        recipe_ingredients = find_recipe(input_ingredients, 1)['ingredients'].iloc[0][1:-1]
        ingredients_list = []
        for i in recipe_ingredients.split('",'):
            ingredients_list.append(i.replace('"',''))
        
        instructions = find_recipe(input_ingredients, 1)['instructions'].iloc[0][1:-1]
        instructions_list = []
        for j in instructions.split('",'):
            instructions_list.append(j.replace('"',''))
        
        return render_template('recipe_finder.html', 
                                ingredients=input_ingredients, 
                                title=title, 
                                recipe_ingredients=ingredients_list, 
                                instructions=instructions_list)

# Blueprints and interfacing with SQLite

app.register_blueprint(housewares_bp)
app.teardown_appcontext(close_hw_db)

# Sessions and logging in

app.secret_key = b'h\x13\xce`\xd9\xde\xbex\xbd\xc3\xcc\x07\x04\x08\x88~'

app.register_blueprint(auth_bp)
app.teardown_appcontext(close_auth_db)
app.cli.add_command(init_auth_db_command) # run with flask init-auth-db

