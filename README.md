# Introduction
In need of a new recipe? Have a few old pantry items that have be used up? Well, look no further, because the Gouda Group has the answer for you!

This repository allows you to (a) search for recipes that match a list of ingredients, and (b) generate new recipes to try (if you dare). You could be cooking up a storm in no time! And for the technically inclined, we have included a full guide on how to train your own recipe generation models from scratch.

## Repository Organization
We have several folders and files in this repository. The purpose of each one is explained below.
### Folders
1. Flask_Site: This folder contains the material needed to run the recipe website locally.
2. data: This folder will contain our main source of data, a collection of over 1 million recipes located [here](http://im2recipe.csail.mit.edu/dataset/login/). We say "will" because the data set is large and therefore not actually included in the repository. Instructions and code for preparing the data are in the Installation section.
3. py: This folder contains various code files needed for the project.
### Files
1. .gitignore: Text file containing filenames for GitHub Desktop to ignore.
2. README.md: You are here!
4. proposal.md: The project proposal we wrote at the beginning of the quarter.
6. `recipe_generator.ipynb`: Defines and trains RNNs to generate new recipes. If you want to make your own models, this is the place to do it!

# Installation
To use this repository, clone it to your machine and follow these instructions, which will walk you through the process of preparing the recipes1M.db database.

## Data Preparation
To obtain the data, visit the [pic2recipe](http://pic2recipe.csail.mit.edu/) website, and follow the instructions to download the dataset. This will involve creating an account. Next, go to the [download](http://im2recipe.csail.mit.edu/dataset/download/) page and download the data from the link labeled "Layers". The file should be about 400 MB in size, and will take a while to download!

Place this file in the top-level directory of your cloned repository and check that the following conditions hold.
1. The data file is named "recipe1M_layers.tar.gz" (this is the default name). 
2. There is a .gitignore text file in the repository that contains both "recipe1M_layers.tar.gz" and "recipes1M.db" in it. It is fine if there's other text as well.

It is important that both of these conditions are satisfied before proceeding! The recipes1M.db file is large (over 1 GB) and you do not want to attempt to push it to GitHub.

Next, open up a command line interface. Activate a Python environment and change the directory to the `py` folder. Then run the file `prepare_data.py` (by typing `python prepare_data.py`). This may take a few minutes. The file will periodically print updates on its progress. If you see "conversion successful!", then you are good to go!

## Location of recipes1M.db
To train new models (using `recipe_generator.ipynb`), recipes1M.db must be in the "data" folder. In order to run the website, recipes1M.db must be in the "Flask_Site" folder.

# Demo

## Website

## Recipe Finding

## Recipe Generating

# Conclusion
We really enjoyed designing and implementing this project. The recipe finder is useful because it can draw upon a huge reservoir to make recipe suggestions in response to detailed user requests. If you want to use up a specific set of ingredients that will expire soon, this function provides a way to quickly obtain only the recipes that satisfy that constraint.

The recipe generator was quite fun as well. It was really cool to see that our model could learn English and recipe-specific language with just a couple hours of training, and also simultaneously funny to see the clear culinary genius that it had learned as well.

# Credits
We want to give credit to the [Recipe1M team](http://im2recipe.csail.mit.edu/) at MIT for originally gathering the data that we used. We also want to credit [Oleksii Trekhleb](https://github.com/trekhleb) for the [post](https://www.kdnuggets.com/2020/07/generating-cooking-recipes-using-tensorflow.html) he wrote on the [KDNuggets](https://www.kdnuggets.com/) blog. This post provided a lot of helpful guidance to get the generation part of our project off the ground, particularly in `train.py` and `recipe_generator.ipynb`.







# Code Demonstration
Below we show examples of our two recipe tasks at work.

```python
import json
import pandas as pd
import sqlite3
import numpy as np
```

## Recipe Finder

The function below is our __recipe finder__ function. It allows a user to input a list of ingredients, and retrieve some relevant recipes with matching ingredients.


```python
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
    with sqlite3.connect("/content/drive/Shareddrives/Gouda Group Project/recipes1M.db") as conn:
        
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

    return "No matching recipes!"
```


```python
find_recipe(["potato", "asparagus"], n = 10)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>ingredients</th>
      <th>instructions</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>54315</th>
      <td>Herb Marinade Grilled Veggies</td>
      <td>["1/4 cup (60 ml) olive oil", "1/4 cup (60 ml)...</td>
      <td>["Put veggies in shallow dish and marinade 2 h...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>59018</th>
      <td>New Potatoes Avec</td>
      <td>["20 small new potatoes, scrubbed", "14 cup pa...</td>
      <td>["add potatoes to a large pot of rapidly boili...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>75656</th>
      <td>Napa Nouveau Pierogies</td>
      <td>["1 (16 ounce) box pierogies, I like potato &amp; ...</td>
      <td>["Cook pierogies according to package directio...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>70467</th>
      <td>Ham-Potato Bake</td>
      <td>["1 cup baked ham, cut in lg. pieces", "1 cup ...</td>
      <td>["Add all ingredients to a bake-proof dish.", ...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>33202</th>
      <td>Chicken Florentine with Spring Vegetable and D...</td>
      <td>["1 pound fresh spinach, soaked and washed wel...</td>
      <td>["For the Chicken:", "Preheat oven to 350 degr...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>70913</th>
      <td>Easy Creamy Crab and Asparagus Soup</td>
      <td>["2 slices bacon, diced small", "1/2 cup mince...</td>
      <td>["Cook and stir the bacon and onion in a sauce...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>71338</th>
      <td>Creamy Ham and Potato Soup</td>
      <td>["3 large red potatoes, diced", "1 onion, chop...</td>
      <td>["Combine potatoes, onion, turkey, ham, celery...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4791</th>
      <td>Andalusian Flamenco Eggs</td>
      <td>["2 -3 slices cooked ham", "12 lb sliced cooke...</td>
      <td>["Cut the ham into small pieces and fry in the...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15004</th>
      <td>Asparagus Potato and Watercress Soup</td>
      <td>["2 cups asparagus, trimmed,peeled if thick &amp; ...</td>
      <td>["Over medium heat, sweat the shallots and gar...</td>
      <td>2</td>
    </tr>
    <tr>
      <th>26260</th>
      <td>Spring Asparagus Soup</td>
      <td>["2 pounds asparagus", "1 shallot, sliced thin...</td>
      <td>["Cut off asparagus tips and put aside, cut of...</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



## Recipe Generation

In this section, we develop a __recipe generation__ function. It allows a user to input ingredients, and generate recipes using models trained on recurrent neural networks. At the moment, we're working with an __LSTM__ (long short-term memory) model, and a __GRU__ (Gated Recurrent Units) model.

```python
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers

# modeling
import pathlib # for setting up checkpoint directory
import os # ditto
```

### Auxiliary Code + Functions

The code below is used in prepping the `generate_recipe` function.


```python
def import_data(n):
  ''' imports the first n recipes from the recipe database. '''
  
  with sqlite3.connect("/content/drive/Shareddrives/Gouda Group Project/recipes1M.db") as conn:
    query = \
    f"""
    SELECT R.title, R.ingredients, R.instructions
    FROM recipes R
    LIMIT ?
    """

    df = pd.read_sql_query(query, conn, params = [n])
  
  return df
```


```python
DATA_SIZE = 100000
data_raw = import_data(DATA_SIZE)
```


```python
# Oleksii Trekhleb

# define relevant constant values
STOP_WORD_TITLE = '📗 '
STOP_WORD_INGREDIENTS = '\n🥕\n\n'
STOP_WORD_INSTRUCTIONS = '\n📝\n\n'
```


```python
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
```


```python
# condense each recipe into a single string
data_str = data_raw.apply(lambda x: condense(x.title, x.ingredients, x.instructions), axis = 1)
```


```python
# Oleksii Trekhleb
MAX_RECIPE_LENGTH = 2000

def filter(recipe):
  ''' removes recipes that are too long. '''
  return len(recipe) <= MAX_RECIPE_LENGTH 

data_filter = [recipe for recipe in data_str if filter(recipe)] 
```


```python
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

tokenizer.get_config() # show results
```




    {'char_level': True,
     'document_count': 94136,
     'filters': '',
     'index_docs': '{"1": 94135, "101": 1, "55": 26345, "51": 51101, "17": 94135, "21": 93421, "32": 76497, "10": 94111, "25": 89419, "34": 70465, "7": 94131, "14": 94029, "41": 62330, "47": 94135, "27": 90429, "48": 94135, "5": 94116, "4": 94133, "3": 94126, "26": 91327, "22": 92324, "15": 94095, "54": 39644, "2": 94135, "28": 90400, "38": 65029, "18": 93792, "11": 94079, "31": 78336, "35": 59588, "62": 32509, "13": 94120, "12": 94135, "30": 82207, "42": 64041, "9": 94130, "20": 93543, "16": 94034, "19": 93812, "23": 93354, "8": 94123, "44": 54366, "24": 92673, "33": 74283, "46": 52304, "49": 94135, "39": 64915, "29": 90369, "6": 94130, "36": 66005, "45": 41533, "58": 36437, "64": 21373, "61": 32407, "59": 31291, "70": 12369, "53": 43677, "43": 61155, "60": 26479, "52": 47844, "63": 30461, "40": 59826, "37": 70695, "73": 9668, "76": 8657, "65": 18289, "75": 10409, "56": 36455, "50": 48091, "66": 14933, "69": 15236, "84": 1147, "57": 33385, "71": 12941, "72": 12220, "81": 2567, "82": 1864, "91": 164, "74": 7646, "68": 17451, "78": 4850, "77": 5263, "67": 13607, "80": 3423, "79": 2847, "90": 231, "83": 1861, "92": 188, "85": 564, "87": 282, "86": 287, "88": 396, "89": 249, "94": 57, "95": 54, "93": 29, "96": 46, "97": 43, "99": 20, "98": 21, "100": 7}',
     'index_word': '{"1": " ", "2": "e", "3": "o", "4": "a", "5": "t", "6": "n", "7": "i", "8": "r", "9": "s", "10": "l", "11": "d", "12": "\\n", "13": "c", "14": "h", "15": "u", "16": "p", "17": "\\u2022", "18": "m", "19": "g", "20": "b", "21": ".", "22": "f", "23": "1", "24": "w", "25": ",", "26": "k", "27": "y", "28": "v", "29": "2", "30": "S", "31": "C", "32": "4", "33": "3", "34": "x", "35": "/", "36": "-", "37": "P", "38": ")", "39": "(", "40": "0", "41": "A", "42": "B", "43": "5", "44": "T", "45": "z", "46": "R", "47": "\\ud83d\\udcd7", "48": "\\ud83e\\udd55", "49": "\\ud83d\\udcdd", "50": "I", "51": "M", "52": "F", "53": "j", "54": "D", "55": ";", "56": "W", "57": "L", "58": "8", "59": "q", "60": "O", "61": "G", "62": "6", "63": "H", "64": "E", "65": "\'", "66": "N", "67": ":", "68": "7", "69": "9", "70": "K", "71": "U", "72": "V", "73": "!", "74": "&", "75": "Y", "76": "J", "77": "\\"", "78": "\\\\", "79": "*", "80": "Q", "81": "Z", "82": "$", "83": "%", "84": "X", "85": "#", "86": "]", "87": "[", "88": "?", "89": "~", "90": "+", "91": "=", "92": "@", "93": "_", "94": ">", "95": "`", "96": "{", "97": "}", "98": "<", "99": "^", "100": "|", "101": "\\u2423"}',
     'lower': False,
     'num_words': None,
     'oov_token': None,
     'split': '',
     'word_counts': '{"\\u2423": 1, "\\ud83d\\udcd7": 94135, " ": 13835352, "D": 60264, "i": 3908737, "l": 2963677, "y": 585357, "M": 87109, "a": 4697710, "c": 2344750, "r": 3759007, "o": 4773276, "n": 4157229, "S": 248856, "d": 2425854, "R": 97727, "e": 7189338, "p": 2121880, "\\n": 2378587, "\\ud83e\\udd55": 94135, "\\u2022": 1719642, "1": 767640, ".": 929099, "b": 1102426, "w": 763308, "m": 1416555, "u": 2132226, "A": 138349, "h": 2165337, "s": 3704124, "(": 162784, "4": 206332, ")": 163460, "/": 185739, "2": 440415, "g": 1339223, "3": 194217, "t": 4566001, "v": 552895, "\\ud83d\\udcdd": 94135, "C": 218344, "k": 741721, ";": 58270, ",": 762950, "B": 133385, "x": 188721, "T": 121236, "f": 889817, "6": 45478, "G": 48896, "z": 101606, "8": 53321, "q": 52876, "K": 17021, "E": 39480, "-": 177456, "O": 51814, "P": 168191, "F": 86792, "5": 129450, "0": 150306, "H": 42840, "j": 84558, "!": 13221, "\'": 26638, "W": 56996, "J": 11001, "Y": 12933, "I": 89948, "9": 20918, "N": 22465, "X": 1345, "L": 54997, "V": 16115, "U": 16594, "Z": 3017, "&": 13018, "$": 2512, "=": 299, "7": 21452, "\\\\": 9410, "\\"": 10269, ":": 22004, "Q": 4092, "*": 6118, "+": 309, "%": 2288, "@": 209, "#": 701, "[": 511, "]": 514, "?": 475, "~": 387, ">": 94, "`": 65, "_": 148, "{": 54, "}": 51, "^": 30, "<": 38, "|": 26}',
     'word_docs': '{"\\u2423": 1, ";": 26345, "M": 51101, "\\u2022": 94135, ".": 93421, "4": 76497, "l": 94111, ",": 89419, "x": 70465, "i": 94131, "h": 94029, "A": 62330, " ": 94135, "\\ud83d\\udcd7": 94135, "y": 90429, "\\ud83e\\udd55": 94135, "t": 94116, "a": 94133, "o": 94126, "k": 91327, "f": 92324, "u": 94095, "D": 39644, "e": 94135, "v": 90400, ")": 65029, "m": 93792, "d": 94079, "C": 78336, "/": 59588, "6": 32509, "c": 94120, "\\n": 94135, "S": 82207, "B": 64041, "s": 94130, "b": 93543, "p": 94034, "g": 93812, "1": 93354, "r": 94123, "T": 54366, "w": 92673, "3": 74283, "R": 52304, "\\ud83d\\udcdd": 94135, "(": 64915, "2": 90369, "n": 94130, "-": 66005, "z": 41533, "8": 36437, "E": 21373, "G": 32407, "q": 31291, "K": 12369, "j": 43677, "5": 61155, "O": 26479, "F": 47844, "H": 30461, "0": 59826, "P": 70695, "!": 9668, "J": 8657, "\'": 18289, "Y": 10409, "W": 36455, "I": 48091, "N": 14933, "9": 15236, "X": 1147, "L": 33385, "U": 12941, "V": 12220, "Z": 2567, "$": 1864, "=": 164, "&": 7646, "7": 17451, "\\\\": 4850, "\\"": 5263, ":": 13607, "Q": 3423, "*": 2847, "+": 231, "%": 1861, "@": 188, "#": 564, "[": 282, "]": 287, "?": 396, "~": 249, ">": 57, "`": 54, "_": 29, "{": 46, "}": 43, "^": 20, "<": 21, "|": 7}',
     'word_index': '{" ": 1, "e": 2, "o": 3, "a": 4, "t": 5, "n": 6, "i": 7, "r": 8, "s": 9, "l": 10, "d": 11, "\\n": 12, "c": 13, "h": 14, "u": 15, "p": 16, "\\u2022": 17, "m": 18, "g": 19, "b": 20, ".": 21, "f": 22, "1": 23, "w": 24, ",": 25, "k": 26, "y": 27, "v": 28, "2": 29, "S": 30, "C": 31, "4": 32, "3": 33, "x": 34, "/": 35, "-": 36, "P": 37, ")": 38, "(": 39, "0": 40, "A": 41, "B": 42, "5": 43, "T": 44, "z": 45, "R": 46, "\\ud83d\\udcd7": 47, "\\ud83e\\udd55": 48, "\\ud83d\\udcdd": 49, "I": 50, "M": 51, "F": 52, "j": 53, "D": 54, ";": 55, "W": 56, "L": 57, "8": 58, "q": 59, "O": 60, "G": 61, "6": 62, "H": 63, "E": 64, "\'": 65, "N": 66, ":": 67, "7": 68, "9": 69, "K": 70, "U": 71, "V": 72, "!": 73, "&": 74, "Y": 75, "J": 76, "\\"": 77, "\\\\": 78, "*": 79, "Q": 80, "Z": 81, "$": 82, "%": 83, "X": 84, "#": 85, "]": 86, "[": 87, "?": 88, "~": 89, "+": 90, "=": 91, "@": 92, "_": 93, ">": 94, "`": 95, "{": 96, "}": 97, "<": 98, "^": 99, "|": 100, "\\u2423": 101}'}




```python
# Oleksii Trekhleb

VOCABULARY_SIZE = len(tokenizer.word_counts) + 1 # record for later
data_vec = tokenizer.texts_to_sequences(data_filter) # vectorize the data
```

The following cell sets up the models for text generation. The original models (which are set up for training) are shown in `recipe_generator.ipynb`. The blog post referenced above uses an LSTM model, which we modified slightly and used as our baseline model. We then designed a second model using a GRU layer instead, because we weren't able to train our model for a long period of time, and we wanted to obtain sensible results more quickly.

```python
# create generator using LSTM model
generator_LSTM = tf.keras.models.Sequential([
  layers.Embedding(input_dim = VOCABULARY_SIZE,
                  output_dim = 256,
                  batch_input_shape = [1, None]), # for generation, we use a batch size of 1. Our training code uses a batch size of 64.
  layers.LSTM(units = 1024,
              return_sequences = True, # keep the sequence length dimension
              stateful = True, # remember the old state of the model from batch to batch
              recurrent_initializer = tf.keras.initializers.GlorotNormal()),
  layers.Dense(VOCABULARY_SIZE)         
])

generator_LSTM.load_weights("/content/drive/Shareddrives/Gouda Group Project/recipe_model/baseline/checkpoint_4").expect_partial()
generator_LSTM.build(tf.TensorShape([1, None]))

# create generator using GRU model
generator_GRU = tf.keras.models.Sequential([
  layers.Embedding(input_dim = VOCABULARY_SIZE,
                  output_dim = 512,
                  batch_input_shape = [1, None]),
  layers.GRU(units = 1024,
              return_sequences = True,
              stateful = True),
  layers.Dense(VOCABULARY_SIZE)         
])

generator_GRU.load_weights("/content/drive/Shareddrives/Gouda Group Project/recipe_model/gru1/checkpoint_4").expect_partial()
generator_GRU.build(tf.TensorShape([1, None]))
```

### Main Function

Below is the main `generate_recipe` function.


```python
def generate_recipe(n, model, seed, length, temperature):
    """
    Function that generates recipes based on an RNN model.
    RNN Model can easily be swapped, so further testing on optimizing a model can be done.

    n: Number of recipes to be generated.
    model: String of model name to use. Currently, "LSTM" and "GRU" are only valid model types. More can be added later.
    seed: Ingredient name/seed to generate recipe with.
    length: Length in characters of output recipe.
    temperature: Temperature to be used when generating new recipe.
    """

    # load appropriate generator, more models can be added here later if developed
    if model == "LSTM":
        generator = generator_LSTM
        
    elif model == "GRU":
        generator = generator_GRU
    
    else:
        raise ValueError("Please input a valid model!")

    # initialize empty list of recipes
    recipes = []

    # iterate n times to generate n recipes
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

        # print recipe
        print("----- RECIPE " + str(i + 1) + " -----")
        print("SEED: ", seed, ", TEMPERATURE: ", temperature)
        print(recipes[len(recipes) - 1])
```


```python
# GRU model, kinda smart
generate_recipe(n = 5, model = "GRU", seed = "salmon", length = 500, temperature = 0.8)
```

    ----- RECIPE 1 -----
    SEED:  salmon , TEMPERATURE:  0.8
    📗 salmon with a red pepper flakes, gently add to the pot and cover with pita bread and sliced tomatoes with the lemon zest and, for topping and chop stems and top with the lemon zest, soup
    • Salt and freshly ground black pepper to taste, and toss well.
    • Serve shrimp with some papred by adding oil (for frying).
    • Makes Reslette.
    • When you have to work in an even bowl.
    • Spray a triangle of the fried onions to a plate to cool completely begin to spread out the steaks with mayonnaise.
    • Don't leave with 
    ----- RECIPE 2 -----
    SEED:  salmon , TEMPERATURE:  0.8
    📗 salmon and cover with aluminum foil or wax paper formon through green cabbage leaves.
    • May be freezery, add a few dinnex from the baking sheet and dash of the nuts and bake the top should be done removed.
    • 3.77 (Patteet) in a saucepan over medium heat, strain the mushrooms on top of the steak and cheese, onion and garlic for the flour to make it all accumulated by hands and meat for two minutes at the ends are boiling it forming around the edges.
    • Place the bones and half of the stem through the mo
    ----- RECIPE 3 -----
    SEED:  salmon , TEMPERATURE:  0.8
    📗 salmon for leaves and cooking to ready to use, place onion on the bottom of the pan.
    • Cook 1-1/4 cups chopped over high heat until al dente, about 2 minutes.
    • Turn off the heat, add the soy sauce, water, salt, and pepper.
    • Add the dry ingredients to the vegetable oil spray and squeeze out and stir into pan for a few minutes.
    • Add the boneless (you may need to stif).
    • Press the top of the bowl of solids with water, tossing them in a lit to marinate for at least 1 hour.
    • Drain the leaves, about 1/
    ----- RECIPE 4 -----
    SEED:  salmon , TEMPERATURE:  0.8
    📗 salmon and cooked to your bread is best puddings dont work evenly.
    • ).
    • Place the bread in the flour, almond bark to pan, salt and pepper to taste.
    • Cook until the bacon is melted and is thick and bubbly and the bottom has cooked through and set.
    • Remove the leeks, under a meat off for 15 minutes and serve with salved tomatoes until you pull them to top and soup with more the mushrooms and flavor.
    ␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣
    ----- RECIPE 5 -----
    SEED:  salmon , TEMPERATURE:  0.8
    📗 salmon if it.
    • Serve in a pinch, add in the olive oil and suger or more about 1 tablespoon of the olive oil and the seafood, smell straight to turn a soup bowls and serve over them with shredded capers, cut off each cake flour, and to finish off the seeds.
    • Reserve, 1 tablespoon of water to the real water.
    • * serve: Remove The bars, Reperare and spinach if desired.
    ␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣
    


```python
# LSTM model, not as smart
generate_recipe(n = 5, model = "LSTM", seed = "lemon", length = 500, temperature = 0.4)
```

    ----- RECIPE 1 -----
    SEED:  lemon , TEMPERATURE:  0.4
    📗 lemon📝•📝o🥕oning large bowl with the chicken stock and stir to make a light brown sugar and salt to the boiling water and stir until the center is melted and they are lettuce.
    • Add the soup and brown sugar.
    • Add the chicken stock, sugar, cornstarch, and salt, and stir to coat.
    • Reduce heat to low and simmer for 25 minutes.
    • Stir in the remaining ingredients and stir to cook over medium heat and cook until stiff the consistency to serve.
    ␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣␣
    ----- RECIPE 2 -----
    SEED:  lemon , TEMPERATURE:  0.4
    📗 lemon📝🥕oth colive with a medium non-stick skillet and then to a simmer for 5 minutes or until softened.
    • Transfer to a boil and stir until the carefly mixture and the center comes out clean is tender.
    • Cook the low for 1 hour or until the center of the center beans are tender.
    • Fold in the batter and stir until melted and cooked through.
    • Turn the chicken in a bowl and stir the mixture in the sauce mixture and stir to melte.
    • Add the garlic, minced garlic, salt, and pepper.
    • Add the potatoes, a
    ----- RECIPE 3 -----
    SEED:  lemon , TEMPERATURE:  0.4
    📗 lemon📝📝e• tiningllants with salt and pepper.
    • Add the remaining with the salt and salt and pepper.
    • Add the salt and pepper flakes.
    • Stir in the flour, salt and pepper to taste.
    • Stir in the chopped onions, sugar, and salt and pepper to taste.
    • Stir in the flour, and stir to combine.
    • Place the mixture into the pan and set aside.
    • Stir the stock and cook until the chili powder, about 4 minutes.
    • Add the chicken stock and stir until the cooking shallots and stir in the mixture and cook the sti
    ----- RECIPE 4 -----
    SEED:  lemon , TEMPERATURE:  0.4
    📗 lemon📝📝e• oninglestess sprinkle with salt and pepper.
    • Bring to a boil and stir in the butter and place in a large skillet over medium heat.
    • Add the pork chops, and season with salt and pepper.
    • Stir in the butter.
    • Pour into a large bowl and stir in the sauce and the salt and pepper to taste.
    • Add the remaining chilies and cook until the soft and brown and the center and cook until smooth.
    • Add the tomatoes, and serve the salt and pepper.
    • Cook over medium heat and stir in the sugar and the 
    ----- RECIPE 5 -----
    SEED:  lemon , TEMPERATURE:  0.4
    📗 lemon📝📝
    📝
    📝 oning and broth in a large skillet over medium heat.
    • Add the lemon juice, cinnamon, thinly sliced and salt.
    • Stir in sauce and salt and pepper to taste.
    • Sprinkle with salt and pepper.
    • Set aside.
    • Bake at 350 for about 15 minutes.
    • Add the chicken broth and lemon juice in a small bowl with the salt and pepper to taste.
    • Cover and stir for 3 minutes.
    • Add the oil in a small bowl and add the tomatoes, and cut into small mixing bowl.
    • Add the remaining mixture over the meat and st
