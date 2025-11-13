import json 

# prints the JSON file to console 
def openJson(filename: str):
    try:
        with open(f"./strategies/{filename}", "r") as file: 
            data = json.load(file)
        print(data)
    except FileNotFoundError:
        print(f"File {filename} not found.")

# returns the JSON file
def returnJson(filename: str): 
    try:
        with open(f"./strategies/{filename}", "r") as file: 
            data = json.load(file)
        return data 
    except FileNotFoundError:
        print(f"File {filename} not found.")
