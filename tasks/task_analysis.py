from collections import Counter, defaultdict
from .models import TaskModel
import random
import spacy

nlp = spacy.load("en_core_web_md")


def analyze_title_frequencies(tasks, n):
    """
    Analyzes and counts how frequently similar beginnings of task titles occur.

    Args:
        tasks (QuerySet): A Django QuerySet of TaskModel instances to analyze.
        n (int): The number of initial words in the task title to consider for creating title parts.

    Returns:
        dict: A dictionary where keys are the first n-1 words of task titles and values are the frequencies of these beginnings.
    """
    title_parts = defaultdict(int)
    for task in tasks:
        # Extract the first n-1 words from each task title
        base_part = ' '.join(task.title.split()[:n])
        title_parts[base_part] += 1
    return title_parts


def extract_keywords(text, nlp, top_n=5):
    """
    Extract the most common keywords from the provided text.

    Args:
        text (str): The text from which to extract keywords.
        nlp (Language): The spaCy language model.
        top_n (int): Number of top keywords to return.

    Returns:
        List[str]: The list of top_n keywords.
    """
    doc = nlp(text.lower())
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]  # nouns and proper nouns
    keywords += [ent.text for ent in doc.ents]
    return [item for item, count in Counter(keywords).most_common(top_n)]  # return the (top_n) most common keywords


def generate_suggestions():
    """
        Generates task suggestions based on the analysis of completed tasks.

        Returns:
            List[str]: A list of suggestion strings based on frequently occurring title parts and keywords.
        """
    tasks = TaskModel.objects.filter(status='completed')  # only completed tasks
    title_frequencies = analyze_title_frequencies(tasks, 2)
    suggestions = []

    # Generate suggestions based on frequent title parts
    for title_part, freq in title_frequencies.items():
        if freq >= 2:  # Threshold for considering a title part frequent
            suggestions_keywords_title = ['Follow-up', 'Finalize', 'Review', 'Update', 'Maintain', 'Improve', 'Optimize', 'Deploy']
            suggestions.append(f"{random.choice(suggestions_keywords_title)} {title_part}")

    combined_text = " ".join(task.title for task in tasks)
    top_keywords = extract_keywords(combined_text, nlp, 3)  # extract top 3 keywords

    for keyword in top_keywords:
        # Generate suggestions based on common keywords
        suggestions.append(f"Consider creating a task related to -> {keyword}")

    return suggestions
