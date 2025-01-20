import os


def analyze_dataset(folder_path):
    """
    Analyze a dataset folder and return statistics on number of files,
    average lines, characters, and words per file.

    Args:
        folder_path (str): Path to the dataset folder.

    Returns:
        dict: Contains number of files, average number of lines,
              average number of characters, and average number of words.
    """
    file_count = 0
    total_lines = 0
    total_chars = 0
    total_words = 0
    total_line_len = 0

    # Check if the folder exists
    if not os.path.exists(folder_path):
        return {"error": "Folder does not exist"}

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Ensure it's a file and not a directory
        if os.path.isfile(file_path):
            file_count += 1
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                lines_len = len(lines)
                total_lines += lines_len
                total_chars += sum(len(line) for line in lines)
                total_words += sum(len(line.split()) for line in lines)

    # Calculate averages
    avg_lines = total_lines / file_count if file_count > 0 else 0
    avg_chars = total_chars / file_count if file_count > 0 else 0
    avg_words = total_words / file_count if file_count > 0 else 0
    avg_lines_len = total_words/ total_lines

    return {
        "number_of_files": file_count,
        "average_lines_per_file": avg_lines,
        "average_characters_per_file": avg_chars,
        "average_words_per_file": avg_words,
        "average_line_len": avg_lines_len
    }


# Example usage
if __name__ == "__main__":
    folder_path = input("Enter the dataset folder path: ").strip()
    result = analyze_dataset(folder_path)

    if "error" in result:
        print(result["error"])
    else:
        print(f"Number of files: {result['number_of_files']}")
        print(f"Average lines per file: {result['average_lines_per_file']:.2f}")
        print(f"Average characters per file: {result['average_characters_per_file']:.2f}")
        print(f"Average words per file: {result['average_words_per_file']:.2f}")
        print(f"Average lines per file: {result['average_line_len']:.2f}")
