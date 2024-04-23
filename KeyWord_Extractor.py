import nltk 
from nltk.corpus import stopwords
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
nltk.download('stopwords')

# initialize the stopwords
stops = stopwords.words('english')

# Get user input for the URL, then send request to that URL to access the text
# Use Beatiful Soup to scrape the text and store it in a variable. 
text = input("Enter the URL for the webpage:")
r = requests.get(text)
soup = BeautifulSoup(r.text, "html.parser")
print(soup.text)

# Convert it to text blob so we can loop through the words
soup_blob = TextBlob(soup.text)

# Loop through each of the words in soup_blob to see if any of them are stopwords
# If they are, they are removed from the text blob. This is how we get our keywords
for word in soup_blob.words:
    if word in stops:
         soup_blob.words.remove(word)

# This asks the user for the name of the file they want use
# It makes that file and writes each keyword in soup_blob to it
# This can then be accessed by the user.
file_name = input("Enter the desired name for the file; have .txt at the end too:")
key_file = open(file_name, 'w')
nl = "\n"
for word in soup_blob.words:
    key_file.write(word)
    key_file.write(nl)