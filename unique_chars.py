import codecs
import time

def main():
    # Open the file in binary mode and read as UTF-8
    with codecs.open('Datasets/all_tlg_words.txt', mode='rb', encoding='utf-8') as file:
        text = file.read()

    # Create a set of unique characters
    unique_chars = set(text)

    # Count the occurrence of each unique character
    char_count = {char: text.count(char) for char in unique_chars}

    # Print the result to a file
    with open('unique_characters.txt', mode='w', encoding='utf-8') as file:
        for char, count in char_count.items():
            file.write(f"{char}\n")

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))