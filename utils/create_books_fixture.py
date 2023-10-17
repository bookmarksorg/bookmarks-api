import csv
import json
import random
import ast  # Required to safely evaluate string representation of a list

# Open and read the CSV file with selected columns
with open('top_500_books_selected_columns.csv', mode='r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file)

    # Create a list to hold the JSON data
    json_data = []

    # Iterate through the rows and convert them to JSON
    for row in reader:
        if row['isbn'] == '9999999999999':
            # random isbn with 13 numbers
            row['isbn'] = str(random.randint(1000000000000, 9999999999999))
            
        json_data.append({
            'model': 'bookmarks.book',  # Replace with your app name and model name
            'pk': row['isbn'], 
            'fields': {
                'title': row['title'],
                'author': row['author'],
                'blurb': row['description'],
                'language': row['language'],
                # 'isbn': row['isbn'],
                # 'genres': genres,
                'number_pages': row['pages'],
                'cover': row['coverImg'],
            }
        })

# Save the JSON data to a fixture file
with open('books_fixture.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("JSON fixture file 'books_fixture.json' created.")