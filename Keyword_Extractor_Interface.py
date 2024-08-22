import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import string
from KeyWord_Extractor import init_nltk, get_stopwords, init_rake, get_url, print_keyword_file, scrap_text, text_blobification, filter_words, extract_keywords, print_keyword_file

def main():
    init_nltk()
    # Define layout of the the interface
    layout = [
        [sg.Text('Enter a language: ')],
        [sg.Input(key='language')],
        [sg.Text('Enter a URL:')],
        [sg.Input(key='-URL-')],
        [sg.Button('Submit')],
        [sg.Text(size=(50,10), key='-OUTPUT-')],
    ]
    
    window = sg.Window('Keyword Extractor', layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Submit':
            language = values['language']
            url = values['-URL-']
            stops = get_stopwords(language)
            punctuation = string.punctuation
            rake = init_rake(stops, punctuation)
            article_txt = scrap_text(url)
            article_blob = text_blobification(article_txt)
            filtered_text = filter_words(article_blob, stops)
            keywords = extract_keywords(rake, filtered_text)
            phrases = [phrase.strip() for phrase in keywords]
            print_keyword_file(phrases)
    window.close()
    
if __name__ == "__main__":
    main()