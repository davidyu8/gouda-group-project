import tensorflow as tf
import numpy as np
import pickle

# define relevant constant values
STOP_WORD_TITLE = '📗 '
STOP_WORD_INGREDIENTS = '\n🥕\n\n'
STOP_WORD_INSTRUCTIONS = '\n📝\n\n'
MAX_RECIPE_LENGTH = 2000
STOP_SIGN = '␣'

with open('app/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def generate_recipe_GRU(seed, length, temperature):
	"""
	Function that generates recipes based on an RNN model.
	
	seed: Ingredient name/seed to generate recipe with.
	length: Length in characters of output recipe.
	temperature: Temperature to be used when generating new recipe.
	"""

	# load appropriate generator, more models can be added here later if developed
	generator = tf.keras.models.load_model('generator_GRU')

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

		recipe = start + ''.join(result)
		recipe.replace('␣', '')

	return recipe
