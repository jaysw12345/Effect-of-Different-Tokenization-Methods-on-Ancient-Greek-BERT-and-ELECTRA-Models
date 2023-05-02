import re

def main():
    # Open the two input files
    with open('50k-Wordpiece/wordpiece-50k-vocab.txt') as f1, open('test_conversion.txt') as f2:
        # Read the contents of each file
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())
    
    with open('50k-Unigram/50k_Unigram_vocab_characters.txt') as f:
        set3 = set(f.read().splitlines())

    # Find elements in set1 that are not in set2
    diff = set1 - set2

    # Define a regex pattern to match ancient greek characters, ##, or letters
    pattern = re.compile("[^\u0370-\u03FF\s#A-Za-z]")

    diff = [word for word in diff if not word.isdigit()]

    # Loop through the differences and check for invalid characters
    for elem in diff:
        if pattern.search(elem):
            if elem in set3:
                print(elem)



if __name__ == '__main__':
    main()