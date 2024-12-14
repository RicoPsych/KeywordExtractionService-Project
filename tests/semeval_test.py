import asyncio
import aiohttp
import nltk
from datasets import load_dataset
from nltk.tokenize import word_tokenize

async def fetch_keywords_async(api_url, texts, ngram_size):
    """Send texts to the asynchronous API and fetch task UUID."""
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json={ "texts": texts, "ngram": ngram_size }) as response:
            response_data = await response.json()
            return response_data.get("taskId")


async def get_keywords_results(api_url, task_id):
    """Fetch the results of the keyword extraction task using the task UUID."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_url}?uuid={task_id}") as response:
            response_data = await response.json()
            return response_data.get("results")


async def extract_keywords(api_url, texts, ngram_size):
    """Extract keywords asynchronously for a list of texts."""
    task_id = await fetch_keywords_async(api_url, texts, ngram_size)
    if not task_id:
        raise ValueError("Failed to retrieve task ID")

    for _ in range(20):
        await asyncio.sleep(2)
        results = await get_keywords_results(api_url, task_id)
        if results:
            return results

    raise TimeoutError("Keyword extraction task timed out")


def bio_tags_to_keywords(document, bio_tags):
    """Convert BIO tags to keywords."""
    keywords = []
    current_keyword = []

    for token, tag in zip(document, bio_tags):
        if tag.startswith("B"):
            if current_keyword:
                keywords.append(" ".join(current_keyword))
                current_keyword = []
            current_keyword.append(token)
        elif tag.startswith("I") and current_keyword:
            current_keyword.append(token)
        elif current_keyword:
            keywords.append(" ".join(current_keyword))
            current_keyword = []

    if current_keyword:
        keywords.append(" ".join(current_keyword))

    return keywords

def calculate_f1(true_keywords, predicted_keywords):
    """Calculate precision, recall, and F1 score with token-based overlap."""
    def tokenize_and_normalize(phrase):
        return set(word_tokenize(phrase.lower()))

    true_keywords = [tokenize_and_normalize(kw) for kw in true_keywords]
    predicted_keywords = [tokenize_and_normalize(kw) for kw in predicted_keywords]

    intersection_count = 0
    for pred_kw in predicted_keywords:
        if any(pred_kw & true_kw for true_kw in true_keywords):
            intersection_count += 1

    precision = intersection_count / len(predicted_keywords) if predicted_keywords else 0
    recall = intersection_count / len(true_keywords) if true_keywords else 0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    return precision, recall, f1


async def main(api_url, ngram_size):
    """Main function to run the YAKE keyword extraction and evaluate it."""
    dataset = load_dataset("midas/semeval2017", "extraction")
    test_data = dataset["test"]

    texts = [" ".join(item["document"]) for item in test_data]
    ground_truth_keywords = [
        bio_tags_to_keywords(item["document"], item["doc_bio_tags"]) for item in test_data
    ]

    predicted_keywords = await extract_keywords(api_url, texts, ngram_size)

    f1_scores = []
    for true_kw, pred_kw in zip(ground_truth_keywords, predicted_keywords):
        _, _, f1 = calculate_f1(true_kw, pred_kw)
        f1_scores.append(f1)

    average_f1 = sum(f1_scores) / len(f1_scores)
    return average_f1


# Example usage
if __name__ == "__main__":
    models = ["yake", "keybert", "multirake"]
    results = {}
    ngram_size = 3
    for model in models:
        API_URL = f"http://127.0.0.1:8080/{model}/dataset"
        model_average_score = asyncio.run(main(API_URL, ngram_size))
        results[model] = model_average_score

    print(results)