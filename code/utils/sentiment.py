from senti_classifier import senti_classifier
import nltk
import csv
sentences = ['The movie was the worst movie', 'It was the worst acting by the actors']
pos_score, neg_score = senti_classifier.polarity_scores(sentences)
print pos_score, neg_score
path_to_scene_csv = "../../ds113_study_description/stimulus/task001/annotations/german_audio_description.csv"

def translate_file(filename):
  with open(filename, 'rt') as csvfile:
    reader = csv.DictReader(
        csvfile,
        fieldnames=['start', 'end', 'german-desc'])
    for row in reader:
        print row

def get_sentiment(phrase):
    print senti_classifier.polarity_scores(phrase)

get_sentiment(["hello you are ugly and i hate you", "hello you are beautiful and i love you"])
