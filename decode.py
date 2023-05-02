import sentencepiece as spm

# Load the SentencePiece model
sp = spm.SentencePieceProcessor()
#sp.load("50k-Unigram/50k-Unigram.model")
sp.load("25k-Unigram.model")

# Iterate over all the vocabulary pieces and obtain their string representations
vocab_size = sp.get_piece_size()

#with open('50k-Unigram/sentencepiece_vocab.txt', 'w') as h:
with open('25k_Unigram_vocab_characters.txt', 'w') as h:
    for i in range(vocab_size):
        h.write("{}\n".format(sp.id_to_piece(i)))