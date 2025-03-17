import re
import uuid
from langchain_core.documents import Document
from build_knowledge_graph import query_graph, ATTRIBUTES_ORDER, enreach_query_with_relative_tags

def make_str(obj):
    res = ''
    if isinstance(obj, list):
        for obj_ in obj:
            if res == "":
                res = make_str(obj_)
            else:
                res += ", " + make_str(obj_)
    else:
        if res == "":
            res = str(obj)
        else:
            res += ", " + str(obj)
    return res

class Recipe:
    def __init__(self, recipe=None):
        if recipe is not None:
            self.make_keys_dict()
            for key in self.keys_dict:
                setattr(self, key, None)
            self.add_features(recipe)
            self.clean_tags()
            self.add_tags()

    def make_document(self):            
        self.uuid = str(uuid.uuid4())
        self.document = Document(
            page_content=(self.make_str_recipe()).\
                replace('\t', ' ').replace('\n', ' ').replace('  ', ' '),
            metadata={'uuid': self.uuid, 'name': self.name})
    

    def display(self):
        for attr in self.__dict__.keys():
            print(f"{attr}: {getattr(self, attr)}")


    def clean_tags(self):        
        if self.geography is not None:
            self.geography = [tag.replace('кухня', '').strip() for tag in self.geography]
        if self.diet is not None:
            self.diet = [tag.replace('рецепты', '').replace('питание', '').replace('для', '').strip() for tag in self.diet]
            


    def add_tags(self):
        if self.occasions is not None:
            if 'для детей' in set(self.occasions):
                self.occasions.append('детский')
        if self.diet is not None:
            if 'пп' in set(self.diet):
                self.diet.append('полезный')
                self.diet.append('здоровый')     

    def standardize_time(self):
        if self.time is None:
            self.standard_time = 0
            return
        
        s = self.time    
        s = s.replace('ч.', 'ч')
        if "дн." in s:
            days, right = s.split("дн.", 1)
        else:
            days = 0 
            right = s
        if "ч" in right:
            hours, right = right.split("ч")
        else:
            right = s
            hours = 0
        if "мин" in right:
            minutes = right.split("мин")[0]
        else:
            minutes = 0
        self.standard_time = (int(days)*60*24 + int(hours)*60 + int(minutes))

    
    def make_str_recipe(self):
        if self.name is not None:
            res = self.name + "\n\n"
        else:
            res = ""
        if self.description is not None:
            res += "\n".join(self.description) + ".\n\n"
        if self.recipeYield is not None:
            res += self.keys_dict["recipeYield"] + ": " + make_str(self.recipeYield) + ".\n"
        if self.ingridients is not None:
            res += self.keys_dict["ingridients"] + "\n"
            for ing in self.ingridients:
                res += "\t" +  ing[0] + ": " + ing[1] + ".\n"
        if self.steps is not None:
            res += "\n" + self.keys_dict["steps"] + "\n"
            for n, step in enumerate(self.steps):
                res += "\t" + str(n + 1) + ". "  +  step + ".\n"
        for key in self.keys_dict_order[5:]:
            if key in self.__dict__.keys():
                val = getattr(self, key)
                res += self.keys_dict[key] + ": " + make_str(val) + ".\n"
        return res

    def add_features(self, recipe):
        if len(recipe['type']) > 0:
            self.name = recipe['type'][-1]
            self.meal = recipe['type'][2:-1]
        else:
            self.name = None
            
            
        if len(recipe['description']) == 2:
            self.description = [recipe['description'][0], recipe['description'][1].split(":")[1].strip()]
            
            
        self.ingridients = [None] * len(recipe['ingridients'])
        for n, ing_set in enumerate(recipe['ingridients']):
            if '       ' in ing_set[1]:
                ing_set_1 = ing_set[1].split('       ')
                ing_set_1 = [d.strip() for d in ing_set_1 if d != '']
                self.ingridients[n] = (ing_set[0].lower(), ing_set_1[0].lower(), ing_set_1[1].lower())
            else:
                self.ingridients[n] = (ing_set[0].lower(), ing_set[1].lower(), None)

        attr_name = {
            'yield_value': 'recipeYield',
            'Калорийность': 'calories',
            'Жиры': 'fatContent',
            'Углеводы': 'carbohydrateContent',
            'Белки': 'proteinContent',
            'Назначение':'occasions',
            'Диета':'diet',
            'Основной ингредиент': 'mainIngridients',
            'География кухни':'geography',
            'Блюдо':'type_',
        }
        
        _tags = {}

        if 'tags' in recipe.keys():
            i = 0
            key = None
            while (i < len(recipe['tags'])):
                if ":" in recipe['tags'][i]:
                    key = recipe['tags'][i].replace(":","").strip()
                    _tags[key] = []
                else:
                    _tags[key].append(recipe['tags'][i])
                i += 1
                
        for key in _tags:
            setattr(self, attr_name[key], [t.lower() for t in _tags[key]])


        self.ratingValue = 0
        self.ratingCount = 0
        
        for key in ['ratingValue', 'ratingCount']:
            if key in  recipe.keys() and len(recipe[key]) > 0:
                setattr(self, key, float(recipe[key][0]))

        self.time = None
        for key in ['time']:
            if key in  recipe.keys() and len(recipe[key]) > 0:
                setattr(self, key, recipe[key][0])


        for key in ['yield_value']:
            if key in  recipe.keys() and len(recipe[key]) > 0:
                setattr(self, attr_name[key], float(recipe[key][0]))

        if 'calories_info' in recipe.keys():
            for i in range(0, len(recipe['calories_info']), 2):
                val, key = recipe['calories_info'][i], recipe['calories_info'][i + 1]
                setattr(self, attr_name[key], val)
            
        if 'steps' in recipe.keys():
            self.steps = [s.split("\t")[-1].strip() for s in recipe['steps']]
            pattern = r'^\d+\.?\s*'
            for n, st in enumerate(self.steps):
                self.steps[n] = re.sub(r'^\d+\.?\s*', '', st)

    def make_keys_dict(self):
        self.keys_dict = {
            'name':'Название',
            'description': 'Описание',
            'recipeYield': 'Количество порций',
            'ingridients': 'Ингридиенты',
            'steps':'Способ приготовления',
            'calories':'Калории',   
            'proteinContent':'Белки',
            'fatContent':'Жиры',
            'carbohydrateContent': 'Углеводы',
            'time':'Время приготовления',
            'meal':'Тип блюда',
            'occasions':'Назначение',
            'diet':'Диета',
            'mainIngridients': 'Основные ингредиенты',
            'geography':'География кухни',
            'time':'Время',
            'ratingValue':'Средняя оценка',
            'ratingCount':'Количество оценок',
            'standard_time': 'standard_time'
        }

        self.keys_dict_order = [
            'name',
            'description',                  
            'recipeYield',
            'ingridients',
            'steps',
            'calories',
            'proteinContent',
            'fatContent',
            'carbohydrateContent',
            'time',
            'meal',
            'occasions',
            'diet',
            'mainIngridients',
            'geography',
            'ratingValue',
            'ratingCount',]


