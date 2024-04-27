import nltk 
from nltk.corpus import stopwords
from rake_nltk import Rake
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import string
nltk.download('stopwords')

# initialize the stopwords
stops = stopwords.words('english')

# Explain
punct = string.punctuation

# Initialize RAKE while excluding repeated phrases
rake = Rake(include_repeated_phrases=False
            ,min_length=1, max_length=3
            ,stopwords=stops,
            punctuations=punct)


# This asks the user for the name of the file they want use
# It makes that file and writes each keyword in article_blob to it
# This can then be accessed by the user.
def print_keyword_file(keywords):
    file_name = "keywords.txt"
    key_file = open(file_name, 'w')
    for word in keywords:
        key_file.write(word)
        key_file.write('\n')
    print("Keywords have been extracted to ", file_name)
# Get user input for the URL, then send request to that URL to access the text
# Use Beatiful Soup to scrape the text and store it in a variable. 
text = input("Enter the URL for the webpage:")
r = requests.get(text)
soup = BeautifulSoup(r.text, "html.parser")

# Explain
# List Comprehension
paragraphs = [p.get_text() for p in soup.find_all('p')]
headings = [h.get_text() for h in soup.find_all(['h1','h2','h3','h4','h5','h6'])]
article_text = ' '.join(headings + paragraphs)


# Convert it to a text blob so we can loop through the words
article_blob = TextBlob(article_text)

# TEST
#t = input("Enter a string:")
#rake.extract_keywords_from_text(t)
#keywords = rake.get_ranked_phrases()
#print(keywords)
 
# Loop through each of the words in soup_blob to see if any of them are stopwords
# If they are, they are removed from the text blob. This is how we get our keywords
def filter_words(article_blob):
    filtered_words = []
    for word in article_blob.words:
        if word.lower() not in stops:
            filtered_words.append(word.lower())
    filtered_text = ' '.join(filtered_words) 

    rake.extract_keywords_from_text(filtered_text)

    keywords = rake.get_ranked_phrases()

    phrases = [phrase.strip() for phrase in keywords]

    print(phrases)

    print_keyword_file(phrases)

#print_keyword_file(keywords)
