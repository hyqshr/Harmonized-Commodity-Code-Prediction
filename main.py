from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yake
import json
import re

kw_extractor = yake.KeywordExtractor()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)

with open('code_keyword_map.json', 'r') as file:
    code_keyword_map = json.load(file)
    
def jaccard_similarity(sentence1, sentence2):
    # Tokenize the sentences into words
    set1 = set(sentence1.split())
    set2 = set(sentence2.split())

    # Calculate intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # Compute Jaccard similarity
    jaccard = len(intersection) / len(union)

    return jaccard
def clean(input_str):
    # Remove all numbers
    input_str = input_str.lower()
    input_str = re.sub(r'\d+', '', input_str)

    # Remove specific substrings
    patterns = ["hs", "h\.s\.", "code"]
    for pattern in patterns:
        input_str = re.sub(pattern, '', input_str, flags=re.IGNORECASE)

    # Return the modified string
    return input_str.strip()

def find_alternate_code(description, code_keyword_map):
    alternate = {}
    
    # Loop through each code and its associated keyword list
    for code, keyword_list in code_keyword_map.items():
        similarity = jaccard_similarity(clean(description), " ".join(keyword_list))
        
        # If there's some similarity, add to the alternate dictionary
        if similarity > 0:
            alternate[code] = similarity

    # Sort the alternate dictionary by similarity scores in descending order and take the top 5
    sorted_alternate = dict(sorted(alternate.items(), key=lambda item: item[1], reverse=True)[:5])

    return sorted_alternate

@app.get('/hs_code')
async def get_code(description: str):
    if not description:
        raise HTTPException(status_code=400, detail="Description must be provided")
    
    alternate_codes = find_alternate_code(description, code_keyword_map)
    
    return {"result": alternate_codes}