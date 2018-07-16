"""
Created on  11 - July -2018

Author: HD
"""
import os
import re
from _ast import alias


import codecs
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

""" 
 Common Utilities

"""


def safeStr(obj):
    try: return str(obj)
    except UnicodeEncodeError:
        return obj.encode('utf-8', 'ignore')
        # return obj.encode('utf-8', 'ignore').decode('utf-8').strip()
    except:
        print str(obj)
        return obj.encode('ascii', 'ignore').decode('ascii')


def tupleToStr(aTuple):
    # return tuple([e.encode() if e else str(e) for e in aTuple])
    return tuple([safeStr(e).strip() if e else str(e) for e in aTuple])


def listOfTupleToTupleStr(aList):
    # return tuple([e.encode() if e else str(e) for e in aTuple])
    tmp_lst = []
    for aTuple in aList:
        for e in aTuple:
            tmp_lst.append(safeStr(e))
    return tmp_lst
    # return tuple([safeStr(e) if e else str(e) for e in aTuple for aTuple in aList])


def decode_tuple(aTuple, encoding="ascii"):
    return tuple([i.encode(encoding) for i in aTuple if i])
    # return map( lambda x: (x[0].encode("utf-8"),)+x[1:], row )


def question_sanitize(question):
    question = question.replace("'", "\'")
    question = question.replace("\"", "\\\"")
    
    return question

# def sanitize_characters(string, replace_invalid_with=ERROR):
#     try:
#         string.encode("utf-8")
#         if "\0" in string:
#             raise UnicodeEncodeError
#         yield string
#     except UnicodeEncodeError:
#         for character in string:
#             point = ord(character)
#
#             if point == 0:
#                 if replace_invalid_with is ERROR:
#                     raise ValueError("Identifier contains NUL character.")
#                 else:
#                     yield replace_invalid_with
#             elif 0xD800 <= point <= 0xDBFF:
#                 if replace_invalid_with is ERROR:
#                     raise ValueError("Identifier contains high-surrogate character.")
#                 else:
#                     yield replace_invalid_with
#             elif 0xDC00 <= point <= 0xDFFF:
#                 if replace_invalid_with is ERROR:
#                     raise ValueError("Identifier contains low-surrogate character.")
#                 else:
#                     yield replace_invalid_with
#
#             # elif (0xE000 <= point <= 0xF8FF or
#             #       0xF0000 <= point <= 0xFFFFD or
#             #       0x100000 <= point <= 0x10FFFD):
#             #     if replace_invalid_with is ERROR:
#             #         raise ValueError("Identifier contains private user character.")
#             #     else:
#             #         yield replace_invalid_with
#             # elif 0xFDD0 <= point <= 0xFDEF or (point % 0x10000) in (0xFFFE, 0xFFFF):
#             #     if replace_invalid_with is ERROR:
#             #         raise ValueError("Identifier contains non-character character.")
#             #     else:
#             #         yield replace_invalid_with
#             else:
#                 yield character


# def quote_identifier(identifier, replace_invalid_with=ERROR):
#     sanitized = "".join(sanitize_characters(identifier, replace_invalid_with))
#     return "\"" + sanitized.replace("\"", "\"\"") + "\""




"""
Functions to do encoding checkings.
"""

# import logging
# from quepy import settings
# logger = logging.getLogger("quepy.encodingpolicy")


def encoding_flexible_conversion(string, complain=False):
    """
    Converts string to the proper encoding if it's possible
    and if it's not raises a ValueError exception.
    If complain it's True, it will emit a logging warning about
    converting a string that had to be on the right encoding.
    """

    if isinstance(string, unicode):
        return string
    try:
        # ustring = string.decode(settings.DEFAULT_ENCODING)
        ustring = string.decode('utf-8')
    except UnicodeError:
        message = u"Argument must be unicode or {}"
        # raise ValueError(message.format(settings.DEFAULT_ENCODING))
        raise ValueError(message.format('utf-8'))
    if complain:
        print(u"Forced to guess the encoding of {!r}, please provide a unicode string instead".format(string))
        # logger.warning(u"Forced to guess the encoding of {!r}, please provide a unicode string instead".format(string))

    return ustring


def assert_valid_encoding(string):
    """
    If string it's not in a valid encoding it raises a
    ValueError exception.
    """

    if not isinstance(string, unicode):
        raise ValueError(u"Argument must be unicode")