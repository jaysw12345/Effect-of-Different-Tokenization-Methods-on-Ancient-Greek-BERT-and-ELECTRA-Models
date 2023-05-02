import sentencepiece as spm
from transformers import BertTokenizer

def main():
    #text = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων, ὡς ἐπολέμησαν πρὸς ἀλλήλους, ἀρξάμενος εὐθὺς καθισταμένου καὶ ἐλπίσας μέγαν τε ἔσεσθαι καὶ ἀξιολογώτατον τῶν προγεγενημένων, τεκμαιρόμενος ὅτι ἀκμάζοντές τε ᾖσαν ἐς αὐτὸν ἀμφότεροι παρασκευῇ τῇ πάσῃ καὶ τὸ ἄλλο Ἑλληνικὸν ὁρῶν ξυνιστάμενον πρὸς ἑκατέρους, τὸ μὲν εὐθύς, τὸ δὲ καὶ διανοούμενον. [2] κίνησις γὰρ αὕτη μεγίστη δὴ τοῖς Ἕλλησιν ἐγένετο καὶ μέρει τινὶ τῶν βαρβάρων, ὡς δὲ εἰπεῖν καὶ ἐπὶ πλεῖστον ἀνθρώπων. [3] τὰ γὰρ πρὸ αὐτῶν καὶ τὰ ἔτι παλαίτερα σαφῶς μὲν εὑρεῖν διὰ χρόνου πλῆθος ἀδύνατα ἦν, ἐκ δὲ τεκμηρίων ὧν ἐπὶ μακρότατον σκοποῦντί μοι πιστεῦσαι ξυμβαίνει οὐ μεγάλα νομίζω γενέσθαι οὔτε κατὰ τοὺς πολέμους οὔτε ἐς τὰ ἄλλα. 2. φαίνεται γὰρ ἡ νῦν Ἑλλὰς καλουμένη οὐ πάλαι βεβαίως οἰκουμένη, ἀλλὰ μεταναστάσεις τε οὖσαι τὰ πρότερα καὶ ῥᾳδίως ἕκαστοι τὴν ἑαυτῶν ἀπολείποντες βιαζόμενοι ὑπό τινων αἰεὶ πλειόνων."
    text = "(«+‹<‚※—„⟦‘‵*–~♃|⩚’{"
    # Load the SentencePiece model
    sp = spm.SentencePieceProcessor()
    sp.load(f"25k-Unigram/25k-Unigram.model")

    # Encode the sentence using the loaded model
    tokens = sp.encode_as_pieces(text)

    print(text)

    print(tokens)
    #text = "Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων"

    #print(text)

    tokenizer = BertTokenizer.from_pretrained('25k-Unigram/24897_Unigram_vocab.txt')
    ids = tokenizer.encode(text)
    print(tokenizer.convert_ids_to_tokens(ids))

    tokenizer = BertTokenizer.from_pretrained('25k-Wordpiece/wordpiece-25k-vocab.txt')
    ids = tokenizer.encode(text)
    print(tokenizer.convert_ids_to_tokens(ids))



if __name__ == '__main__':
    main()