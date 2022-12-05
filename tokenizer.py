from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import re
import unicodedata
import six
import tensorflow as tf
import tensorflow_text as text
import pandas as pd
import numpy as np

def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
  """Checks whether the casing config is consistent with the checkpoint name."""

  if not init_checkpoint:
    return

  m = re.match("^.*?([A-Za-z0-9_-]+)/bert_model.ckpt", init_checkpoint)
  if m is None:
    return

  model_name = m.group(1)

  lower_models = [
      "uncased_L-24_H-1024_A-16", "uncased_L-12_H-768_A-12",
      "multilingual_L-12_H-768_A-12", "chinese_L-12_H-768_A-12"
  ]

  cased_models = [
      "cased_L-12_H-768_A-12", "cased_L-24_H-1024_A-16",
      "multi_cased_L-12_H-768_A-12"
  ]

  is_bad_config = False
  if model_name in lower_models and not do_lower_case:
    is_bad_config = True
    actual_flag = "False"
    case_name = "lowercased"
    opposite_flag = "True"

  if model_name in cased_models and do_lower_case:
    is_bad_config = True
    actual_flag = "True"
    case_name = "cased"
    opposite_flag = "False"

  if is_bad_config:
    raise ValueError(
        "You passed in `--do_lower_case=%s` with `--init_checkpoint=%s`. "
        "However, `%s` seems to be a %s model, so you "
        "should pass in `--do_lower_case=%s` so that the fine-tuning matches "
        "how the model was pre-training. If this error is wrong, please "
        "just comment out this check." % (actual_flag, init_checkpoint,
                                          model_name, case_name, opposite_flag))

