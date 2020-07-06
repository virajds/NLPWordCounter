import re
import os
import json
import webbrowser
#--------------------------------------------------#
# Python NLTK corpus english stopwords list is limited
#nltk.download('stopwords')
#from nltk.corpus import stopwords
#venv/bin/python3.7 -m nltk.downloader stopwords
#--------------------------------------------------#
from nltk.tokenize import RegexpTokenizer
from collections import Counter

def get_stopwords():
    # Getting stop words from file. You can add your own stop words in to this file depends on your results.
    # Original list found in https://gist.github.com/sebleier/554280/
    # The Python NLTK corpus english stopword is not covered everything.
    # Already added some words based on test results

    stopwords_file = open('stop_words.txt', 'r')
    # Push stop words from text file to an array. Stop words must be written separated by new line
    stopwords = [line.lower().strip() for line in stopwords_file.readlines()]
    stopwords_file.close()

    return stopwords

def perform_count(word_count_dict, doc_records, paragraph, words, doc_path):
    # RegEx NLP Tokanizing for words
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(paragraph)

    # Individual word count dict for all files
    file_word_count_dict = Counter()

    # Check words is passed
    if words:
        # Include only the given words
        words_list = [x.lower().strip() for x in words.split(',')]
        file_word_count_dict = Counter(w.title() for w in tokens if w.lower() in words_list)
    # Else switch to default stopwords method
    else:
        # Get stopwords
        stopwords = get_stopwords()

        # Removing stop words
        file_word_count_dict = Counter(w.title() for w in tokens if w.lower() not in stopwords)

    # Adding to the master for common results
    word_count_dict += file_word_count_dict

    #define file Name
    filename = ""
    if doc_path:
        filename = doc_path.name
    else:
        filename = "Parameter"

    # Processing current file info when it's content in the memmory
    for word_set in file_word_count_dict.items():
        try:
            # New word entry
            if word_set[0] in doc_records:
                doc_records[word_set[0]]['files'] += ", " + filename
            # Update existing word entry
            else:
                doc_records[word_set[0]] = dict()
                # sentences array
                doc_records[word_set[0]]['sentences'] = []
                # file list
                doc_records[word_set[0]]['files'] = filename
        except KeyError:
            print("Error in key: " + word_set[0])
            continue

        # Assumes all sentences ends with dots. Can improve more
        for sentence in paragraph.split('.'):
            # Using regex search for whole words other than parts of other words
            if re.compile(r'\b({0})\b'.format(word_set[0]), flags=re.IGNORECASE).search(sentence):
                str_compile = re.compile(word_set[0], re.IGNORECASE)
                doc_records[word_set[0]]['sentences'].append(
                    str_compile.sub("<strong>" + word_set[0] + "</strong>", sentence.strip()))

def save_documents(word_count_dict, doc_records):
    html = """<html>
            <head>
            <title>Word Count</title>
            </head>
            <body>
            <div align="center">
            <table width='90%' border='1' cellpadding='2'>
            <tr>
            <th width='20%'>Word (Total Occurrences)</th><th width='10%'>Documents</th><th width='70%'>Sentences containing the word</th>
            </tr>"""

    # Looping common Word count object
    for word_set in sorted(word_count_dict.items(), key=lambda pair: pair[1],
                           reverse=True):  # most_common() function didn't work properly for the joined Counter object
        doc_records[word_set[0]]['count'] = word_set[1]
        html += "<tr><td width='20%' valign='top'>" + str(word_set[0]) + "(" + str(
            word_set[1]) + ")</td><td width='10%' valign='top'>" + doc_records[word_set[0]][
                    'files'] + "</td><td width='70%'>" + "<br /><br />".join(
            doc_records[word_set[0]]['sentences']) + "</td></tr>"

    html += """</table>
                </body>
                </html>"""

    # Write HTML file
    html_file = open("WordCount.html", "w")
    html_file.write(html)
    html_file.close()

    # Convert master dict to JSON
    json_data = json.dumps(doc_records, ensure_ascii=False)

    # Write JSON file
    json_file = open("WordCount.json", "w")
    json_file.write(json_data)
    json_file.close()

    print("Please refer WordCount.html and WordCount.json files for the Results. They should be available in the same location of this Module.")

    #Open in Web browser
    try:
        webbrowser.open('file://' + os.path.realpath("WordCount.html"))
        return
    except:
        return

def count_words(path=None, words=None, paragraph=None):
    # Document Path
    path = "ExampleDocs/Test Docs/"

    #save param paragraph
    param_paragraph = paragraph

    #Common word count dict for all files
    word_count_dict = Counter()
    # Words' data master dict.
    # Not suitable for large amount files processing or heavy files.
    # Better switch to DB or cache methods for them.
    doc_records = dict()

    #If paragraph passed as Var
    if paragraph:
        perform_count(word_count_dict, doc_records, paragraph, words, None)
    else:
        #Open file in dir
        with os.scandir(path) as docs_obj:
            for doc_path in docs_obj:
                #Looping text files only
                if doc_path.name.endswith(".txt") and doc_path.is_file():

                    text_file = open(doc_path.path)

                    paragraph = text_file.read()# Use this to read file content as a stream:

                    perform_count(word_count_dict, doc_records, paragraph, words, doc_path)

                    text_file.close()

    #return objects - test Mode
    if param_paragraph:
        return sorted(word_count_dict.items(), key=lambda pair: pair[1], reverse=True)
    #File p[ath mode - Save HTML and JSON files
    else:
        # Save HTML and JSON output file
        save_documents(word_count_dict, doc_records)