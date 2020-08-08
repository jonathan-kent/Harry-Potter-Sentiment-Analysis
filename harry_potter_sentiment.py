import math
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_book(title):
    file = open(title)
    text = "".join(file.readlines())
    file.close()
    # remove page numbers
    text = re.sub("Page \| .*\n", "", text)
    text = re.sub("P a g e \| .*\n", "", text)
    # remove line breaks
    text = re.sub(" \n", " ", text)
    text = re.sub("\n{2,}", "\n", text)
    paragraphs = text.split("\n")
    revised = []
    for paragraph in paragraphs:
        # ignore empty line paragraphs
        if paragraph == "\n":
            print(paragraph)
            pass
        # dialogue paragraphs added without parsing
        elif "\"" in paragraph:
            revised.append(paragraph)
        else:
            # filter out periods that don't end sentences
            paragraph = paragraph.replace("Mr.", "Mr<>")
            paragraph = paragraph.replace("Mrs.", "Mrs<>")
            paragraph = paragraph.replace("...", "%%%")
            #split paragraph into sentences
            for i in range(0, len(paragraph)):
                if paragraph[i] == "!" or paragraph[i] == "?" or paragraph[i] == ".":
                    paragraph = paragraph[:i+1] + "***" + paragraph[i+1:]
            paragraph = paragraph.replace("Mr<>", "Mr.")
            paragraph = paragraph.replace("Mrs<>", "Mrs.")
            paragraph = paragraph.replace("%%%", "...")
            sentences = paragraph.split("*** ")
            for sentence in sentences:
                revised.append(sentence)
    return revised


def get_chapters(book):
    n = 0
    for sentence in book:
        if "CHAPTER" in sentence:
            n += 1
    chapters = [[] for _ in range(n)]
    i = -1
    for sentence in book:
        if "CHAPTER" in sentence:
            i += 1
        if i < 0:
            pass
        else:
            chapters[i].append(sentence)
    return chapters


def get_part_sentiments(chapters):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = [[] for _ in range(len(chapters))]
    for i, chapter in enumerate(chapters):
        parts = [[],[],[],[]]
        part_length = math.ceil(len(chapter)/4)
        avg_sent = 0
        sentences = 0
        for idx, sentence in enumerate(chapter):
            if idx % part_length == 0:
                avg_sent = 0
                sentences = 0
            sentiment = get_sentiment(analyzer, sentence)
            if sentiment != 0:
                sentences += 1
                avg_sent += sentiment
                parts[math.floor(idx / part_length)] = avg_sent / sentences
        sentiments[i] = parts
    return sentiments

def get_chapter_sentiments(chapters):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for chapter in chapters:
        avg_sent = 0
        sentences = 0
        for sentence in chapter:
            sentiment = get_sentiment(analyzer, sentence)
            if sentiment !=0:
                sentences += 1
                avg_sent += sentiment
        sentiments.append(avg_sent / sentences)
    return sentiments


def get_sentiment(analyzer, string):
    sentiment = analyzer.polarity_scores(string)['compound']
    return sentiment


def plot_data_parts(sentiments):
    x = []
    y = []
    parts = 0
    for chp in sentiments:
        for part in chp:
          x.append(parts/4)
          parts += 1
          y.append(part)
    plt.plot(x, y)
    plt.ylabel('Sentiment') 
    plt.title("Harry Potter and the Prisoner of Azkaban")  
    plt.show()

def plot_data_chaps(sentiments):
    x = []
    y = []
    chaps = 0
    for s in sentiments:
          x.append(chaps)
          chaps += 1
          y.append(s)
    plt.plot(x, y)
    plt.ylabel('Sentiment') 
    plt.title("Harry Potter and the Prisoner of Azkaban")  
    plt.show()

def plot_data_series(series):
    y = []
    for book in series:
        for chap in book:
            y.append(chap)
        # gap size between books
        for i in range(10):
            y.append(99)
    y = np.ma.array(y)
    y = np.ma.masked_where(y > 5 , y)

    plt.annotate("Diagon Alley", (3, 0.14), size=8)
    plt.annotate("The Forbidden Forest", (12, -0.13), size=8)
    plt.annotate("Dobby's Warning", (26, -0.1), size=8)
    plt.annotate("At Flourish and Blotts", (27, 0.12), size=8)
    plt.annotate("Cat, Rat, and Dog", (70, -0.17), size=8)
    plt.annotate("Owl Post Again", (74, 0.165), size=8)
    plt.annotate("Beauxbatons and Durmstrang", (101, 0.20), size=8)
    plt.annotate("Flesh, Blood, and Bone", (117, -0.28), size=8)
    plt.annotate("Hogawarts High Inquisitor", (146, 0.11), size=8)
    plt.annotate("The Only One He Ever Feared", (167, -0.24), size=8)
    plt.annotate("The Half-Blood Prince", (188, 0.215), size=8)
    plt.annotate("Flight of the Prince", (207, -0.36), size=8)
    plt.annotate("The Seven Potters", (222, -0.2), size=8)
    plt.annotate("Epilogue", (253, 0.21), size=8)

    plt.plot([-10,280],[0,0], color='black', linewidth=0.5)
    plt.plot(y, color='red')
    plt.ylabel('Sentiment') 
    plt.title("Harry Potter Sentiment Over Series")
    plt.xlim([-10,270])
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    fig = mpl.pyplot.gcf()
    fig.set_size_inches(18, 8)
    plt.show()


def main():
    series = [[],[],[],[],[],[],[]]
    for i in range(1,8):
        book = get_book("book"+str(i)+".txt")
        chapters = get_chapters(book)
        sentiments = get_chapter_sentiments(chapters)
        series[i-1] = sentiments
    plot_data_series(series)
    
            


if __name__ == "__main__":
    main()

