# you can create custom tokenizer components based on your own custom algorithm
# for clarification purpose. I'm taking example script from hf tokenizers repo
# Here => https://github.com/huggingface/tokenizers/blob/main/bindings/python/examples/custom_components.py

from typing import List

import jieba
from tokenizers import NormalizedString, PreTokenizedString, Regex,
from tokenizers.decoders import Decoder
from tokenizers.models import BPE
from tokenizers.normalizers import Normalizer
from tokenizers.pre_tokenizers import PreTokenizer


class JiebaPreTokenizer:
    def jieba_split(self, i: int, normalized_string: NormalizedString) -> List[NormalizedString]:
        splits = []
        # we need to call `str(normalized_string)` because jieba expects a str,
        # not a NormalizedString
        for token, start, stop in jieba.tokenize(str(normalized_string)):
            splits.append(normalized_string[start:stop])

        return splits
        # We can also easily do it in one line:
        # return [normalized_string[w[1] : w[2]] for w in jieba.tokenize(str(normalized_string))]

    def odd_number_split(self, i: int, normalized_string: NormalizedString) -> List[NormalizedString]:
        # Just an odd example...
        splits = []
        last = 0
        for i, char in enumerate(str(normalized_string)):
            if char.isnumeric() and int(char) % 2 == 1:
                splits.append(normalized_string[last:i])
                last = i
        # Don't forget the last one
        splits.append(normalized_string[last:])
        return splits

    def pre_tokenize(self, pretok: PreTokenizedString):
        # Let's call split on the PreTokenizedString to split using `self.jieba_split`
        pretok.split(self.jieba_split)
        # Here we can call `pretok.split` multiple times if we want to apply
        # different algorithm, but we generally just need to call it once.
        pretok.split(self.odd_number_split)


class CustomDecoder:
    def decode(self, tokens: List[str]) -> str:
        return "".join(tokens)


class CustomNormalizer:
    def normalize(self, normalized: NormalizedString):
        # Most of these can be replaced by a `Sequence` combining some provided Normalizer,
        # (ie Sequence([ NFKC(), Replace(Regex("\s+"), " "), Lowercase() ])
        # and it should be the prefered way. That being said, here is an example of the kind
        # of things that can be done here:
        normalized.nfkc()
        normalized.filter(lambda char: not char.isnumeric())
        normalized.replace(Regex("\s+"), " ")
        normalized.lowercase()