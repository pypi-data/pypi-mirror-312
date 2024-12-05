import json
import numpy as np
import re
from itertools import combinations as itertools_combinations
import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from sentence_transformers import SentenceTransformer
import aiohttp
import asyncio
import time
from openai import OpenAI
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from pathlib import Path
import nest_asyncio
import urllib.parse
   
nest_asyncio.apply()
   
ua = UserAgent()

headers = {
    "User-Agent": f"{ua.random}"
    }

this_directory = Path(__file__).parent

folder_path = (this_directory / 'qids_folder')

if not os.path.exists(folder_path):
    os.mkdir(folder_path)
else:
    pass


folder_path_1 = (this_directory / 'info_extraction')

if not os.path.exists(folder_path_1):
    os.mkdir(folder_path_1)
else:
    pass

async def fetch_json(url, session):
    async with session.get(url) as response:
        return await response.json()

async def combination_method(name, session):
    async with aiohttp.ClientSession() as session:
        data = set()
        new_name = name.split()
        x = itertools_combinations(new_name, 2)
        for i in x:
            new_word = (i[0] + " " + i[1])
            url = f"https://www.google.com/search?q={new_word} site:el.wikipedia.org inurl:/wiki/ -inurl:? -inurl:Κατηγορία: -inurl:Αρχείο: -inurl:Χρήστης: -inurl:Βοήθεια: -inurl:Συζήτηση: -inurl:Πρότυπο:&num=5"
            html = requests.get(url, headers=headers)
            soup = BeautifulSoup(html.text, "html.parser")
            elements_with_href = soup.find_all(href=True)
            href_links = [element['href'] for element in elements_with_href]
            for link in href_links:
                if link.startswith('https://el.wikipedia.org/wiki/'):
                    data.add(link.split("/")[-1])
    return data

async def single_method(name, session):
    async with aiohttp.ClientSession() as session:
        data = set()
        new_name = name.replace("-", " ").replace("/", " ").split()
        for i in new_name:
            url = f"https://www.google.com/search?q={i} site:el.wikipedia.org inurl:/wiki/ -inurl:? -inurl:Κατηγορία: -inurl:Αρχείο: -inurl:Χρήστης: -inurl:Βοήθεια: -inurl:Συζήτηση: -inurl:Πρότυπο:&num=5"
            html = requests.get(url, headers=headers)
            soup = BeautifulSoup(html.text, "html.parser")
            elements_with_href = soup.find_all(href=True)
            href_links = [element['href'] for element in elements_with_href]
            for link in href_links:
                if link.startswith('https://el.wikipedia.org/wiki/'):
                    data.add(link.split("/")[-1])
    return data

