import asyncio
import aiohttp
import os
import re
from nltk.tokenize import word_tokenize
from pystempel import Stemmer
from semeval_test import fetch_keywords_async,get_keywords_results, extract_keywords


# Otherwise the load sequence is broken
def natural_sort_key(filename):
    """Extract numerical value from filename for sorting."""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', filename)]


def stem_words_polish(word_list, stemmer):
    # Stem the words
    stemmed_words = [stemmer(word) for word in word_list]

    return stemmed_words


def load_txt_files_to_list(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    files_sorted = sorted(files, key=natural_sort_key)  # Sort using numerical values

    text_list = []
    for filename in files_sorted:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            text_list.append(file.read())  # Append file content to list
    print("\n")
    return text_list


def load_key_files_to_sublists(folder_path):
    key_files_list = []

    # Check if folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Error: The folder '{folder_path}' does not exist.")

    # Get a sorted list of .key files
    key_files = [f for f in os.listdir(folder_path) if f.endswith(".key")]
    key_files_sorted = sorted(key_files, key=natural_sort_key)

    # Read and store file contents
    for filename in key_files_sorted:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines()]  # Remove extra spaces/newlines
                key_files_list.append(lines)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    return key_files_list

def calculate_f1(true_keywords, predicted_keywords, stemmer):
    """Calculate precision, recall, and F1 score with token-based overlap."""
    def tokenize_and_normalize(phrase):
         tokens = set(word_tokenize(phrase.lower()))
         stemmed_tokens = {stemmer(token) for token in tokens}  # Stem each token
         return stemmed_tokens


    true_keywords_tok = [tokenize_and_normalize(kw) for kw in true_keywords]
    predicted_keywords_tok = [tokenize_and_normalize(kw) for kw in predicted_keywords]

    intersection_count = 0
    for pred_kw in predicted_keywords_tok:
        #print(pred_kw)
        if any(pred_kw == true_kw for true_kw in true_keywords_tok):
            print(f'Intersection for {pred_kw}')
            intersection_count += 1

    # print("Intersection Count:", intersection_count)
    # print("True Keywords Count:", len(true_keywords))

    precision = intersection_count / len(predicted_keywords) if predicted_keywords else 0
    recall = intersection_count / len(true_keywords) if true_keywords else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1

# Runs keyword extraction on two input folders containing .txt files
async def main(api_url, texts, true_keywords, ngram_size, lang, stemmmer):
    try:
        predicted_keywords = await extract_keywords(api_url, texts, ngram_size, lang)

        # predicted_keywords_stem = stem_words_polish(predicted_keywords, stemmmer)
        # true_keywords_stem = stem_words_polish(true_keywords, stemmmer)

        f1_scores = []
        pr_scores = []
        re_scores = []
        for true_kw, pred_kw in zip(true_keywords, predicted_keywords):
            pr, re, f1 = calculate_f1(true_kw, pred_kw, stemmmer)
            f1_scores.append(f1)
            pr_scores.append(pr)
            re_scores.append(re)

        average_f1 = sum(f1_scores) / len(f1_scores)
        average_pr = sum(pr_scores) / len(pr_scores)
        average_re = sum(re_scores) / len(re_scores)

        return average_pr, average_re, average_f1

    except ValueError as ve:
        print("Error:", ve)
    except TimeoutError as te:
        print("Error:", te)
    except Exception as e:
        print("Unexpected Error:", e)

if __name__ == "__main__":
    results = {}
    ngram_size = 3
    lang = "pl"
    stem_lang = "polish"
    models = ["yake", "keybert", "multirake"]

    #Load data synchronoulsy
    input_texts = "pak2018/docsutf8"
    texts = load_txt_files_to_list(input_texts)

    input_keywords = "pak2018/keys"
    true_keywords = load_key_files_to_sublists(input_keywords)
    print(true_keywords[0])

    stemmer = Stemmer.default()

    for model in models:
        API_URL = f"http://127.0.0.1:8080/{model}/dataset"
        average_pr, average_re, model_average_score = asyncio.run(main(API_URL, texts, true_keywords, ngram_size, lang, stemmer))
        results[model] = (average_pr, average_re, model_average_score)

    print(results)






