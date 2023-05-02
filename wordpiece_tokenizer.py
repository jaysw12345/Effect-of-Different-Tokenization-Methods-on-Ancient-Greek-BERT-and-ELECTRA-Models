import os
from tokenizers import BertWordPieceTokenizer

# tokenize the data
def main():
    # initialize
    tokenizer = BertWordPieceTokenizer(
        clean_text=False,
        handle_chinese_chars=False,
        strip_accents=True,
        lowercase=True
    )
    tokenizer.train(files='Datasets/all_tlg_words.txt', vocab_size=50_000, min_frequency=2,
                limit_alphabet=1000, wordpieces_prefix='##',
                special_tokens=[
                    '[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]'])
    
    os.mkdir('./wordpiece-25k')
    tokenizer.save_model('./wordpiece-25k', 'wordpiece-25k')

    return tokenizer

if __name__ == '__main__':
    main()
