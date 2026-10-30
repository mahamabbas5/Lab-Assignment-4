
import re
from collections import Counter


def summarize_text(text, max_sentences=5):

    # Split article into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 30
    ]

    if not sentences:
        return "No summary available."

    # Common words to ignore
    stop_words = {
        "the", "is", "are", "was", "were", "a", "an",
        "and", "or", "but", "in", "on", "at", "to",
        "of", "for", "with", "by", "from", "as", "it",
        "this", "that", "these", "those", "be", "has",
        "have", "had", "will", "would", "can", "could"
    }

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    filtered_words = [
        word for word in words if word not in stop_words
    ]

    word_frequency = Counter(filtered_words)

    sentence_scores = {}

    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b', sentence.lower()
        )

        score = sum(
            word_frequency[word]
            for word in sentence_words
            if word not in stop_words
        )

        sentence_scores[index] = score

    # Select highest scoring sentences
    important_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:max_sentences]

    # Restore original article order
    important_sentences.sort()

    summary = " ".join(
        sentences[index]
        for index in important_sentences
    )

    return summary
