```python
import json
import pandas as pd
import sqlite3
```


```python
with open("recipes_raw\\recipes_raw_nosource_ar.json") as f:
    data = json.load(f)
df = pd.DataFrame(data)
df.shape
```




    (4, 39802)




```python
df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>rmK12Uau.ntP510KeImX506H6Mr6jTu</th>
      <th>5ZpZE8hSVdPk2ZXo1mZTyoPWJRSCPSm</th>
      <th>clyYQv.CplpwJtjNaFGhx0VilNYqRxu</th>
      <th>BmqFAmCrDHiKNwX.IQzb0U/v0mLlxFu</th>
      <th>N.jCksRjB4MFwbgPFQU8Kg.yF.XCtOi</th>
      <th>kq.naD.8G19M4UU9dVvJgHtpfo.l/eC</th>
      <th>lYrgWNn00EXblOupzM3tL0jGr9O0CB2</th>
      <th>Fu0DgGYFUGwc0BBlN6r20o/ihOVs5bO</th>
      <th>MBRNtqELRRuv8zJH4k7Aba2bmIc2A3C</th>
      <th>ZPyPoMiNvgAfrKcRpH9FEYV/XsPZBsW</th>
      <th>...</th>
      <th>uHHb42/tuIKsmN5U6l9AD.FdVpSFxs6</th>
      <th>IPAeN3L6rm2oughJpUhbG038k.ACJ0K</th>
      <th>3UIhlTQFH5jyIaHN8zeKlK5V.94Kjwu</th>
      <th>PdBxkE2gnI/.ynokkp1Hu1KLGZnGdei</th>
      <th>SB46Udqc5Svsi70S1qRmRLv5tlg8Oca</th>
      <th>gehEOcDPtU3SmNSXrwWwWD4ulPpUdMO</th>
      <th>VRAsyF.1xMBYqAVKX1biyIORH6N6qzy</th>
      <th>Lf8/u.0k2029QMSQFrHS4gRsvKOQFUG</th>
      <th>ay.AqX/9ysBtWHcnHoDeGAyJ5Orla8e</th>
      <th>2Q3Zpfgt/PUwn1YABjJ5A9T3ZW8xwVa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>title</th>
      <td>Slow Cooker Chicken and Dumplings</td>
      <td>Awesome Slow Cooker Pot Roast</td>
      <td>Brown Sugar Meatloaf</td>
      <td>Best Chocolate Chip Cookies</td>
      <td>Homemade Mac and Cheese Casserole</td>
      <td>Banana Banana Bread</td>
      <td>Chef John's Fisherman's Pie</td>
      <td>Mom's Zucchini Bread</td>
      <td>The Best Rolled Sugar Cookies</td>
      <td>Singapore Chili Crabs</td>
      <td>...</td>
      <td>Citrus Creme Brulee</td>
      <td>Honey Nutty Granola</td>
      <td>Salmon en Croute</td>
      <td>Homemade Blender Butter</td>
      <td>Gluten Free Chicken Noodle Soup</td>
      <td>Thai-Indian Veggie Soup</td>
      <td>Coconut Milk-Free Panang Curry Chicken</td>
      <td>Cooked Cold Salad</td>
      <td>Easy Eggnog Creme Brulee</td>
      <td>Super Power Stovetop Granola</td>
    </tr>
    <tr>
      <th>ingredients</th>
      <td>[4 skinless, boneless chicken breast halves AD...</td>
      <td>[2 (10.75 ounce) cans condensed cream of mushr...</td>
      <td>[1/2 cup packed brown sugar ADVERTISEMENT, 1/2...</td>
      <td>[1 cup butter, softened ADVERTISEMENT, 1 cup w...</td>
      <td>[8 ounces whole wheat rotini pasta ADVERTISEME...</td>
      <td>[2 cups all-purpose flour ADVERTISEMENT, 1 tea...</td>
      <td>[For potato crust: ADVERTISEMENT, 3 russet pot...</td>
      <td>[3 cups all-purpose flour ADVERTISEMENT, 1 tea...</td>
      <td>[1 1/2 cups butter, softened ADVERTISEMENT, 2 ...</td>
      <td>[Sauce: ADVERTISEMENT, 1/2 cup ketchup ADVERTI...</td>
      <td>...</td>
      <td>[2 oranges, juiced ADVERTISEMENT, lemon, juice...</td>
      <td>[3 cups rolled oats ADVERTISEMENT, 1 1/2 cups ...</td>
      <td>[1 cup watercress, or as desired ADVERTISEMENT...</td>
      <td>[2 pints heavy whipping cream ADVERTISEMENT, s...</td>
      <td>[1/2 (12 ounce) box Barilla® Gluten Free Elbow...</td>
      <td>[2 teaspoons olive oil ADVERTISEMENT, 1/4 cup ...</td>
      <td>[2 cups light cream ADVERTISEMENT, 1/4 teaspoo...</td>
      <td>[3 tablespoons bacon grease ADVERTISEMENT, 2 c...</td>
      <td>[4 egg yolks ADVERTISEMENT, 1 tablespoon white...</td>
      <td>[1/4 cup canola oil ADVERTISEMENT, 3 cups quic...</td>
    </tr>
    <tr>
      <th>instructions</th>
      <td>Place the chicken, butter, soup, and onion in ...</td>
      <td>In a slow cooker, mix cream of mushroom soup, ...</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>Preheat oven to 350 degrees F. Line a 2-quart ...</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>Bring a large saucepan of salted water and to ...</td>
      <td>Grease and flour two 8 x 4 inch pans. Preheat ...</td>
      <td>In a large bowl, cream together butter and sug...</td>
      <td>Whisk ketchup, chicken broth, egg, soy sauce, ...</td>
      <td>...</td>
      <td>Preheat oven to 300 degrees F (150 degrees C)....</td>
      <td>Preheat oven to 300 degrees F (150 degrees C)....</td>
      <td>Preheat oven to 375 degrees F (190 degrees C)....</td>
      <td>Pour cream into a blender. Cover and blend unt...</td>
      <td>Saute onions in olive oil over medium heat unt...</td>
      <td>Heat oil in a large pot over medium heat. Add ...</td>
      <td>Heat cream and coconut extract in a skillet or...</td>
      <td>Heat bacon grease in a skillet over medium-hig...</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>Heat 1/4 cup canola oil in large skillet over ...</td>
    </tr>
    <tr>
      <th>picture_link</th>
      <td>55lznCYBbs2mT8BTx6BTkLhynGHzM.S</td>
      <td>QyrvGdGNMBA2lDdciY0FjKu.77MM0Oe</td>
      <td>LVW1DI0vtlCrpAhNSEQysE9i/7rJG56</td>
      <td>0SO5kdWOV94j6EfAVwMMYRM3yNN8eRi</td>
      <td>YCnbhplMgiraW4rUXcybgSEZinSgljm</td>
      <td>jRnWGDXDdyOg3rta4/HVAR2rD19XubC</td>
      <td>aUca10AaD8T2yYvcLOgH/UJlR5/OhOe</td>
      <td>YdgEVyLVffZgh9NZPN3Eqj6MaX8KdzK</td>
      <td>UrgvDGu4roLiho160fTVIwCUrGZna8i</td>
      <td>OFp6yXFwzlrkMQ5STffYPllxQvMVLUS</td>
      <td>...</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>cWEzUSv9Ozr3b4MxNVCqJYgTjIS.kHm</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
      <td>qE58a7Z1Au0GXvPO188iHZZVqna9hLa</td>
    </tr>
  </tbody>
</table>
<p>4 rows × 39802 columns</p>
</div>




```python
df = df.T
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>ingredients</th>
      <th>instructions</th>
      <th>picture_link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>rmK12Uau.ntP510KeImX506H6Mr6jTu</th>
      <td>Slow Cooker Chicken and Dumplings</td>
      <td>[4 skinless, boneless chicken breast halves AD...</td>
      <td>Place the chicken, butter, soup, and onion in ...</td>
      <td>55lznCYBbs2mT8BTx6BTkLhynGHzM.S</td>
    </tr>
    <tr>
      <th>5ZpZE8hSVdPk2ZXo1mZTyoPWJRSCPSm</th>
      <td>Awesome Slow Cooker Pot Roast</td>
      <td>[2 (10.75 ounce) cans condensed cream of mushr...</td>
      <td>In a slow cooker, mix cream of mushroom soup, ...</td>
      <td>QyrvGdGNMBA2lDdciY0FjKu.77MM0Oe</td>
    </tr>
    <tr>
      <th>clyYQv.CplpwJtjNaFGhx0VilNYqRxu</th>
      <td>Brown Sugar Meatloaf</td>
      <td>[1/2 cup packed brown sugar ADVERTISEMENT, 1/2...</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>LVW1DI0vtlCrpAhNSEQysE9i/7rJG56</td>
    </tr>
    <tr>
      <th>BmqFAmCrDHiKNwX.IQzb0U/v0mLlxFu</th>
      <td>Best Chocolate Chip Cookies</td>
      <td>[1 cup butter, softened ADVERTISEMENT, 1 cup w...</td>
      <td>Preheat oven to 350 degrees F (175 degrees C)....</td>
      <td>0SO5kdWOV94j6EfAVwMMYRM3yNN8eRi</td>
    </tr>
    <tr>
      <th>N.jCksRjB4MFwbgPFQU8Kg.yF.XCtOi</th>
      <td>Homemade Mac and Cheese Casserole</td>
      <td>[8 ounces whole wheat rotini pasta ADVERTISEME...</td>
      <td>Preheat oven to 350 degrees F. Line a 2-quart ...</td>
      <td>YCnbhplMgiraW4rUXcybgSEZinSgljm</td>
    </tr>
  </tbody>
</table>
</div>




```python
def find_recipe(ingredients):
    df["Score"] = 0
    for ingr in ingredients:
        for recipe in df["ingredients"]:
            for recipe_ingredient in recipe:
                if ingr in recipe_ingredient:
                    return recipe
```


```python
find_recipe(["eggs"])
```




    ['1/2 cup packed brown sugar ADVERTISEMENT',
     '1/2 cup ketchup ADVERTISEMENT',
     '1 1/2 pounds lean ground beef ADVERTISEMENT',
     '3/4 cup milk ADVERTISEMENT',
     '2 eggs ADVERTISEMENT',
     '1 1/2 teaspoons salt ADVERTISEMENT',
     '1/4 teaspoon ground black pepper ADVERTISEMENT',
     '1 small onion, chopped ADVERTISEMENT',
     '1/4 teaspoon ground ginger ADVERTISEMENT',
     '3/4 cup finely crushed saltine cracker crumbs ADVERTISEMENT',
     'ADVERTISEMENT']




```python
df.iloc[2, 0]
```




    'Place the chicken, butter, soup, and onion in a slow cooker, and fill with enough water to cover.\nCover, and cook for 5 to 6 hours on High. About 30 minutes before serving, place the torn biscuit dough in the slow cooker. Cook until the dough is no longer raw in the center.\n'




```python

```


```python
import numpy as np

with np.load('simplified-recipes-1M.npz', allow_pickle = True) as data:
    recipes = data['recipes']
    ingredients = data['ingredients']
```


```python
ingredients[recipes[10]]
```




    array(['avocado', 'blue cheese', 'cheese', 'cottage cheese', 'cream',
           'crumbled blue cheese', 'garlic', 'garlic powder', 'lemon',
           'lemon juice', 'onion', 'onion salt', 'pepper', 'salt', 'sauce',
           'sour cream', 'worcestershire sauce'], dtype='<U39')




```python
df_rec = pd.DataFrame({"recipes": recipes})
df_ing = pd.DataFrame({"ingredients": ingredients})
```


```python
df_rec.shape
```




    (1067557, 1)




```python

```
