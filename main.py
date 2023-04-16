import openai
import csv
import os
import dotenv


# Set up your OpenAI API credentials
dotenv.load_dotenv()
openai.api_key = os.getenv('API_KEY')


# Function that will rate each review
def rate_review(review_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"Rate this customer review from 1 to 10, where 1 is extremely negative and 10 is very positive:\n\n{review_text}\n\nRating:"),
        temperature=0.5,
        max_tokens=1,
        n=1,
        stop=None,
        timeout=15,
    )
    rating = response
    return rating


# Set the directory and filename for the input CSV file
dir_path = os.getenv('DIR')
file_name = "customer_reviews.csv"

# Read in the reviews from the input CSV file
with open(os.path.join(dir_path, file_name), 'r') as f:
    reader = csv.DictReader(f)
    rows = []
    for row in reader:
        rows.append(row)

# Rate each review and add the rating to the CSV file
for row in rows:
    rating = rate_review(row['review text'])
    row['rate'] = rating

# Sort the reviews by rating
rows_sorted = sorted(rows, key=lambda x: int(x['rate']), reverse=True)

# Set the filename for the output CSV file
output_file_name = f"{os.path.splitext(file_name)[0]}_analyzed.csv"

# Write the updated CSV file with ratings and sorting
with open(os.path.join(dir_path, output_file_name), 'w') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows_sorted)