def convert_to_unicode(text):
  """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
  if isinstance(text, str):
    return text
  elif isinstance(text, bytes):
    return text.decode("utf-8", "ignore")
  else:
    raise ValueError("Unsupported string type: %s" % (type(text)))
  

def printable_text(text):
  """Returns text encoded in a way suitable for print or `tf.logging`."""
  if six.PY3:
    if isinstance(text, str):
      return text
    elif isinstance(text, bytes):
      return text.decode("utf-8", "ignore")
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  elif six.PY2:
    if isinstance(text, str):
      return text
    elif isinstance(text, unicode):
      return text.encode("utf-8")
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  else:
    raise ValueError("Not running on Python2 or Python 3?")


def load_vocab(vocab_file):
  """Loads a vocabulary file into a dictionary."""
  nl = pd.read_csv(vocab_file,index_col=0)
  """
  with tf.gfile.GFile(vocab_file, "r") as reader:
    while True:
      token = convert_to_unicode(reader.readline())
      if not token:
        break
      token = token.strip()
      vocab[token] = index
      index += 1
  """
  return nl.loc[nl.en_Trainable,'en_ids1'].to_dict()

def whitespace_tokenize(text):
  """Runs basic whitespace cleaning and splitting on a piece of text."""
  text = text.strip()
  if not text:
    return []
  tokens = text.split()
  return tokens

class albert_en_preprocess():
  def __init__(self,vocab_file,len_sequence=128):
    self.full_tokenizer = FullTokenizer(vocab_file)
    self.len_sequence = len_sequence
    
  def __call__(self,text):
    tokens = self.full_tokenizer.encode(self.full_tokenizer.tokenize(text))

    input_word_ids = np.zeros((1,self.len_sequence),dtype='int32')
    input_word_ids[0,:len(tokens)] = tokens
    
    input_mask = np.zeros((1,self.len_sequence),dtype='int32')
    input_mask[0,:len(tokens)] = np.ones(len(tokens),dtype='int32')
    input_mask[0,1] = 0
    for i in tokens:
      break
      if i == 23044:
        input_mask[0,tokens.index(i)] = 0
        
    input_type_ids = np.zeros((1,self.len_sequence),dtype='int32')

    return [input_word_ids,input_mask,input_type_ids]

  def encode(self, tokens):
    return self.full_tokeinzer.encode(tokens)

  def decode(self, ids):
    return self.full_tokenizer.decode(ids)
  
class FullTokenizer(object):
  """Runs end-to-end tokenziation."""

  def __init__(self, vocab_file, do_lower_case=True,return_org=False):
    self.vocab = load_vocab(vocab_file)
    self.inv_vocab = {v: k for k, v in self.vocab.items()}
    self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
    self.wordpiece_tokenizer = WordpieceTokenizer(vocab=self.vocab,return_org=return_org)

  def tokenize(self, text):
    split_tokens = []
    for token in self.basic_tokenizer.tokenize(text):
      for sub_token in self.wordpiece_tokenizer.tokenize(token):
        split_tokens.append(sub_token)
    return split_tokens

  def encode(self, tokens):
    output = [2]
    for token in tokens:
      output.append(self.vocab[token])
    output.append(3)
    return output

  def decode(self, ids):
    s = ""
    group_token = False
    for i in ids:
      if i == 48:
        group_token = True
        continue
      if i == 49:
        group_token = False
        s += " "
        continue
      if i not in [2,3,0]:
        s += self.inv_vocab[i]
        if not group_token:
          s += " "
          
    return s[:-1]

  def save_new_vocab(self,new_vocab_file,vocabs):
    pd.DataFrame(data=vocabs.values(),columns=['vocab']).to_csv(new_vocab_file)

class BasicTokenizer(object):
  """Runs basic tokenization (punctuation splitting, lower casing, etc.)."""

  def __init__(self, do_lower_case=True):
    """Constructs a BasicTokenizer.

    Args:
      do_lower_case: Whether to lower case the input.
    """
    self.do_lower_case = do_lower_case

  def tokenize(self, text):
    
    """Tokenizes a piece of text."""
    text = convert_to_unicode(text)
    text = self._clean_text(text)
    text = self._tokenize_chinese_chars(text)

    orig_tokens = whitespace_tokenize(text)
    split_tokens = []
    for token in orig_tokens:
      if self.do_lower_case:
        token = token.lower()
        token = self._run_strip_accents(token)
      split_tokens.extend(self._run_split_on_punc(token))

    return whitespace_tokenize(" ".join(split_tokens))

  def _run_strip_accents(self, text):
    """Strips accents from a piece of text."""
    text = unicodedata.normalize("NFD", text)
    output = []
    for char in text:
      cat = unicodedata.category(char)
      if cat == "Mn":
        continue
      output.append(char)
    return "".join(output)

  def _run_split_on_punc(self, text):
    """Splits punctuation on a piece of text."""
    chars = list(text)
    i = 0
    start_new_word = True
    output = []
    while i < len(chars):
      char = chars[i]
      if _is_punctuation(char):
        output.append([char])
        start_new_word = True
      else:
        if start_new_word:
          output.append([])
        start_new_word = False
        output[-1].append(char)
      i += 1

    return ["".join(x) for x in output]

  def _tokenize_chinese_chars(self, text):
    """Adds whitespace around any CJK character."""
    output = []
    for char in text:
      cp = ord(char)
      if self._is_chinese_char(cp):
        output.append(" ")
        output.append(char)
        output.append(" ")
      else:
        output.append(char)
    return "".join(output)

  def _is_chinese_char(self, cp):
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
        (cp >= 0x3400 and cp <= 0x4DBF) or  #
        (cp >= 0x20000 and cp <= 0x2A6DF) or  #
        (cp >= 0x2A700 and cp <= 0x2B73F) or  #
        (cp >= 0x2B740 and cp <= 0x2B81F) or  #
        (cp >= 0x2B820 and cp <= 0x2CEAF) or
        (cp >= 0xF900 and cp <= 0xFAFF) or  #
        (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
      return True

    return False

  def _clean_text(self, text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
      cp = ord(char)
      if cp == 0 or cp == 0xfffd or _is_control(char):
        continue
      if _is_whitespace(char):
        output.append(" ")
      else:
        output.append(char)
    return "".join(output)


class WordpieceTokenizer(object):
  """Runs WordPiece tokenziation."""

  def __init__(self, vocab, return_org, unk_token="[UNK]", max_input_chars_per_word=100):
    self.vocab = vocab
    self.unk_token = unk_token
    self.max_input_chars_per_word = max_input_chars_per_word
    self.return_org = return_org

  def tokenize(self, text):
    tokens = []
    for token in whitespace_tokenize(text):
      if len(token) > self.max_input_chars_per_word:
        tokens.append(self.unk_token)
        continue

      if token not in self.vocab.keys():
        sub_tokens = []
        sub_tokens.append('[BOW]')
        p = len(token)
        h = 0
        while not p == h:
          if token[h:p] not in self.vocab.keys():
            p -= 1
          else:
            sub_tokens.append(token[h:p])
            h = p
            p = len(token)
        sub_tokens.append('[EOW]')
        tokens.extend(sub_tokens)
      else:
        tokens.append(token)
    return tokens

  def load_new_voab(self,new_vocab_file):
    return pd.read_csv(new_vocab_file,index_col=0)['vocab'].to_dict()

def _is_whitespace(char):
  """Checks whether `chars` is a whitespace character."""
  # \t, \n, and \r are technically contorl characters but we treat them
  # as whitespace since they are generally considered as such.
  if char == " " or char == "\t" or char == "\n" or char == "\r":
    return True
  cat = unicodedata.category(char)
  if cat == "Zs":
    return True
  return False

def _is_control(char):
  """Checks whether `chars` is a control character."""
  # These are technically control characters but we count them as whitespace
  # characters.
  if char == "\t" or char == "\n" or char == "\r":
    return False
  cat = unicodedata.category(char)
  if cat in ("Cc", "Cf"):
    return True
  return False

def _is_punctuation(char):
  """Checks whether `chars` is a punctuation character."""
  cp = ord(char)
  
  if ((cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or
      (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126)):
    return True
  cat = unicodedata.category(char)
  if cat.startswith("P"):
    return True
  return False

if __name__ == '__main__':
  pre = albert_en_preprocess(r'C:\Users\User\Documents\predictor\data\vocab.csv',len_sequence=256)
  x = pre('india is the largest country in the world')
  print(x)
  albert = tf.saved_model.load(r'C:\Users\User\Documents\predictor\models\NewsReader\Albert_en\Albert_encoder')
  decoder = tf.saved_model.load(r'C:\Users\User\Documents\predictor\models\NewsReader\Albert_en\Decoder')
  y = decoder(albert(x)[0])
  print(tf.argmax(y,axis=-1)[0])
  print(pre.decode(tf.argmax(y,axis=-1)[0].numpy()))
