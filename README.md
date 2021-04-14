# Project Proposal
## Abstract
The goal is to design and implement a program that will take in existing recipe data and output a coherent computer-generated recipe fit with the required ingredients and directions to follow sucessfully. We anticipate the creation of this program will draw primarily on these skills: _data manipulation_ (to format the data in a way that facilitates the model's success), _natural language processing_ (to break down and understand a recipe, and to write a novel one), and _machine learning_ (to discover patterns across recipes, and to avoid generating unreasonable results).
## Deliverables
Full Success: 

A fully successful version of our project would be a machine learning model that can create new recipes based on the ingredient data that it is given. If everything goas according to plan, someone with no coding experience should be able to seamlessly input their ingredients to obtain a somewhat coherent recipe, with all the intrsutions and measurments. 

Partial Success: 

The most difficult task would be the actual generation of a new recipe. If this task turns out to be too difficult, we would like our model to be able to point to an existing recipe based on the ingredients the user inputs. The resulting recipes will be drawn from a pool of recipes gathered online through web scraping. There should be quitable representation of different cultures and culinary practices in the resulting recipes. 
## Resources
For our first deliverable we will be working with a few different recipe datasets found on Kaggle. These datasets can be found [here](https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions?select=PP_recipes.csv). These datasets only contain recipes from [food.com](https://www.food.com/). This will give us a framework to understand what sorts of data need to be scraped from the internet for our next deliverable which will contain recipe data from a multitude of different sources, spanning different cuisines and cultures.
## Tools/Skills

There are multiple different skills we'll need in order to realize this project- the main three being _machine learning_, _natural language processing_, and _web-scraping_. If we cannot find enough pre-collected or sufficient recipe data online, we can use tools from `scrapy` in order to collect more data. Additionally, natural language processing techniques from `nltk` may come in handy when we are looking at these websites and trying to break down a written recipe into simpler and more digestible pieces of data that we can use to train our machine learning model. NLP techniques will likely be useful in generating new recipes too. Lastly, we'll want to utilize tools from `scikit-learn` in order to build machine learning models on input data.

Depending on the amount of data we are actually able to collect, using `sqlite` databases in lieu of `pandas` dataframes may also be a possibility, as it would help to improve efficiency and allow us to train machine learning models on a much more reliable foundation. Visualizations from `seaborn` or `plotly` may also be useful to use, in order to portray relationships between variables in a way that explains and motivates our predictor variable choices.
## Risks
One risk that this project faces is whether or not we will be able to find and parse through useful data appropriately and effectively. As detailed in the ethics section below, we want to make sure to diversify our input data as best as possible in order to minimize our machine learning model developing cultural biases. Using web-scraping techniques on a variety of different websites with different formats could prove difficult, as we have to standardize all of our input data in order to train a machine learning model effectively. Perhaps one website specifies cooking time very clearly, while another does not. Or, perhaps one website lists measurements for their ingredients, while another tells the reader to eyeball the amount. There do exist databases of consolidated recipe information online already, but we have to work harder in order to integrate other sources of data into our project.

Another risk is whether or not generating a __new__ recipe is actually possible. We can try to break information about recipes found online into smaller, more concrete pieces of data- like ingredients, cooking time, cooking techniques, measurements, etc. However, we aren't sure that NLP techniques will allow us to reconstruct this data back into a new recipe that makes sense and is readable. We can try to simplify our generated recipes a bit, for example if we just return a list of ingredients and cooking steps. If this still falls through, we can still work on making a project that can __recommend__ a suitable recipe for the user to cook based on input ingredients, which is also pretty cool!
## Ethics
As described in the assignment example, our project has the potential to be biased against particular cuisines. If our starting data is mostly made up of dishes from, say, Japan, then the new recipes it generates (or the existing recipes it suggests) could very possibly draw more heavily from that type of food, at the cost of other cuisines. The easiest way to try to prevent this would be to diversify the data that we draw on to form our data set. This can be achieved by manually checking the websites that we scrape, or the existing data we acquire, to see the approximate distribution of cuisines. We could then search for and add in websites which focus on recipes from a culture that is underrepresented in our data. For example, are we missing Nigerian or Turkish food? Head over [here](https://www.allnigerianrecipes.com/) or [here](https://www.turkfoodsrecipes.com/). These were just two random countries I though of, and recipe sites focused on their food were easy to find, so this is a problem that can be manually rectified.

Another solution would be to add a feature allowing users to submit websites that they know of to the database. Then the web scraper can check out these places as well. This has the advantage of expanding cultural reach beyond the cuisines that the authors have been exposed to. In this way, potential bias in the form of cultural omission can be reversed into a potential strength, allowing a diverse audience to make new contributions that grow the variety of recipes included.

## Timeline
The following schedule lays out the anticipated schedule of the project in two week intervals.

### Stage 1 (after two weeks)
By this point, we aim to build a program which accepts a list of available ingredients and finds an existing recipe in the database that uses the most of the ingredients. This will involve some work in collecting data and manipulating it, but not too much. The main focus will be on locating an optimal recipe in an efficient manner. We will need code to analyze the text to the recipe to determine what ingredients it requires and an algorithm to determine which recipe best suits the user, based on the raw materials and amounts they have on hand.
### Stage 2 (after four weeks)
In this period, we target our main source of potential bias (failing to treat different cuisines in an equitable manner). As a baseline plan, we will incorporate new data sets of recipes that bring different cultures into our existing data. This may require some hefty data manipulation, depending on the format of the data sets. However, our ideal result will be a web scraper that can visit food-related websites and collect recipe data autonomously. In this case, we need only feed the web scraper new URLs to go to. This will allow our program to diversify and ensure it does not silence other cuisines by omission.
### Stage 3 (after six weeks)
Finally, our ultimate goal is to design and implement a machine learning model that can analyze the data we have collected and produce a brand-new recipe to match the supplies that the user already has on hand. We anticipate this will draw on multiple techniques: natural language processing (to break down and understand a recipe, and to write a novel one), machine learning (to discover patterns across recipes, and to avoid generating unreasonable results), and data manipulation (to format the data in a way that facilitates the model's success).

## Notes
This is stuff that David wrote down during Saturday's meeting. I'll delete it before we submit.

2. full success is inputting a list of available ingredients, and then a ML model that creates a new recipe to help you use up as much of your ingredients as possible.

partial success is taking in a list of available ingredients, and then finding a recipe that matches most of the ingredients, and then sending the appropriate link.

Timeline

Checkpoint 1: A simple model that takes in a list of ingredients and finds a recipe that uses them.
Checkpoint 2: Expand to new data sets, scrape, and integrate with existing data.
Checkpoint 3: Train a ML model on the totality of the data, so that it can generate new and exciting recipes to try.
