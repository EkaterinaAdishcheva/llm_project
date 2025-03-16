import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from tqdm import tqdm
import pickle

from Recipe import Recipe

def process_recipe_html(file_name):
    """
        this function scrap html files and get all features from the file
        return dict with recipe features
        
        file_name: file to process        
    """
    site = open(file_name)
    res = {}
    soup = BeautifulSoup(site, 'html5lib')

    description = soup.find_all('span', class_ = {'detailed_full'})
    res['description'] = [x.get_text().strip() for x in description]

    type = soup.find_all('span', itemprop = {'itemListElement'})
    res['type'] = [x.get_text().strip() for x in type]

    tags = soup.find_all('div', class_ = {'detailed_tags'})
    if len(tags) > 0:
        tags = [x.get_text().strip() for x in tags][0]
        tags = re.split("\n | /", tags)
        tags = [t.strip() for t in tags]
        tags = [t for t in tags if t != '']
        res['tags'] = tags

    _ingridients = soup.find_all('li', class_ = {'ingredient'})
    _ingridients = [x.get_text().strip() for x in _ingridients]
    ingridients = []
    for ing in _ingridients:
        ing = re.split("\n | /", ing)
        ing = [t.strip() for t in ing]
        ing = [t for t in ing if t != '']
        ingridients.append(ing)
    res['ingridients'] = ingridients

    yield_value = soup.find_all('span', class_ = {'yield value'})
    res['yield_value'] = [x.get_text().strip() for x in yield_value]

    calories_info = soup.find_all('div', class_ = {'calories_info'})
    if len(calories_info) > 0:
        calories_info = [x.get_text().strip() for x in calories_info][0]
        calories_info = re.split("\n | /", calories_info)
        calories_info = [t.strip() for t in calories_info]
        calories_info = [t for t in calories_info if t != '']
        res['calories_info'] = calories_info

    ratingValue = soup.find_all('span', itemprop = {'ratingValue'})
    ratingValue = [x.get_text().strip() for x in ratingValue]
    res['ratingValue'] = ratingValue

    ratingCount = soup.find_all('span', itemprop = {'ratingCount'})
    ratingCount = [x.get_text().strip() for x in ratingCount]
    res['ratingCount'] = ratingCount

    steps = soup.find_all('div', class_ = {'detailed_step_description_big'})
    steps = [x.get_text().strip() for x in steps]
    res['steps'] = steps
    
    time = soup.find_all('span', class_ = {'duration'})
    time = [x.get_text().strip() for x in time]
    res['time'] = time
    
    return res


def make_data_set(dir_name):
    """
        process all files in the direction and makes list of precessed recipes       
    """
    for _, _, files  in os.walk(dir_name):
        break

    results = []
    for _name in tqdm(files):    
        results.append(process_recipe_html(dir_name + _name))
        
    return results


def save_recipes_pkl(recipes_list, file_name):
    """
        saves recipes list to file       
    """
    with open(file_name, 'wb') as handle:
        pickle.dump(recipes_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        
def read_recipes_pkl(file_name):
    """
        saves recipes list to file       
    """
    with open(file_name, 'rb') as handle:
        res = pickle.load(handle)
        
    return res


def good_recipe(recipe):
    if recipe.name is None:
        return False
    
    if len(recipe.steps) == 0 or len(recipe.steps) >= 10:
        return False
    
    if len(recipe.ingridients) == 0:
        return False
    
    if recipe.ratingValue < 4:
        return False

    if recipe.ratingCount < 3:
        return False
    
    if recipe.standard_time >= 120:
        return False

    return True


def make_recipes(recipes, output_file=None):
    result = []

    for rec in recipes:
        _rec = Recipe(rec)
        _rec.standardize_time()
        
        if good_recipe(_rec):
            _rec.make_document()    
            result.append(_rec)

    print(f"Total {len(result)} recipes is picked up")
    
    if output_file is not None:
        with open(output_file, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    
    return result    