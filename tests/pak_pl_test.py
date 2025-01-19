import asyncio
import aiohttp
import os
import re
from nltk.tokenize import word_tokenize
from semeval_test import calculate_f1, fetch_keywords_async,get_keywords_results, extract_keywords


# Otherwise the load sequence is broken
def natural_sort_key(filename):
    """Extract numerical value from filename for sorting."""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', filename)]


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


# Runs keyword extraction on two input folders containing .txt files
async def main(api_url, texts, true_keywords, ngram_size, lang):
    try:
        predicted_keywords = await extract_keywords(api_url, texts, ngram_size, lang)

        f1_scores = []
        for true_kw, pred_kw in zip(true_keywords, predicted_keywords):
            _, _, f1 = calculate_f1(true_kw, pred_kw)
            f1_scores.append(f1)

        average_f1 = sum(f1_scores) / len(f1_scores)
        return average_f1
    except ValueError as ve:
        print("Error:", ve)
    except TimeoutError as te:
        print("Error:", te)
    except Exception as e:
        print("Unexpected Error:", e)

if __name__ == "__main__":
    models = ["yake", "keybert", "multirake"]

    #Load data synchronoulsy
    input_texts = "pak2018/docsutf8"
    texts = load_txt_files_to_list(input_texts)

    input_keywords = "pak2018/keys"
    true_keywords = load_key_files_to_sublists(input_keywords)

    results = {}
    ngram_size = 3
    lang = "pl"

    for model in models:
        API_URL = f"http://127.0.0.1:8080/{model}/dataset"
        model_average_score = asyncio.run(main(API_URL, texts, true_keywords, ngram_size, lang))
        results[model] = model_average_score

    print(results)






