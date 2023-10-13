import csv

# Open and read the input CSV file
with open('books.csv', mode='r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file)

    # Sort the rows by the 'numRatings' column in descending order
    sorted_rows = sorted(reader, key=lambda row: int(row['numRatings']), reverse=True)

# Select the top 500 rows
top_500_rows = sorted_rows[:500]

# Define the headers for the new CSV file
new_headers = ['title', 'author', 'description', 'language', 'isbn', 'genres', 'pages', 'firstPublishDate', 'coverImg']

# Write the selected columns of the top 500 rows to a new CSV file
with open('top_500_books_selected_columns.csv', mode='w', encoding='utf-8', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=new_headers)
    writer.writeheader()
    for row in top_500_rows:
        selected_data = {key: row[key] for key in new_headers}
        writer.writerow(selected_data)

print("Selected columns from top 500 rows saved to 'top_500_books_selected_columns.csv'")