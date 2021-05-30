# Note
This is a temporary document that describes the instructions that the user should execute to set up the program. The content will eventually be copied into the README.md file, so that this file can be deleted.

# Introduction
In this document, we will show you how to build this project from scratch. After following all the instructions, you will be able to find recipes and generate new ones, and much more.

1. Acquire and Prepare Data (recipes1M)
2. Acquire and Prepare Data (Kaggle) [if needed]
3. Load & Train Models [if needed]

# Data Preparation
In this section, you will set up the recipes1M database. To obtain the data, visit the (pic2recipe)[http://pic2recipe.csail.mit.edu/] website, and follow the instructions to download the dataset. This will involve creating an account. Next, go to the (download)[http://im2recipe.csail.mit.edu/dataset/download/] page and download from the link labeled "Layers".

Place this file in the directory of your GitHub repository and check that the following conditions hold.
1. The data file is named "recipe1M_layers.tar.gz" (this is the default name). 
2. There is a .gitignore text file in the repository that contains both "recipe1M_layers.tar.gz" and "recipes1M.db" in it. It is fine if there's other text as well.

It is important that both of these conditions are satisfied before proceeding! The recipes1M.db file is large (over 1.5 GB) and you do not want to attempt to push it to GitHub.

Next, run the file `prepare_data.py`, and you will be good to go!