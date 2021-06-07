# Introduction
In need of a new recipe? Have a few old pantry items that have be used up? Well, look no further, because the Gouda Group has the answer for you!

This repository allows you to (a) search for recipes that match a list of ingredients, and (b) generate new recipes to try (if you dare). You could be cooking up a storm in no time! And for the technically inclined, we have included a full guide on how to train your own recipe generation models from scratch.

## Repository Organization
We have several folders and files in this repository. The purpose of each one is explained below.
### Folders
1. data: This folder will contain our main source of data, a collection of over 1 million recipes located [here](http://im2recipe.csail.mit.edu/dataset/login/). We say "will" because the data set is large and therefore not actually included in the repository. Instructions and code for preparing the data are in the Installation section.
2. flask: This folder contains the material needed to run the recipe web application locally.
3. py: This folder contains various code files needed for the project.
4. weights: If you choose to train your own models, the model weights will be saved here.
### Files
1. .gitignore: Text file containing filenames for GitHub Desktop to ignore.
2. README.md: You are here!
4. proposal.md: The project proposal we wrote at the beginning of the quarter.
6. `recipe_generator.ipynb`: Defines and trains RNNs to generate new recipes. If you want to make your own models, this is the place to do it!

# Installation
To use this repository, clone it to your machine and follow these instructions, which will walk you through the process of preparing the recipes1M.db database.

To obtain the data, visit the [pic2recipe](http://pic2recipe.csail.mit.edu/) website, and follow the instructions to download the dataset. This will involve creating an account. Next, download the data from the link labeled "Layers". The file should be about 400 MB in size, and will take a while to download!

Place this file in the top-level directory of your cloned repository and check that the following conditions hold.
1. The data file is named "recipe1M_layers.tar.gz" (this is the default name). If the file is named "recipe1M_layers.tar" without the .gz extension, it's possible that your browser decompressed the file upon downloading. If this occurs, try downloading the file via chrome, and the .gz extension should be preserved.
2. There is a .gitignore text file in the repository that contains both "recipe1M_layers.tar.gz" and "recipes1M.db" in it. It is fine if there's other text as well.

It is important that both of these conditions are satisfied before proceeding! The recipes1M.db file is large (over 1 GB) and you do not want to attempt to push it to GitHub.

Next, open up a command line interface. Activate a Python environment and change the directory to the `py` folder. Then run the file `prepare_data.py` (by typing `python prepare_data.py`). This may take a few minutes. The file will periodically print updates on its progress. If you see "conversion successful!", then you are good to go!

# Demo

## Website

In order to run our site using Flask, there's a few things we have to do:

1. Make sure Flask is installed on your machine, either manually using the command line or through a GUI like Anaconda Navigator.
2. Using the command line, navigate to the "flask" directory in your cloned project repository. Then, run the following three lines:

```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

(_note_: if the terminal does not recognize flask as a command, make sure you are in the correct Python environment. Using the Anaconda framework, this can be done by calling the line `conda activate env`, where `env` is the Anaconda environment in which Flask has been isntalled.

Your command line should now display something similar to the following:

```
* Serving Flask app "app" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 297-133-662
```

Using a browser to navigate to http://127.0.0.1:5000/, you can now access the Flask website!

![alt text](https://github.com/davidyu8/gouda-group-project/blob/main/flask/images_for_readme/homepage.jpeg)

## Recipe Finding

Clicking on `Find a Recipe`, we can navigate to the page that allows us to find a recipe given a user specified list of ingredients. For example, let's say we have potatoes, chives, butter, and pork in our kitchen. We can input these ingredients into the site, and it will find an appropriate recipe to cook!

![alt text](https://github.com/davidyu8/gouda-group-project/blob/main/flask/images_for_readme/recipe_find.png)

This page works by calling our `find_recipe` function, which goes through the following steps to find recipes:

1. Query the `recipes1M.db` database for recipes matching at least one of the user's input ingredients, and store the retrieved recipes in a `pandas` dataframe.
2. Scan through the dataframe and assign each recipe a score based on how many ingredients match the user's supplied ingredients.
3. Return a random recipe with the best score possible, i.e. the most matching ingredients.

For more information, docstrings, and comments on this function, check the `find_recipe.py` file, contained within the `py` directory in this repository.

## Recipe Generating

Clicking on `Create a Recipe`, we can navigate to the page that allows us to generate a new recipe based on an input ingredient. For example, let's say we want to generate a recipe that uses meatballs. Providing the site with our desired input, it'll try and create a brand-new computer-generated recipe as follows:

![alt text](https://github.com/davidyu8/gouda-group-project/blob/main/flask/images_for_readme/recipe_generate.png)

Under the hood, this page is using a __GRU__, which is a type of __recurrent neural network__, or __RNN__. Recurrent neural networks are particularly helpful here, as they are able to work with data that is _sequential_, like text in a recipe. In order to use this method of text generation, we call a function `generate_recipe_GRU` that does the following:

1. Loads in a pre-trained GRU model.
2. Uses the model to generate new text on top of a seed string supplied by the user.

These two steps are relatively simple themselves, but there's quite a bit of auxiliary code that goes into actually making this process happen. The definition of `generate_recipe_GRU` and all of its helper code can be found in the `generators.py` file, contained within the `app` directory used to set up the Flask site.

(_note_: in `recipe_generator.ipynb`, a user can actually train an __LSTM__ (long short-term memory) model, which is a bit more rudimentary than the GRU. We haven't included direct accesibility to an LSTM model in the Flask website because its recipe generation is quite nonsensical compared to the GRU, but it can be implemented somewhat easily by a more curious user.)

## Limitations

As evidenced by the sample recipe output, the generator is a bit lacking. It can produce English text that is largely readable, but the content of the recipe doesn't make a lot of sense. It would certainly be a struggle to cook this, to say nothing of what it would actually taste like.

To mitigate this, we attempted to design a generative adversarial network (GAN) to be the model framework, instead of an LSTM or GRU. A GAN is made up of two parts, a generator (similar to the RNNs we used) and a discriminator, which tries to classify text as either real (originating from an actual recipe) or fake (created by the generator). Over time, the aim is to allow the generator to become better and better at generating text, to the point where the discriminator can no longer tell which is which.

Unfortunately, we were not able to successfully implement this model. So it remains an intriguing and complex extension to our project.

# Conclusion
We really enjoyed designing and implementing this project. The recipe finder is useful because it can draw upon a huge reservoir to make recipe suggestions in response to detailed user requests. If you want to use up a specific set of ingredients that will expire soon, this function provides a way to quickly obtain only the recipes that satisfy that constraint.

The recipe generator was quite fun as well. It was really cool to see that our model could learn English and recipe-specific language with just a couple hours of training, and also simultaneously funny to see the clear culinary genius that it had learned as well.

## Credits
We want to give credit to the [Recipe1M team](http://im2recipe.csail.mit.edu/) at MIT for originally gathering the data that we used. We also want to credit [Oleksii Trekhleb](https://github.com/trekhleb) for the [post](https://www.kdnuggets.com/2020/07/generating-cooking-recipes-using-tensorflow.html) he wrote on the [KDNuggets](https://www.kdnuggets.com/) blog. This post provided a lot of helpful guidance to get the generation part of our project off the ground, particularly in `train.py` and `recipe_generator.ipynb`.

## Group Contributions

The following outlines the main contributions made by each member of our group.

* David implemented the text generation models that were used to create new recipes. This included building a variety of models to learn from the recipe database, then training, evaluating, and adjusting them, and finally making a version that could quickly generate new recipe text in the web app.
* 
*