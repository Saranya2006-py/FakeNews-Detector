clickbait_words = [
"shocking",
"secret",
"unbelievable",
"breaking",
"you won't believe",
"exposed",
"miracle"
]

def detect_clickbait(text):

    score = 0

    for word in clickbait_words:
        if word in text.lower():
            score += 1

    return score