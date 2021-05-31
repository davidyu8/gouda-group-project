# -*- coding: utf-8 -*-
"""
This program uses a variety of models to generate original recipe text.

The code is organized as follows. The first section loads in the data and sets it up as a TensorFlow Dataset. The second section defines and trains the models (each model is given a subsection). The third and final section covers recipe generation.

While most of the code in this file is our own, some of it was derived from the code written in this blog post (located at https://www.kdnuggets.com/2020/07/generating-cooking-recipes-using-tensorflow.html), from author Oleksii Trekhleb (https://github.com/trekhleb). Some of the overall structure of our program also follows the plan laid down in that post. Cells which use his code are clearly marked with a comment reading
# Oleksii Trekhleb at the top.

# Section 1: Data Preparation

We connect the program to Google Drive, where the data and models are to be stored. Then we extract the data and prepare it for modeling, finishing by converting it into a TensorFlow Dataset.
"""

# import packages
import numpy as np # general
import pandas as pd # general
import sqlite3 # connect to database .db files
import tensorflow as tf # modeling

# define constants
STOP_WORD_TITLE = '📗 ' # for data processing
STOP_WORD_INGREDIENTS = '\n🥕\n\n' # for data processing
STOP_WORD_INSTRUCTIONS = '\n📝\n\n' # for data processing
MAX_RECIPE_LENGTH = 2000 # for data processing
STOP_SIGN = '␣' # for data processing
BATCH_SIZE = 64 # for model training
SHUFFLE_BUFFER_SIZE = 1000 # for model training

def import_data(n):
  ''' imports the first n recipes from the recipe database. '''
  
  with sqlite3.connect("data/recipes1M.db") as conn:
    query = \
    f"""
    SELECT R.title, R.ingredients, R.instructions
    FROM recipes R
    LIMIT ?
    """

    df = pd.read_sql_query(query, conn, params = [n])
  
  return df

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


def filter(recipe):
  ''' removes recipes that are too long. '''
  return len(recipe) <= MAX_RECIPE_LENGTH 

def split_input_target(recipe):
  ''' separate each string by removing one of the end characters, for model prediction later. '''
  input_text = recipe[:-1]
  target_text = recipe[1:]
    
  return input_text, target_text

def generate(model, seed, length, temperature, tokenizer):
  ''' generates text of length length, using the provided seed text and model. '''
  start = STOP_WORD_TITLE + seed
  indices = np.array(tokenizer.texts_to_sequences([start])) # vectorize
  result = []

  model.reset_states() # make separate predictions independent
  for char in range(length): # predict next character
    preds = model(indices)
    preds = tf.squeeze(preds, 0) # reduce a dimension
    preds = preds / temperature

    # pick next character
    pred_id = tf.random.categorical(preds, num_samples = 1)[-1, 0].numpy()
    
    # add the predicted character
    indices = tf.expand_dims([pred_id], 0)
    next_char = tokenizer.sequences_to_texts(indices.numpy())[0]
    result.append(next_char)

  return (start + ''.join(result))