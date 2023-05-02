import sentencepiece as spm
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def preprocess(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    text = remove_accents(text.lower())
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

def main():

    # Define the path to the input file and the output tokenized file
    input_file = "Datasets/all_tlg_words.txt"

    preprocessed_file = "preprocessed.txt"

    # Preprocess the input file
    # preprocess(input_file, preprocessed_file)

    # Define the SentencePiece model configuration

    spm.SentencePieceTrainer.train(
        f'--input={input_file} '
        '--normalization_rule_tsv=normalization.TSV '
        '--model_prefix=25k-Unigram '
        '--vocab_size=25000 '
        '--character_coverage=1.0 '
        '--model_type=unigram '
        '--max_sentence_length=15000000 '
        "--control_symbols=[MASK],[PAD] "
        '--pad_piece=[PAD] '
        '--unk_piece=[UNK] '
        '--bos_piece=[CLS] '
        '--eos_piece=[SEP]'
    )

    # Test the tokenizer on an Ancient Greek sentence
    sentence = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων, ὡς ἐπολέμησαν πρὸς ἀλλήλους, ἀρξάμενος εὐθὺς καθισταμένου καὶ ἐλπίσας μέγαν τε ἔσεσθαι καὶ ἀξιολογώτατον τῶν προγεγενημένων, τεκμαιρόμενος ὅτι ἀκμάζοντές τε ᾖσαν ἐς αὐτὸν ἀμφότεροι παρασκευῇ τῇ πάσῃ καὶ τὸ ἄλλο Ἑλληνικὸν ὁρῶν ξυνιστάμενον πρὸς ἑκατέρους, τὸ μὲν εὐθύς, τὸ δὲ καὶ διανοούμενον. [2] κίνησις γὰρ αὕτη μεγίστη δὴ τοῖς Ἕλλησιν ἐγένετο καὶ μέρει τινὶ τῶν βαρβάρων, ὡς δὲ εἰπεῖν καὶ ἐπὶ πλεῖστον ἀνθρώπων. [3] τὰ γὰρ πρὸ αὐτῶν καὶ τὰ ἔτι παλαίτερα σαφῶς μὲν εὑρεῖν διὰ χρόνου πλῆθος ἀδύνατα ἦν, ἐκ δὲ τεκμηρίων ὧν ἐπὶ μακρότατον σκοποῦντί μοι πιστεῦσαι ξυμβαίνει οὐ μεγάλα νομίζω γενέσθαι οὔτε κατὰ τοὺς πολέμους οὔτε ἐς τὰ ἄλλα."

    print(sentence)

    # Load the SentencePiece model
    sp = spm.SentencePieceProcessor()
    sp.load(f"25k-Unigram.model")

    # Encode the sentence using the loaded model
    tokens = sp.encode_as_pieces(sentence)

    print(tokens)

if __name__ == '__main__':
    main()