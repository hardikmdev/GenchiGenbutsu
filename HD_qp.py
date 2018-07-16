

import refo
from refo import Predicate, Literal, Star, Any, Group
from HD_utils import encoding_flexible_conversion

string = "What is your question ?"
# words = string.split()
# result = None
#     for word in words:
#         if result is None:
#             result = predicate(word)
#         else:
#             result += predicate(word)


def _predicate_sum_from_string(string, predicate):
    assert issubclass(predicate, Predicate)

    string = encoding_flexible_conversion(string)
    words = string.split()
    result = None
    for word in words:
        if result is None:
            result = predicate(word)
        else:
            result += predicate(word)

    return result


def Lemmas(string):
    """
    Returns a Predicate that catches strings
    with the lemmas mentioned on `string`.
    """
    return _predicate_sum_from_string(string, Lemma)