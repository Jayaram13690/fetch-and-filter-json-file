import json


def load_data(data):
    print("Default Data:")
    for person in data:
        print(f"ID: {person['id']}")
        print(f"Name: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"City: {person['city']}")
        print("------------")

with open('data.json', 'r') as file:
    data = json.load(file) #loads the json file data to python list.
    
    load_data(data)

if isinstance(data, list):
    filtered_data = []
    
    for person in data:
        if person['city'] == 'Hyderabad':
            filtered_data.append(person)
            
    print("Filtered Results:\n")

    for person in filtered_data:
        print(f"ID: {person['id']}")
        print(f"Name: {person['name']}")
        print(f"Age: {person['age']}")
        print(f"City: {person['city']}")
        print("------------")
else:
    print("Json File not found!!")