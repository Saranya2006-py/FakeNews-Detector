def source_score(url):

    trusted_sources = [
        "bbc",
        "reuters",
        "cnn",
        "nytimes",
        "theguardian"
    ]

    suspicious_sources = [
        "unknown",
        "blogspot",
        "wordpress"
    ]

    score = 50

    for source in trusted_sources:
        if source in url:
            score = 90

    for source in suspicious_sources:
        if source in url:
            score = 20

    return score