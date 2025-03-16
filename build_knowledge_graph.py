from collections import defaultdict
import spacy
from tqdm import tqdm
import re
import networkx as nx

from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords


nlp = spacy.load("ru_core_news_sm")

ATTRIBUTES_ORDER = [
    'mainIngridients',
    'ingridients',
    'diet',
    'meal',
    'occasions',
    'geography',
]

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            
            tokens.append(token)
    return tokens

def make_tags_list_for_attribute(recipes_list, attribute, min_count=10):
    
    tags_stat = defaultdict(int)
    for recipe in recipes_list:
        tags_list = getattr(recipe, attribute)
        if tags_list is not None:
            for tag in tags_list:
                if attribute == 'ingridients':
                    tags_stat[tag[0]] += 1
                else:
                    tags_stat[tag] += 1
        
    tags_list = list(tags_stat.keys()) 
    for tag in tags_list:
        if tags_stat[tag] < min_count:
            del tags_stat[tag]
                
    return tags_stat

    
def make_tags_list(recipes_list):
    
    tags = {}
    
    for attribute in ATTRIBUTES_ORDER:
        tags[attribute] = make_tags_list_for_attribute(recipes_list, attribute)
        
    return tags


def lemmatize_sentance(text):
    return lemmatize(text)
    # res = [nlp(word)[0].lemma_ for word in text.split(" ")]
    # return res
    

def lemmatize_tags(tags):
    nlp = spacy.load("ru_core_news_sm")
    for attribute in tags:
        for tag in tags[attribute]:
            if "(" in tag:
                new_tag = re.sub(r'\([^)]*\)', '', tag).strip()
            else:
                new_tag = tag
            tags[attribute][tag] = {
                'stat': tags[attribute][tag],
                'lemma': tuple(lemmatize_sentance(new_tag))
            }   



def add_recipes_to_graph(G, recipes_list):
    for recipe in recipes_list:
        G.add_node(recipe.uuid, node_type="recipe")
        G.nodes[recipe.uuid]['name'] = recipe.name
    

def add_tags_to_graph(G, tags):
    for attribute in tags:
        for tag in tags[attribute]:
            G.add_node(tags[attribute][tag]['lemma'], node_type=attribute)


def add_edges_to_graph(G, recipes_list, tags):
    for attribute in ATTRIBUTES_ORDER:
        for recipe in recipes_list:
            tags_list = getattr(recipe, attribute)
            if tags_list is not None:
                for tag in tags_list:
                    if attribute != 'ingridients':
                        if tag in tags[attribute]: 
                            if G.has_node(tags[attribute][tag]['lemma']):
                                G.add_edge(recipe.uuid, tags[attribute][tag]['lemma'])
                    else:
                        if tag[0] in tags[attribute]: 
                            if G.has_node(tags[attribute][tag[0]]['lemma']):
                                G.add_edge(recipe.uuid, tags[attribute][tag[0]]['lemma'])


def build_knowledge_graph(recipes_list, tags):
    
    G = nx.Graph()
    add_recipes_to_graph(G, recipes_list)
    add_tags_to_graph(G, tags)
    add_edges_to_graph(G, recipes_list, tags)
    
    return G
    


def querry_graph(querry, graph, tags, min_number=5):
    querry_lemms = lemmatize_sentance(querry)
    
    
    answer = set()
    
    for n in graph.nodes():
        if graph.nodes[n]['node_type'] == 'recipe':
            answer.add(n)

    for attribute in ATTRIBUTES_ORDER:
        for tag in tags[attribute]:
            if len(set(querry_lemms).intersection(set(tags[attribute][tag]['lemma'])))\
                    == len(set(tags[attribute][tag]['lemma'])):
                current_subgraph = set()
                for n in graph.neighbors(tags[attribute][tag]['lemma']):
                    current_subgraph.add(n)
                answer_new = answer.intersection(current_subgraph)
                if len(answer_new) < min_number:
                    break
                answer = answer_new
    return answer_new, None