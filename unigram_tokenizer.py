import os
from tokenizers import Tokenizer, decoders
import re
import unicodedata
import string
import os
from tokenizers.models import Unigram
from tokenizers import normalizers
from tokenizers.normalizers import StripAccents, Lowercase
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import UnigramTrainer
from tokenizers.processors import TemplateProcessing

def preprocess_text(text):
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn') # remove diacritical marks for both Greek and non-Greek characters

    return text


# tokenize the data
def main():
    # initialize
    tokenizer = Tokenizer(Unigram())
    # normalizer = normalizers.Sequence([StripAccents(), Lowercase()])
    # tokenizer.normalizer = normalizer
    tokenizer.pre_tokenizer = ByteLevel()
    tokenizer.decoder = decoders.ByteLevel()
    trainer = UnigramTrainer(vocab_size=50000, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
    tokenizer.post_processor = TemplateProcessing(  
        single="[CLS] $A [SEP]",
        pair="[CLS] $A [SEP] $B:1 [SEP]:1",
        special_tokens=[("[CLS]", 1), ("[SEP]", 2)],)

    #files = ["super_mini_wordpiece.txt"]
    #tokenizer.train(files, trainer)
    with open("super_mini_wordpiece.txt", "r") as f:
        text = f.read()
    preprocessed_text = preprocess_text(text)
    with open("test123.txt", 'w') as f:
        f.write(preprocessed_text)
    files = ["test123.txt"]
    tokenizer.train(files, trainer)

    vocab = tokenizer.get_vocab()

    with open('unigram-50k-vocab.txt', 'w') as f:
        for token in vocab.items():
            f.write(f"{token[0]}\n")

    #os.mkdir("./unigram-it")
    #tokenizer.save_model("./unigram-it/vocab.txt")

    return tokenizer

if __name__ == '__main__':
    main()
