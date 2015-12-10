import csv
import textblob as tb
from math import ceil, floor
import unicodedata

path_to_scene_csv = "../../ds113_study_description/stimulus/task001/annotations/german_audio_description.csv"


def get_polarity_dict(filename):
    polarity_dict = {}
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=['start', 'end', 'german_desc'])
        for row in reader:
            start = ceil(float(row['start']))
            end = floor(float(row['end']))
            desc = row['german_desc']
            desc = unicode(desc, "utf-8")
            desc = unicodedata.normalize('NFKD', desc).encode('ascii', 'ignore')
            blob = tb.TextBlob(desc)
            try:
                translated_blob = blob.translate(from_lang="de", to="en")
            except tb.exceptions.NotTranslated:
                pass
            sentiment = get_sentiment(translated_blob)
            polarity_dict[(start, end)] = sentiment
    print(polarity_dict)
    return polarity_dict


def get_sentiment(blob):
    sentences = blob.sentences
    sentence_total = len(sentences)
    sentiment_total = 0
    for sentence in sentences:
        sentiment_total += sentence.sentiment.polarity
    return float(sentiment_total) / float(sentence_total)


get_polarity_dict(path_to_scene_csv)
