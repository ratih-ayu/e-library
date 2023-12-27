import csv
from faker import Faker
import random
from datetime import timedelta

# Create Faker instance for generating dummy data with Indonesian address and phone number
fake = Faker('id_ID')

# Generate dummy data for the 'genre' table
genres = ['Action', 'Adventure', 'Sci-Fi', 'Mystery', 'Romance']
genre_data = [(genre, i + 1) for i, genre in enumerate(genres)]

# Generate dummy data for the 'location_info' table with Indonesian locations and addresses
locations = [(i + 1, fake.city(), fake.address()) for i in range(5)]

# Generate dummy data for the 'user_info' table with Indonesian names, addresses, and phone numbers
user_data = [(i + 1, fake.name(), fake.phone_number()[:13], fake.email(), 
              fake.date_time_this_decade()) for i in range(100)]

# Generate dummy data for the 'books' table with updated location_id
book_data = [
    (i + 1, fake.text(max_nb_chars=50), fake.name(), 
     random.randint(1, len(genres)), random.randint(1, 5), random.randint(1, 5))
    for i in range(200)
]

# Generate dummy data for the 'loan_book' table with loan_due_date and various statuses
loan_book_data = []

# Dictionary to track the number of books loaned by each user
user_loan_count = {}

# Function to check if a user can loan another book
def can_loan_more_books(user_id):
    return user_loan_count.get(user_id, 0) < 2

# Generate dummy data for the 'loan_book' table with loan_due_date and various statuses
for i in range(50):
    user_id = random.randint(1, 100)
    book_id = random.randint(1, 200)
    
    # Check if the user can loan another book
    if can_loan_more_books(user_id):
        loan_status = random.choice(['On Loan', 'Returned', 'Overdue'])
        
        # Update the user's loan count
        user_loan_count[user_id] = user_loan_count.get(user_id, 0) + 1
        
        loan_book_data.append([
            i + 1,
            fake.date_time_between(start_date='-30d', end_date='now', tzinfo=None).date(),
            None,  # No return_date initially
            user_id, book_id, loan_status,
            None  # No loan_due_date initially
        ])

# Calculate loan_due_date as 14 days from loan_date
for entry in loan_book_data:
    entry[-1] = entry[1] + timedelta(days=14)

# Calculate return_date based on loan status
for entry in loan_book_data:
    if entry[5] in ['Returned', 'Overdue']:
        entry[2] = fake.date_time_between(start_date=entry[1], end_date='now', tzinfo=None).date()

# Generate dummy data for the 'loan_queue' table
loan_queue_data = [
    (i + 1, random.randint(1, 100), random.randint(1, 200),
     fake.date_time_between(start_date='-30d', end_date='now', tzinfo=None).date(),
     fake.date_time_between(start_date='now', end_date='+30d', tzinfo=None).date(),
     'In Queue')
    for i in range(30)
]

# Export data to CSV files
def export_to_csv(data, filename, header):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(data)

# Order for 'genre.csv': genre_name, genre_id
export_to_csv(genre_data, 'genre.csv', ['genre_name', 'genre_id'])

# Order for 'location_info.csv': location_id, location_name, location_address
export_to_csv(locations, 'location_info.csv', ['location_id', 'location_name', 'location_address'])

# Order for 'user_info.csv': user_id, user_name, phone_number, email, date_register
export_to_csv(user_data, 'user_info.csv', ['user_id', 'user_name', 'phone_number', 'email', 'date_register'])

# Order for 'books.csv': book_id, title, author, quantity, genre_id, location_id
export_to_csv(book_data, 'books.csv', ['book_id', 'title', 'author', 'quantity', 'genre_id', 'location_id'])

# Order for 'loan_book.csv': loan_id, loan_date, return_date, user_id, book_id, loan_status, loan_due_date
export_to_csv(loan_book_data, 'loan_book.csv', ['loan_id', 'loan_date', 'return_date', 'user_id', 'book_id', 'loan_status', 'loan_due_date'])

# Order for 'loan_queue.csv': queue_id, user_id, book_id, queue_start_date, queue_end_date, queue_status
export_to_csv(loan_queue_data, 'loan_queue.csv', ['queue_id', 'user_id', 'book_id', 'queue_start_date', 'queue_end_date', 'queue_status'])
