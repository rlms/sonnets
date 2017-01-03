"""
Conjugate verbs by parsing Wiktionary.
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wiktionary.org/wiki/"

def get_soup(root_form):
    """
    Return the Wiktionary page for the root form of a verb.
    """
    request = requests.get(BASE_URL + root_form)
    soup = BeautifulSoup(request.text)
    return soup

def get_text(element_list):
    """
    Find the text of a verb form from a list of candidates.
    """
    possible = element_list
    if len(possible) >= 1:
        return possible[0].text
    elif not possible:
        raise ValueError("No verb form could be found")

def plural(noun):
    """
    Find the plural of a noun.
    """
    soup = get_soup(noun)
    possible = soup.find_all(class_="form-of lang-en plural-form-of")
    if len(possible) >= 1:
        return possible[0].text
    else:
        raise ValueError("The plural of '{}' couldn't be found.".format(noun))

def conjugate(root_form, person, tense="present"):
    """
    Get a certain conjugation of a verb.

    `person` can either be 1, 2, 3 or "participle"
    `tense` can either be "present" or "past" (future tense is not yet
    supported)

    """
    soup = get_soup(root_form)
    if tense == "present":
        if person in (1, 2):
            return root_form
        elif person == 3:
            possible = soup.find_all(class_="form-of lang-en third-person-singular-form-of")
            return get_text(possible)
        elif person == "participle":
            possible = soup.find_all(class_="form-of lang-en present-participle-form-of")
            return get_text(possible)
        else:
            raise ValueError("Invalid person {}".format(person))

    elif tense == "past":
        if person in (1, 2, 3, "participle"):
            possible = soup.find_all(class_="form-of lang-en simple-past-and-participle-form-of")
            if not possible:
                if person in (1, 2, 3):
                    possible = soup.find_all(class_="form-of lang-en simple-past-form-of")
                elif person == "participle":
                    possible = soup.find_all(class_="form-of lang-en past-participle-form-of")
            return get_text(possible)
        else:
            raise ValueError("Invalid person {}".format(person))
