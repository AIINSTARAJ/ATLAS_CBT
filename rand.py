import json

def load_question(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        question:dict = json.load(file)
    return question
    

question = load_question('questions/CSC_101.json')
question[1]