async def mains(name, single, combination):
    data = set()
    disam_data = set()
    qids = set()
    
    async with aiohttp.ClientSession() as session:
        url = f"https://www.google.com/search?q={name} site:el.wikipedia.org inurl:/wiki/ -inurl:? -inurl:Κατηγορία: -inurl:Αρχείο: -inurl:Χρήστης: -inurl:Βοήθεια: -inurl:Συζήτηση: -inurl:Πρότυπο:"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        elements_with_href = soup.find_all(href=True)
        href_links = [element['href'] for element in elements_with_href]
        for link in href_links:
            if link.startswith('https://el.wikipedia.org/wiki/'):
                data.add(link.split("/")[-1])

        wikipedia_url = f"https://el.wikipedia.org/w/api.php?action=query&list=search&srsearch={name}&srlimit=1&srprop=&srenablerewrites=True&srinfo=suggestion&format=json"
        json_data = await fetch_json(wikipedia_url, session)
        suggestion = json_data.get('query', {}).get('searchinfo', {}).get('suggestion')

        if suggestion:
            suggesion = urllib.parse.unquote(suggestion)
            suggested_url = f"https://el.wikipedia.org/w/api.php?action=query&list=search&srsearch={suggestion}&srlimit=10&srprop=&srenablerewrites=True&srinfo=suggestion&format=json"
            json_suggestion = await fetch_json(suggested_url, session)
            results = json_suggestion.get('query', {}).get('search')
            for i in results:
                data.add(urllib.parse.unquote(i.get('title')))

        # Handle disambiguation links
        if data != {0}:
            for ids in data:
                titles = set()
                wikipedia_disambiguation = f"https://el.wikipedia.org/w/api.php?action=query&generator=links&format=json&redirects=1&pageids={ids}&prop=pageprops&gpllimit=50&ppprop=wikibase_item"
                json_id = await fetch_json(wikipedia_disambiguation, session)
                try:
                    title = json_id.get('query').get('pages')
                    for k, v in title.items():
                        titles.add(urllib.parse.unquote(v.get("title")))
                except:
                    pass

                if "Βικιπαίδεια:Αποσαφήνιση" in titles:
                    for i in titles:
                        if ":" not in i:
                            disam_data.add(urllib.parse.unquote(i))
                else:
                    disam_data.add(ids)

        # Makes combinations of the name
        if combination == "Yes":
            if len(name.replace("-", " ").split()) >= 3: 
                combination_names = await combination_method(name, session)
                for i in combination_names:
                    disam_data.add(i)

        # Checks every word alone
        if single == "Yes":
            if len(name.replace("-", " ").replace("/", " ").split()) >= 2:
                singles = await single_method(name, session)
                for i in singles:
                    disam_data.add(i)

        for ids in disam_data:
            try:
                wikibase_url = f"https://el.wikipedia.org/w/api.php?action=query&titles={ids}&prop=pageprops&format=json"
                json_qid = await fetch_json(wikibase_url, session)
                wikidata_qid = json_qid.get('query', {}).get('pages', {})
                for page_id, page_data in wikidata_qid.items():
                    page_props = page_data.get('pageprops', {})
                    wikibase_item = page_props.get('wikibase_item', None)
                    if wikibase_item:
                        qids.add(wikibase_item)
            except:
                pass

        with open(f"{folder_path}/{name}.json", "w") as f:
            json.dump(list(qids), f)


