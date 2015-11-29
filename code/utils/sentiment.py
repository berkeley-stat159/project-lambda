import nltk
import csv
from textblob import TextBlob

path_to_scene_csv = "../../ds113_study_description/stimulus/task001/annotations/german_audio_description.csv"

def get_polarity_dict(filename):
  with open(filename, 'rt') as csvfile:
    reader = csv.DictReader(
        csvfile,
        fieldnames=['start', 'end', 'german_desc'])
    for row in reader:
        start = float(row['start'])
        end = float(row['end'])
        blob = TextBlob(row['german_desc'])
        translated_blob = blob.translate(to="en")
        sentiment = get_sentiment(blob)
        print sentiment

def get_sentiment(blob):
    sentences = blob.sentences
    sentence_total = len(sentences)
    sentiment_total = 0
    for sentence in sentences:
        sentiment_total += sentence.sentiment.polarity
    return float(sentiment_total) / float(sentence_total)



# get_polarity_dict(path_to_scene_csv)

# phrase = "Eine Computeranimation: Auf einen schroffen Berg mit schneebedeckter Flanke fliegt eine Reihe Sterne zu. Sie bilden einen Kranz um den Gipfel: 'Paramount'."
phrase = "you are ugly"


blob = TextBlob(phrase)
print blob.tags
print blob.noun_phrases
for sentence in blob.sentences:
    print(sentence.sentiment.polarity)

print blob.translate(to="en")

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)
