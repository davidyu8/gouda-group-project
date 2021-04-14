# Project Proposal
## Abstract
The goal is to design and implement a program that will take in existing recipe data and output a coherent computer-generated recipe fit with the required ingredients and directions to follow sucessfully. We anticipate the creation of this program will draw primarily on these skills: data manipulation (to format the data in a way that facilitates the model's success), natural language processing (to break down and understand a recipe, and to write a novel one), and machine learning (to discover patterns across recipes, and to avoid generating unreasonable results).
## Deliverables
## Resources
## Tools/Skills
## Risks
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
