import nltk 
from nltk.corpus import stopwords
from rake_nltk import Rake
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import string
nltk.download('stopwords')


# functions

# initialize the stopwords
def init_nltk():
    nltk.download('stopwords')
def get_stopwords(language):
    stops = stopwords.words(language)
    return stops

# Initialize RAKE while excluding repeated phrases
# We inititialize punctuations so RAKE will not read them from the text
def init_rake(stopwords_list, punct):
    rake = Rake(include_repeated_phrases=False
            ,min_length=1, max_length=3
            ,stopwords=stopwords_list,
            punctuations=punct)
    return rake

# Get user input for the URL
def get_url():
    return input("Enter the URL for the webpage:")


# Send request to that URL to access the text
# Use Beatiful Soup to scrape the text and store it in a variable. 
# List Comprehension: Shorter syntax for adding items to new list from old list
def scrap_text(url):    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    headings = [h.get_text() for h in soup.find_all(['h1','h2','h3','h4','h5','h6'])]
    article_text = ' '.join(headings + paragraphs)
    return article_text

# Convert it to a text blob so we can loop through the words
def text_blobification(text):
    return TextBlob(text)

# Loop through each of the words in soup_blob to see if any of them are stopwords
# If they are, they are removed from the text blob. This is how we get our keywords
def filter_words(article_blob, stopwords_list):
    filtered_words = []
    stops = stopwords_list
    filtered_words = [words.lower() for words in article_blob.words
                       if words.lower() not in stops]
    return ' '.join(filtered_words) 
   # This is the normal form of the code above
    #   for word in article_blob.words:
    #    if word.lower() not in stops:
     #       filtered_words.append(word.lower())

# This is where I implemented RAKE:
    # RAKE extracts the keywords from the candidate list
      # Then it ranks them  
def extract_keywords(rake_obj, filtered_text):
    rake_obj.extract_keywords_from_text(filtered_text)
    return rake_obj.get_ranked_phrases()

# This asks the user for the name of the file they want use
# It makes that file and writes each keyword in article_blob to it
# This can then be accessed by the user.
def print_keyword_file(phrases):
    file_name = "keywords.txt"
    key_file = open(file_name, 'w')
    for word in phrases:
        key_file.write(word)
        key_file.write('\n')
    print("Keywords have been extracted to ", file_name)

# The actual program where all the functions come together
def main():
    init_nltk()
    language = input('Enter a language: ')
    stops = get_stopwords(language)
    punctuation = string.punctuation
    rake = init_rake(stops, punctuation)

    url = get_url()
    article_txt = scrap_text(url)
    article_blob = text_blobification(article_txt)

    filtered_text = filter_words(article_blob, stops)
    keywords = extract_keywords(rake, filtered_text)
    phrases = [phrase.strip() for phrase in keywords]

    print_keyword_file(phrases)

main()