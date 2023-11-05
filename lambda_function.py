import json
import re

'''
This file is for hosting the service on AWS Lambda Serverless 
Upload code_keyword_map.json and code_keyword_pretty.json to the Lambda function 
And then copy paste the code below into the Lambda function editor
'''

with open('code_keyword_map.json', 'r') as file:
    code_keyword_map = json.load(file)
    
with open('code_keyword_pretty.json', 'r') as file:
    data_dict = json.load(file)
    
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
    patterns = ["hs", "code"]
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

def find_keywords(top5):
    keywords = {}
    for code in top5.keys():
        keywords[code] = data_dict[code]
    return keywords

def lambda_handler(event, context):
    print(event)
    description = event['queryStringParameters']['description']
    top5 = find_alternate_code(description, code_keyword_map)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'top5': top5,
            'keywords': find_keywords(top5)
        })
    }
