import csv
import random

# Create empty lists
wood_data = []

# Read data from CSV file
with open('Wood sizes.csv', encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wood_data.append(row)

# Define a function to choose random size
def choose_random_size(material):
    valid_sizes = [(row[f'{material} width'], row[f'{material} length']) for row in wood_data if row[f'{material} width'] and row[f'{material} length']]
    return random.choice(valid_sizes) if valid_sizes else None

def size():
   while True:
       # Ask the user to choose a type of wood
       wood_type = input("Enter the type of wood (Vuren or Grenen): ")

       if wood_type not in ['Vuren', 'Grenen']:
        print("Invalid wood type. Please choose between Vuren or Grenen.")
        continue

       # Get a random size for the chosen wood type
       chosen_size = choose_random_size(wood_type)

       if chosen_size:
           width, length = chosen_size
           print(f'Random size for {wood_type}: {width}x{length}mm')
           print (length)
           break
       else:
           print(f'No valid sizes found for {wood_type}.')
    
   return width, length
