import pytest
import json
from build_sentences import (
    get_seven_letter_word, 
    parse_json_from_file, 
    choose_sentence_structure,
    get_pronoun, 
    get_article, 
    get_word, 
    fix_agreement, 
    build_sentence, 
    structures, 
    pronouns,
    articles
)


# It's convenient to have a fixture ready for JSON data that's used repeatedly in tests.
@pytest.fixture
def sample_data():
    """ Fixture to provide sample data for testing. """
    return {
        "adjectives": ["able", "bad", "best", "better"],
        "nouns": ["apple", "ball", "cat", "dog"],
        "verbs": ["act", "bring", "come", "do"],
        "adverbs": ["ably", "badly", "best", "better"],
        "prepositions": ["about", "above", "across", "after"]
    }

def test_get_seven_letter_word(mocker):
    mocker.patch("builtins.input", return_value="testing")
    assert get_seven_letter_word() == "TESTING"

    mocker.patch("builtins.input", return_value="short")
    with pytest.raises(ValueError):
        get_seven_letter_word()

def test_parse_json_from_file(tmp_path):
    test_data = {"key": "value"}
    file_path = tmp_path / "test.json"
    with open(file_path, 'w') as f:
        json.dump(test_data, f)
    assert parse_json_from_file(file_path) == test_data

def test_choose_sentence_structure(mocker):
    mocker.patch("random.choice", return_value=structures[0])
    assert choose_sentence_structure() == structures[0]

def test_get_pronoun(mocker):
    mocker.patch("random.choice", return_value="they")
    assert get_pronoun() == "they"

def test_get_article(mocker):
    mocker.patch("random.choice", return_value="a")
    assert get_article() == "a"

def test_get_word(sample_data):
    assert get_word("A", sample_data["nouns"]) == "apple"
    assert get_word("C", sample_data["verbs"]) == "come"

def test_fix_agreement():
    """
    Test for side effects (direct modification of a list).
    Check the three rules (he/she, a/an, the).
    """
    # Rule 1: A verb following 'he'/'she' should end with 's'
    sentence1 = ["he", "quickly", "run", "to", "the", "store"]
    fix_agreement(sentence1)
    assert sentence1 == ["he", "quickly", "runs", "to", "the", "store"]
    
    # Rule 2: 'a' should become 'an' before a vowel
    sentence2 = ["a", "red", "apple", "is", "on", "the", "table"]
    fix_agreement(sentence2)
    assert sentence2 == ["an", "red", "apple", "is", "on", "the", "table"]
    
    # Rule 3: A verb following 'the' at the beginning of a sentence should end with 's'
    sentence3 = ["the", "big", "dog", "quickly", "run", "away"]
    fix_agreement(sentence3)
    assert sentence3 == ["the", "big", "dog", "quickly", "runs", "away"]

def test_build_sentence(mocker, sample_data):
    """
    Test for a function that combines multiple other functions.
    Mock random parts to return fixed values, ensuring the final output is correct.
    """
    mocker.patch("build_sentences.get_pronoun", return_value="she")
    mocker.patch("build_sentences.get_article", return_value="a")
    
    seed_word = "ABCDEFG"
    structure = ["PRO", "ADV", "VERB", "ART", "ADJ", "NOUN"]
    expected_words = [
        "she",
        sample_data["adverbs"][0],  # "ably
        sample_data["verbs"][1] + "s",  # "brings"
        "a",   
        sample_data["adjectives"][2],  # "best"
        sample_data["nouns"][3]  # "dog" 
    ]

    expected_sentence = " ".join(expected_words).capitalize()
    result = build_sentence(seed_word, structure, sample_data)
    assert result == expected_sentence
