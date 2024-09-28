import re
import pandas as pd
import Levenshtein

class BKTree:
    def __init__(self, distance_fn):
        self.distance_fn = distance_fn
        self.tree = None

    def add(self, term):
        node = (term, {})
        if self.tree is None:
            self.tree = node
        else:
            self._add(self.tree, node)

    def _add(self, parent, node):
        parent_term, children = parent
        term, _ = node
        distance = self.distance_fn(parent_term, term)
        if distance in children:
            self._add(children[distance], node)
        else:
            children[distance] = node

    def find(self, term, max_distance):
        if self.tree is None:
            return []

        candidates = [self.tree]
        found = []

        while candidates:
            candidate, children = candidates.pop()
            distance = self.distance_fn(term, candidate)
            if distance <= max_distance:
                found.append((candidate, distance))

            candidates.extend(child for d, child in children.items()
                              if distance - max_distance <= d <= distance + max_distance)

        return found

def levenshtein_distance(term1, term2):
    distance = Levenshtein.distance(term1, term2)
    if distance >= 10:
        return 1
    return distance / 10

def build_bk_tree(valid_tokens):
    tree = BKTree(levenshtein_distance)
    for token in valid_tokens:
        tree.add(token)
    return tree

def load_frequency_dict(filepath):
    frequency_df = pd.read_csv(filepath)
    frequency_dict = dict(zip(frequency_df['Token'], frequency_df['Frequency']))
    return frequency_dict

def tokenize_persian(text):
    tokens = re.findall(r'\w+', text)
    return tokens

def get_closest_token_bktree(token, bk_tree, frequency_dict, max_frequency, threshold):
    candidates = bk_tree.find(token, threshold)
    closest_token = token
    max_score = 0
    
    for candidate, dist in candidates:
        frequency_score = frequency_dict.get(candidate, 0) / max_frequency
         
        combined_score = ((1 - dist) + (frequency_score / 4)) / 2
        
        if combined_score > max_score:
            max_score = combined_score
            closest_token = candidate

    return closest_token

def correct_spelling(query, frequency_dict, bk_tree):
    tokens = tokenize_persian(query)
    corrected_tokens = []
            
    for token in tokens:
        closest_token = get_closest_token_bktree(token, bk_tree, frequency_dict, max(frequency_dict.values()), threshold=0.3)
        corrected_tokens.append(closest_token)
    
    corrected_query = ' '.join(corrected_tokens)
    return corrected_query


def get_corrected_response(query):
    frequency_dict = load_frequency_dict('frequency_combined.csv')
    valid_tokens = list(frequency_dict.keys())
    bk_tree = build_bk_tree(valid_tokens)
    return correct_spelling(query, frequency_dict, bk_tree)

print(get_corrected_response('سلاامممممم'))