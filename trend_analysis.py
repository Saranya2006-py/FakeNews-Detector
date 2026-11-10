from collections import Counter

def top_words(text):

    words = text.lower().split()

    common = Counter(words).most_common(5)

    return common