class RecipesProject():
    def __init__(self, resipes=None, knowledgeGraph=None, tags=None, vectorStore=None, oneWordTags=None):
        
        if resipes is None:
            self.resipes = None
        else:
            self.resipes = resipes
        
        if knowledgeGraph is None:
            self.knowledgeGraph = None
        else:
            self.knowledgeGraph = knowledgeGraph
        
        if tags is None:
            self.tags = None
        else:
            self.tags = tags
            
        if vectorStore is None:
            self.vectorStore = None
        else:
            self.vectorStore = vectorStore
                
        if oneWordTags is None:
            self.oneWordTags = None
        else:
            self.oneWordTags = oneWordTags

    def add_resipes_list(self, recipes_list):
        self.resipes = recipes_list
        
    def add_knowledge_graph(self, graph):
        self.knowledgeGraph = graph
        
    def add_tags(self, tags):
        self.tags = tags
        
    def add_vector_store(self, vector_store):
        self.vectorSore = vector_store
        
    def add_one_word_tags(self, one_word_tags):
        self.oneWordTags = one_word_tags
        
    
    def add_one_word_tags(self, query, verbose=False):
        new_tags = enreach_query_with_relative_tags(query, self.oneWordTags)
        new_tags = " ".join(new_tags)
        if verbose:
            print(f"New tags are added: {new_tags}")
        res = query + " " + new_tags
        return res

    def invoke(self, query, verbose=False):
        query = self.add_one_word_tags(query, verbose=verbose)
        answer = query_graph(query, self.knowledgeGraph, self.tags, verbose=verbose)
        return answer