async def get_results(query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()
    
def get_resultss(query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()
    
def cleaner(text):
    text = text.replace('\\', '').replace('\n', ' ')
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(' +', ' ', text).strip()
    return text

async def retriever(qid):
    async with aiohttp.ClientSession() as session: 
        list_with_sent = []

        query_label = f"""SELECT ?subjectLabel
          WHERE {{
            wd:{qid} rdfs:label ?subjectLabel .
            FILTER(LANG(?subjectLabel) = "el")
          }}
          """

        results = await get_results(query_label)

        label = None
        if results["results"]["bindings"]:
            for result in results["results"]["bindings"]:
                for key, value in result.items():
                    label = value.get("value", {}).lower()

        query_alias = f"""SELECT ?alias
          WHERE {{
            wd:{qid} skos:altLabel ?alias
            FILTER(LANG(?alias) = "el")
          }}
          """

        alias_list = []
        results = await get_results(query_alias)

        for result in results["results"]["bindings"]:
            for key, value in result.items():
                alias = value.get("value", "None")
                alias_list.append(alias)

        query_desci = f"""SELECT ?subjectLabel
        WHERE {{
        ?subjectLabel schema:about wd:{qid} ;
                      schema:inLanguage "el" ;
                      schema:isPartOf <https://el.wikipedia.org/> .
        }}
        """

        results = await get_results(query_desci)
        cleaned_first_para = "None"
        
        if results["results"]["bindings"]:
            for result in results["results"]["bindings"]:
                for key, value in result.items():
                    desc = value.get("value", "None")

                title = desc.split("/wiki/")[1]

                url = f"https://el.wikipedia.org/w/api.php?action=query&prop=extracts&titles={title}&exintro=&exsentences=2&explaintext=&redirects=&formatversion=2&format=json"
                
     
                json_data = await fetch_json(url, session)
                cleaned_first_para = cleaner(json_data.get('query', {}).get('pages', [{}])[0].get('extract', 'None'))
        else:
            query_desc = f"""SELECT ?subjectLabel
            WHERE {{
            wd:{qid} schema:description ?subjectLabel .
            FILTER(LANG(?subjectLabel) = "el")
            }}
            """

            results = await get_results(query_desc)
            if results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    for key, value in result.items():
                        cleaned_first_para = value.get("value", "None")

        list_with_sent.append({"qid": qid, "label": label, "description": cleaned_first_para})

        if alias_list:
            for alias in alias_list:
                list_with_sent.append({"qid": qid, "label": alias.lower(), "description": cleaned_first_para})

        return list_with_sent

async def main(name):
    with open(f"{folder_path}/{name}.json", "r") as f:
        final_list = []
        qids = json.load(f)
        for q in qids:
            returned_list = await retriever(q)
            if returned_list:
                final_list.extend(returned_list)

        with open(f"{folder_path_1}/{name}.json", "w", encoding="utf-8") as flast:
            json.dump(final_list, flast)

def EL(api_token=None, sentence=None, mention=None, single="No", combination="No", disambiguation="Yes", embedding_model="intfloat/multilingual-e5-large-instruct"): 
    
    model = SentenceTransformer(embedding_model, trust_remote_code=True)
    
    if api_token:
        endpoint = "https://models.inference.ai.azure.com"
        model_name = "gpt-4o"
        client = OpenAI(
        base_url=endpoint,
        api_key=api_token,
    )
    else:
        raise ValueError("Please enter a valid API token.")
        
    if not sentence:
        raise ValueError("Please write a sentence.")
        
    if not mention:
        raise ValueError("Please write a mention.")
    
    if mention not in sentence:
        raise ValueError("Your mention needs to be inside the sentence.")
        
   
    # Data Normalization
    print("\nPlease Wait...\n")
    start_time = time.time()
                    
    list_with_full_names = []
    list_with_names_to_show = []
                     
    if disambiguation == "Yes":
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """
                                I will give you one or more labels within a sentence. Your task is as follows:

                                Identify each label in the sentence, and check if it is an acronym.

                                If the label is an acronym, respond with the full name of the acronym.
                                If the label is not an acronym, respond with the label exactly as it was given to you.
                                If a label contains multiple terms (e.g., 'phase and DIC microscopy'), treat each term within the label as a separate label.

                                This means you should identify and explain each part of the label individually.
                                Each part should be on its own line in the response.
                                Context-Specific Terms: If the sentence context suggests a relevant term that applies to each label (such as "study" in 'morphological, sedimentological, and stratigraphical study'), add that term to each label’s explanation.

                                Use context clues to determine the appropriate term to add (e.g., 'study' or 'microscopy').
                                Output Format: Your response should contain only the explanations, formatted as follows:

                                Each label or part of a label should be on a new line.
                                Do not include any additional text, and do not repeat the original sentence.
                                Example 1:

                                Input:

                                label: phase and DIC microscopy
                                context: Tardigrades have been extracted from samples using centrifugation with Ludox AM™ and mounted on individual microscope slides in Hoyer's medium for identification under phase and DIC microscopy.
                                Expected response:

                                phase: phase microscopy
                                DIC microscopy: Differential interference contrast microscopy
                                Example 2:

                                Input:

                                label: morphological, sedimentological, and stratigraphical study
                                context: This paper presents results of a morphological, sedimentological, and stratigraphical study of relict beach ridges formed on a prograded coastal barrier in Bream Bay, North Island New Zealand.
                                Expected response:

                                morphological: morphological study
                                sedimentological: sedimentological study
                                stratigraphical: stratigraphical study
                                IMPORTANT:

                                Each label, even if nested within another, should be treated as an individual item.
                                Each individual label or acronym should be output on a separate line.                               
                                """
                },
                {
                    "role": "user",
                    "content": f"label:{mention}, context:{sentence}"
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
                       
                        
        kati = response.choices[0].message.content.splitlines()
        
        for i in kati:
            context = i.split(":")[-1].strip()
            original_name = i.split(":")[0].strip()
            list_with_full_names.append(context)
            list_with_names_to_show.append(original_name)
                        
        name = ",".join(list_with_full_names)
    
    else:
        name = mention
        list_with_full_names.append(name)
        list_with_names_to_show.append(name)
                    
    sentence = sentence.replace(mention, name)  # Changing the mention to the correct one
                    
    response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Given a label or labels within a sentence, provide a brief description (2-3 sentences) explaining what the label represents, similar to how a Wikipedia entry would. Format your response as follows: label: description. I want only the description of the label, not the role in the context. Include the label in the description as well. For example: Sentiment analysis: Sentiment analysis is the use of natural language processing, text analysis, computational linguistics, and biometrics to systematically identify, extract, quantify, and study affective states and subjective information.\nText analysis: Text mining, text data mining (TDM) or text analytics is the process of deriving high-quality information from text. It involves the discovery by computer of new, previously unknown information, by automatically extracting information from different written resources.",
                },
                {
                    "role": "user",
                    "content": f"label:{name}, context:{sentence}"
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
                    
    z = response.choices[0].message.content.splitlines()
    
    list_with_contexts = []
    for i in z:
        context = i.split(":")[-1].strip()
        list_with_contexts.append(context)
            
    # Candidate Retrieval & Information Gathering
    async def big_main(mention, single, combination):
        mention = mention.split(",")
        for i in mention:
            await mains(i, single, combination)
        for i in mention:
            await main(i)
                        
    asyncio.run(big_main(name, single, combination))

    number = 0
    for i,j,o in zip(list_with_full_names,list_with_contexts,list_with_names_to_show):
        number += 1
        with open(f"{folder_path_1}/{i}.json", "r") as f:
            json_file = json.load(f)
            lista = []
            lista_1 = []
            for index, element in enumerate(json_file):
                qid = element.get("qid")
                link = f"https://www.wikidata.org/wiki/{qid}"
                label = element.get("label")
                description = element.get("description")
                
                label_emb = model.encode([label])
                desc_emb = model.encode([description])
                
                lista.append({link: [label_emb, desc_emb]})
    
            label_dataset_emb = model.encode([i])
            desc_dataset_emb = model.encode([j])
    
            for emb in lista:
                for k, v in emb.items():
                    cossim_label = model.similarity(label_dataset_emb, v[0][0])
                    desc_label = model.similarity(desc_dataset_emb, v[1][0])
                    emb_mean = np.mean([cossim_label, desc_label])
                    lista_1.append({k: emb_mean})
    
            sorted_data = sorted(lista_1, key=lambda x: list(x.values())[0], reverse=True)
                           
            if sorted_data:
                sorted_top = sorted_data[0]
                for k, v in sorted_top.items():
                    qid = k.split("/")[-1]
                    
                    wikidata2wikipedia = f"""
                        SELECT ?wikipedia
                        WHERE {{
                              ?wikipedia schema:about wd:{qid} .
                              ?wikipedia schema:isPartOf <https://el.wikipedia.org/> .
                        }}
                        """
                    results = get_resultss(wikidata2wikipedia)

                    for result in results["results"]["bindings"]:
                        for key, value in result.items():
                            wikipedia = urllib.parse.unquote(value.get("value", "None"))
                            
                    
                    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
                    wikidata2dbpedia = f"""
                        SELECT ?dbpedia
                        WHERE {{
                              ?dbpedia owl:sameAs <http://www.wikidata.org/entity/{qid}>.
                        }}
                        """
                    sparql.setQuery(wikidata2dbpedia)
                    sparql.setReturnFormat(JSON)
                    results = sparql.query().convert()
                    
                    for result in results["results"]["bindings"]:
                        dbpedia = result["dbpedia"]["value"]
                                        
                        print(f"The correct entity for '{o}' is:\n")    
                        print(f'Wikipedia: {wikipedia}\n')
                        print(f"Wikidata: {k}\n")
                        print(f"DBpedia: {dbpedia}\n\n\n")
            else:
                print(f"The entity: {o} is NIL.")

    end_time = time.time()
    execution_time = end_time - start_time
    ETA = time.strftime("%H:%M:%S", time.gmtime(execution_time))
    print(f"Execution Time: {ETA}")

    # i think this part can be removed now
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)
        
    for filename in os.listdir(folder_path_1):
        file_path = os.path.join(folder_path_1, filename)
        os.remove(file_path)