import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers

# modeling
import pathlib # for setting up checkpoint directory
import os # ditto

import sqlite3
import pandas as pd
import numpy as np


def import_data(n):
	''' imports the first n recipes from the recipe database. '''

	with sqlite3.connect("recipes1M.db") as conn:
		query = \
		f"""
		SELECT R.title, R.ingredients, R.instructions
		FROM recipes R
		LIMIT ?
		"""
	
	df = pd.read_sql_query(query, conn, params = [n])
  
	return df

DATA_SIZE = 100000
data_raw = import_data(DATA_SIZE)


# define relevant constant values
STOP_WORD_TITLE = '📗 '
STOP_WORD_INGREDIENTS = '\n🥕\n\n'
STOP_WORD_INSTRUCTIONS = '\n📝\n\n'

def condense(title, ingr, instr):
	''' 
	Each recipe is stored across three columns in the original data. This
	function condenses them into a single string, with marked boundaries.
	The concatenation steps in the end of this function were adapted from the code
	source discussed.
	'''

	# set up the ingredients
	temp1 = ingr # get string
	temp1 = temp1[1:-1] # remove outer quotations
	temp1 = temp1.split("\", ") # split into a list according to ",  sequence of those three characters
	temp1 = [item[1:] for item in temp1] # remove leading quotation
	temp1[len(temp1) - 1] = temp1[len(temp1) - 1][:-1] # remove ending quotation on last piece

	# set up the instructions
	temp2 = instr
	temp2 = temp2[1:-1]
	temp2 = temp2.split("\", ")
	temp2 = [item[1:] for item in temp2]
	temp2[len(temp2) - 1] = temp2[len(temp2) - 1][:-1]
    
	ingr_string = ''
	for ingredient in temp1:
		ingr_string += f'• {ingredient}\n'

	instr_string = ''
	for instruction in temp2:
		instr_string += f'• {instruction}\n'

	return f'{STOP_WORD_TITLE}{title}\n{STOP_WORD_INGREDIENTS}{ingr_string}{STOP_WORD_INSTRUCTIONS}{instr_string}'


# condense each recipe into a single string
data_str = data_raw.apply(lambda x: condense(x.title, x.ingredients, x.instructions), axis = 1)

# Oleksii Trekhleb
MAX_RECIPE_LENGTH = 2000

def filter(recipe):
  ''' removes recipes that are too long. '''
  return len(recipe) <= MAX_RECIPE_LENGTH 

data_filter = [recipe for recipe in data_str if filter(recipe)] 


# Oleksii Trekhleb (adapted)

STOP_SIGN = '␣' # will be appended to the end of each recipe

tokenizer = tf.keras.preprocessing.text.Tokenizer(
    filters = '', # we do not want to filter our recipes
    lower = False, # we want the model to recognize uppercase characters
    split = '', # we are using characters, not words
    char_level = True # we want a character-level RNN
)

# show the tokenizer all of the existing characters we have
tokenizer.fit_on_texts([STOP_SIGN])
tokenizer.fit_on_texts(data_filter)


def generate_recipe_GRU(n, seed, length, temperature):
	"""
	Function that generates recipes based on an RNN model.
	RNN Model can easily be swapped, so further testing on optimizing a model can be done.
	
	n: Number of recipes to be generated.
	seed: Ingredient name/seed to generate recipe with.
	length: Length in characters of output recipe.
	temperature: Temperature to be used when generating new recipe.
	"""
	

	# load appropriate generator, more models can be added here later if developed
	generator = tf.keras.models.load_model('generator_GRU')

	# # initialize empty list of recipes
	recipes = []

	# # iterate n times to generate n recipes
	for i in range(n):
		

		start = STOP_WORD_TITLE + seed
		indices = np.array(tokenizer.texts_to_sequences([start])) # vectorize
		result = []

		generator.reset_states() # make separate predictions independent

		for char in range(length): # predict next character
			preds = generator(indices)
			preds = tf.squeeze(preds, 0) # reduce a dimension
			preds = preds / temperature

			# pick next character
			pred_id = tf.random.categorical(preds, num_samples = 1)[-1, 0].numpy()
	                
			# add the predicted character
			indices = tf.expand_dims([pred_id], 0)
			next_char = tokenizer.sequences_to_texts(indices.numpy())[0]
			result.append(next_char)

			recipes.append(start + ''.join(result))
			# recipe = start + ''.join(result)

			# print recipe
			# string = "SEED: " + str(seed) +  ", TEMPERATURE: " + str(temperature) + '\n'
			string = str(recipes[len(recipes) - 1]).replace('␣', '')


			# final = "----- RECIPE -----" + '\n'
			# final += "SEED: " + str(seed) + ", TEMPERATURE: " + str(temperature) + '\n'
			# final += recipe

		return string










