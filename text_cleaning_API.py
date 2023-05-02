from transformers import BertTokenizer, BertForMaskedLM
import torch
import re

def fix_term_sigs(text):
  if text == '':
    return ''
  ls = []
  chars = 'ερτυθιοπλκξηγφδσαζχψωβνμΕΡΤΥΘΙΟΠΛΚΞΗΓΦΔΣΑΖΧΨΩΒΝΜ'
  for i,ch in enumerate(text):
    if i == len(text) - 1:
      continue
    if ch == 'ς' and text[i+1] in chars:
      ls.append('σ')
    else:
      ls.append(ch)
  ls.append(text[-1])
  return ''.join(ls)

def clean(text):
  # brackets
  text = text.replace('[', '')
  text = text.replace(']', '')
  text = text.replace('|', '')
  text = text.replace('<', '')
  text = text.replace('>', '')
  text = text.replace('{', '')
  text = text.replace('}', '')
  text = text.replace('†', '')
  text = text.replace('‖', '')
  text = text.replace('“', '"')
  text = text.replace('„', '"')

  # text = text.replace('\'', '"')
  # text = text.replace('\'', '"')

  
  
  # lunate sigmas at the end of the word
  text = re.sub(r'c(?!\w)', 'ς', text)
  # all remaining lunate sigmas
  text = re.sub(r'c', 'σ', text)
  text = re.sub(r'C', 'Σ', text)
  text = re.sub(r'\n', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  # fix bad sigmas
  text = fix_term_sigs(text)
  # delete strings that contain numbers, but leave end punctuation if it's there
  text = re.sub(r'[^\s]*([0-9])[^\s]*\;', ';', text)
  text = re.sub(r'[^\s]*([0-9])[^\s]*\·', '·', text)
  text = re.sub(r'[^\s]*([0-9])[^\s]*\.', '.', text)
  text = re.sub(r'[^\s]*([0-9])[^\s]*\!', '!', text)
  text = re.sub(r'[^\s]*([0-9])[^\s]*\,', ',', text)
  text = re.sub(r'[^\s]*([0-9])[^\s]*', '', text)
  # new line and white space turns to space
  text = re.sub(r'\n', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  return text

def sent_too_long(sent, max_toks, tokenizer):
  # split up a list until no more than 500 tokens anywhere
  words = sent.split(' ')
  # tokenize each word, concatenate until too many tokens!
  final_ls = []
  cur_str = ''
  cur_toks = 0
  for word in words:
    # if tokenizer_type == 'wordpiece':
    toks = tokenizer(word)['input_ids']
    length = len(toks)
    # elif tokenizer_type == 'unigram':
    #  toks = tokenizer.encode_as_pieces(word)
    #  length = len(toks) + 2
    # else:
    #  raise NameError('invalid name for tokenizer_type')
    if (length + cur_toks) <= max_toks:
      cur_str += (' ' + word)
      cur_toks += length
    else:
      final_ls.append(cur_str)
      cur_str = word
      cur_toks = length
  if cur_toks > 0:
    final_ls.append(cur_str)
    return final_ls

# returns a list of sentences which we can write to a file, separated by newlines
def sep_sents(text, ind, tokenizer, max_toks=500):
  print('IND: ' + str(ind))

  text = clean(text)

  # special clean case
  text = text.replace('.   .   .', ' [UNK] ')
  # add special separator after end punctuation
  text = re.sub(r'\·', '· [SEP] ', text)
  text = re.sub(r'\.', '. [SEP] ', text)
  text = re.sub(r'\;', '; [SEP] ', text)
  text = re.sub(r'\!', '! [SEP] ', text)

  sents = text.split('[SEP]')
  # tokenize each sentence, concatenate until too many tokens!
  final_ls = []
  cur_str = ''
  cur_toks = 0
  for sent in sents:
    # if tokenizer_type == 'wordpiece':
    toks = tokenizer(sent)['input_ids']
    length = len(toks)
    # elif tokenizer_type == 'unigram':
    #  toks = tokenizer.encode_as_pieces(sent)
    #  length = len(toks) + 2
    # else:
    #  raise NameError('invalid name for tokenizer_type')
    if (length + cur_toks) <= max_toks:
      cur_str += (' ' + sent)
      cur_toks += length
    elif cur_toks == 0:
      final_ls += sent_too_long(sent, max_toks, tokenizer)
      cur_toks = 0
      cur_str = ''
    else:
      final_ls.append(cur_str)
      cur_str = sent
      cur_toks = length
  if cur_toks > 0:
    final_ls.append(cur_str)
  if ' ' not in cur_str:
    print('HERE: ' + str(ind))
  ret_ls = []
  for el in final_ls:
    # if tokenizer_type == 'wordpiece':
    new_length = len(tokenizer(el)['input_ids'])
    # elif tokenizer_type == 'unigram':
    #  new_length = len(tokenizer.encode_as_pieces(el)) + 2
    # else:
    #  raise NameError('invalid name for tokenizer_type')
    if new_length > max_toks:
      ret_ls += sep_sents(el, -1 * ind, tokenizer)
    else:
      ret_ls.append(el)
  return ret_ls
