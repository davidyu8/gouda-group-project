# Project Proposal
## Abstract
## Deliverables
## Resources
## Tools/Skills
## Risks
## Ethics
As described in the assignment example, our project has the potential to be biased against particular cuisines. If our starting data is mostly made up of dishes from, say, Japan, then the new recipes it generates (or the existing recipes it suggests) could very possibly draw more heavily from that type of food, at the cost of other cuisines. The easiest way to try to prevent this would be to diversify the data that we draw on to form our data set. This can be achieved by manually checking the websites that we scrape, or the existing data we acquire, to see the approximate distribution of cuisines. We could then search for and add in websites which focus on recipes from a culture that is underrepresented in our data. For example, are we missing Nigerian (go [here](https://www.allnigerianrecipes.com/)) or Turkish food (head over [here](https://www.turkfoodsrecipes.com/))? These were just two random countries I though of, and recipe sites focused on their food were easy to find, so this is a problem that can be manually rectified.

Another solution would be to add a feature allowing users to submit websites that they know of to the database. Then the web scraper can check out these places as well. This has the advantage of expanding cultural reach beyond the cuisines that the authors have been exposed to. In this way, potential bias in the form of cultural omission can be reversed into a potential strength, allowing a diverse audience to make new contributions that grow the variety of recipes included.

## Timeline

## Notes
This is stuff that David wrote down during Saturday's meeting. I'll delete it before we submit.

2. full success is inputting a list of available ingredients, and then a ML model that creates a new recipe to help you use up as much of your ingredients as possible.

partial success is taking in a list of available ingredients, and then finding a recipe that matches most of the ingredients, and then sending the appropriate link.

Timeline

Checkpoint 1: A simple model that takes in a list of ingredients and finds a recipe that uses them.
Checkpoint 2: Expand to new data sets, scrape, and integrate with existing data.
Checkpoint 3: Train a ML model on the totality of the data, so that it can generate new and exciting recipes to try.
