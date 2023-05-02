import re
from collections import defaultdict

def find_unique_words(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    word_freq = defaultdict(int)
    subword_freq = defaultdict(int)

    for line in lines:
        tokens = line.strip().split()
        for token in tokens:
            if token.startswith('##'):
                subword_freq[token[2:]] += 1
            else:
                word_freq[token] += 1

    unique_words = set(word_freq.keys()) - set(subword_freq.keys())
    not_alnum = re.compile('^(?![0-9]+$)[^\W_]+$')
    unique_words = [word for word in unique_words if not not_alnum.match(word) and not word.isdigit()]

    return unique_words

def find_doubled_lines(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Strip leading and trailing whitespace from each line
    lines = [line.strip() for line in lines]

    # Create a set of lines without the ## prefix
    unmarked_lines = set(line[2:] for line in lines if line.startswith('##'))

    # Find lines that appear both with and without the ## prefix
    doubled_lines = set()
    for line in lines:
        if line.startswith('##'):
            if line[2:] in unmarked_lines and not re.match(r'^[\u03B1-\u03C9\u03CA-\u03FB\s]+$', line[2:]):
                doubled_lines.add(line[2:])
        elif line in unmarked_lines and not re.match(r'^[\u03B1-\u03C9\u03CA-\u03FB\s]+$', line):
            doubled_lines.add(line)

    return doubled_lines

def process_file(input_file):
    ignore_with_underscore = ['(', '«', '+', '‹', '<', '‚', '※', '—', '„', '⟦', '‘', '‵', '*', '–', '~', '♃', '|', '⩚', '’', '{', '⸏', '"', '=', '[', '.', ']', '†', '§', '/', '‖']
    pretend_underscore = ['𝈺', '♐', '𝈋', '>', '𝈪', '⎩', '₎', '♋', '𝈢', '𝈛', '𝈬', '⏖', '𝈵', ',', '𝈰', '⸐', '⁝', '𝈲', '𝈟', '𐅽', '♎', '⁜', ';', '𝈇', '𝈭', '𝈆', '𝈒', '𝈿', '♊', '𝈩', '𝈁', '♒', '}', '𝈄', '-', '⟪', '𝈍', '⁞', '⎬', '»', '𝈝', '𝈈', '𝈾', '𝈯', '𝉁', "'", '♑', '¿', '𝈡', '𝈸', '𝈮', '♓', '𝈚', '𝈥', '𝉀', '›', '𝈏', '𝈨', '𝈽', '𝈖', '𝈴', '𐆆', '♈', '“', '𝈕', '𝈗', '⟧', '𝈑', '♍', '𝈃', '𐅹', '𝈉', '𝈜', '♌', '𝈊', '⎧', '𝈙', '℧', '⁚', '‛', '𐆈', '♏', '′', '⸑', ')', '⸔', '‧', '𝈠', '𝈣', '⸎', '⟫', '⸓', '𝈐', '♂', '𝈅', '♄', '⁋', '☍', '”', '𝈂', '𝈷', '𝈹', '𝈔', '!', '\\', '⸒', '𝈤', '𝈀', '𝈌', '𐅾', '₍', '𐆅', '♉', '≌', '⸕', '·', ':', '¡', '•', '𝈎', '𐆉', '?', '𝈘', '𝈞', '𝈦', '☿', '⸖']
    forced_double = ['٢', '⁄', '٦', '⎨', '¨', '𝈶', '★', 'ˋ', 'ϼ', '῀', '𝈳', '¾', '⎪', '¹', '\x9c', '٩', '\x93', '𐅼', '○', 'ʒ', '←', '♀', 'ˆ', '𝈱', 'º', '↑', '⏓', '⎭', '⎠', '⏒', '\x81', '⏔', '᾿', '⎞', '\x84', '☾', '∻', '١', '٠', '→', '٧', '☧', '½', '¸', '˙', '\x91', '☽', '⊗', 'ʽ', '☉', '´', '𐅄', '⌝', '῾', '☩', 'ʼ', '٥', 'ˊ', '𐆂', '٤', '᾽','٨', '⎫', '⏕', '\x80', '⌟', '0', '٣', '𝈓', 'ʹ', 'ⲁ']
    random_singles = ["`", '𐅷', '𐄑', '𐄒', '𐅀', '⏑⏑']
    with open(input_file, 'r') as f_in, open('test_conversion.txt', 'w') as f_out:
        for i, line in enumerate(f_in):
            if i < 5:
                # Skip the first 5 lines and write special tokens instead
                if i == 0:
                    f_out.write('[PAD]\n')
                elif i == 1:
                    f_out.write('[UNK]\n')
                elif i == 2:
                    f_out.write('[CLS]\n')
                elif i == 3:
                    f_out.write('[SEP]\n')
                elif i == 4:
                    f_out.write('[MASK]\n')
                    for word in ignore_with_underscore:
                        f_out.write(word + '\n')
                    for word in pretend_underscore:
                        f_out.write(word + '\n')
                    for word in forced_double:
                        f_out.write(word + '\n')
                    for word in random_singles:
                        f_out.write(word + '\n')
                    
            else:
                # Strip leading and trailing whitespace
                line = line.strip()
                if not line or any(c in line for c in ignore_with_underscore) or any(c in line for c in pretend_underscore) or any(c in line for c in random_singles):
                    pass
                elif line.startswith('▁'):
                    # Write line to output file without leading underscore
                    if line != '▁':
                        f_out.write(line[1:] + '\n')
                else:
                    # Add ## to the beginning of the line and write to output file
                    f_out.write('##' + line + '\n')

def main():
    input_file = '50k-Unigram/50k_Unigram_vocab_characters.txt'
    process_file(input_file)
    # doubled_lines = find_doubled_lines('25k-Wordpiece/wordpiece-25k-vocab.txt')
    # print(doubled_lines)
    # unique_words = find_unique_words('50k-Wordpiece/wordpiece-50k-vocab.txt')
    doubled_lines = find_doubled_lines('50k-Wordpiece/wordpiece-50k-vocab.txt')

    found = []
    not_found = []
    exists_both_ways = []
    underscore_but_not_without = []
    no_underscore_but_exists_without = []
    exists_neither_way = []

    
    for word in doubled_lines:
        if '▁' + word in open(input_file).read():
            found.append(word)
        else:
            not_found.append(word)
    
    for word in found:
        if '\n' + word + '\n' in open(input_file).read():
            exists_both_ways.append(word)
        else:
            underscore_but_not_without.append(word)
    
    for word in not_found:
        if '\n' + word + '\n' in open(input_file).read():
            no_underscore_but_exists_without.append(word)
        else:
            exists_neither_way.append(word)
    
    print('exists_both_ways', exists_both_ways)
    print('underscore_but_not_without', underscore_but_not_without)
    print('no_underscore_but_exists_without', no_underscore_but_exists_without)
    print('exists_neither_way', exists_neither_way)

    with open('50k-Unigram/50k_Unigram_vocab_characters.txt', 'r') as f:
        x = len(f.readlines())
        print('Unigram:', x)
    
    with open('50k-Wordpiece/wordpiece-50k-vocab.txt', 'r') as f:
        x = len(f.readlines())
        print('Wordpiece:', x)

    with open('test_conversion.txt', 'r') as f:
        x = len(f.readlines())
        print('New:', x)



if __name__ == '__main__':
    main()