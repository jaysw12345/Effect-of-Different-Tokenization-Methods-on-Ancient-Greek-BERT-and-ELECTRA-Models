from transformers import BertTokenizer
from tokenizers import Tokenizer, decoders
from tokenizers.pre_tokenizers import ByteLevel
import sentencepiece as spm
import text_cleaning_API
import re
import time

# tokenize the data
def wordpiece():
    tokenizer = BertTokenizer.from_pretrained('25k-Wordpiece/wordpiece-25k-vocab.txt')
    return tokenizer

def old_unigram():
    tokenizer = BertTokenizer.from_pretrained('unigram-50k-vocab.txt')
    tokenizer.pre_tokenizer = ByteLevel()
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.basic_tokenizer.lowercase = True
    tokenizer.basic_tokenizer.strip_accents = True
    return tokenizer

def unigram():
    # sp = spm.SentencePieceProcessor()
    # sp.load(f"25k-Unigram/25k-Unigram.model")
    # return sp
    tokenizer = BertTokenizer.from_pretrained('50k-Unigram/unigram-49695-vocab.txt')
    return tokenizer

def old_tokenizer():
    tokenizer = BertTokenizer.from_pretrained('pranaydeeps/Ancient-Greek-BERT')
    return tokenizer

def main():
    tokenizer = unigram()
    # tokenizer_type = 'unigram'
    is_wordpiece = False
    is_unigram = True
    is_old = False

    text = "Τοίην γὰρ Πελίης φάτιν ἔκλυεν, ὥς μιν ὀπίσσω μοῖρα μένει στυγερή. τοῦδ' ἀνέρος ὅντιν' ἴδοιτο δημόθεν οἰοπέδιλον ὑπ' ἐννεσίῃσι δαμῆναι·"

    # if is_wordpiece:
    ids = tokenizer.encode(text)
    print(text)
    print(ids)
    print(tokenizer.convert_ids_to_tokens(ids))
    
    # elif is_unigram:
    #    tokens = tokenizer.encode_as_pieces(text)
    #    print(text)
    #    print(tokens)
    
    # elif is_old:
    #    ids = tokenizer.encode(text)
    #    print(text)
    #    print(ids)
    #    print(tokenizer.convert_ids_to_tokens(ids))

    # prepare the data to be read by BERT
    with open('Datasets/all_tlg_words.txt', 'r') as f:
        t = f.read()
    f.close()
    t_split = t.split('\n\n')
    print(len(t_split))
    ls = []

    # split sentences
    for i,c in enumerate(t_split):
        ls += text_cleaning_API.sep_sents(c, i, tokenizer)

    
    # check length and append
    # for i in ls:
        # x = (len(tokenizer(i)['input_ids']))
        # if x > 490:
            # print(x)

    new_ls = []
    for i in ls:
        p = re.search('[α-ωΑ-Ω]', i)
        if p is None:
            print
            continue
        else:
            new_ls.append(i)

    print(len(ls))
    print(len(new_ls))

    if is_wordpiece:
        with open('25k-Wordpiece/25k_wordpiece.txt', 'w') as h:
            for sent in new_ls:
                h.write("{}\n".format(sent))
    elif is_unigram:
        with open('50k-Unigram/50k_unigram.txt', 'w') as h:
            for sent in new_ls:
                h.write("{}\n".format(sent))
    elif is_old:
        with open('Desi_chunked.txt', 'w') as h:
            for sent in new_ls:
                h.write("{}\n".format(sent))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))