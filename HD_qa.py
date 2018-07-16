"""
Created on  12 - July -2018

Author: HD
"""

# Question-answering system, questions of the form "Who... ?"  to be translated.

# standard includes
from collections import defaultdict
import os
import re
import HD_db
import HD_utils

baseDir = 'D:\Myfolder\Study\py\ChatterBot'
db_name = 'sample.db'

db_path = os.path.join(baseDir, db_name)

wh_lst = ["what", "when", "where", "which", "who", "whom", "whose", "why", "why don't", "how"]

q_lst = [
    "What is OBCU ?",
    "What is OCC ?",
    "What is OCTYS ?",
    "What is OEE ?",
    "What is OHE ?",
    "What is OPS ?",
    "What is OSGD ?",
    "What is OSGD ?",
    "What is OSMES ?",
    "What is OSS ?",
    "What is OT_IMM ?",
    "What is OT_NUM ?",
    "What is OT_SIM ?",
    "What is OT_ZC ?",
    "What is OTF ?"
]

intent_response_dict = {
    "intro": ["This is a GST FAQ bot. One stop-shop to all your GST related queries"],
    "greet":["hey","hello","hi"],
    "goodbye":["bye","It was nice talking to you","see you","ttyl"],
    "affirm":["cool","I know you would like it"],
    "status":["success","querying"],
    "response":["Sorry I am not trained to do that yet..."]
}

def tokenize(question):
    """
    Return a list containing a tokenized form of `question`.  Works by
    lowercasing, splitting around whitespace, and stripping all
    non-alphanumeric characters.
    """
    return [re.sub(r"\W", "", x) for x in question.lower().split()]
    # return [re.sub(r"\W", "", x) for x in question.split()]


def quote_identifier(identifier):
    return b"\"" + identifier.replace(b"\"", b"\"\"") + b"\""


def remove_spurious_words(text):
    """
    Return `text` with spurious words stripped.  For example, Google
    includes the word "Cached" in many search summaries, and this word
    should therefore mostly be ignored.
    """
    spurious_words = ["Cached", "Similar","the"]
    for word in spurious_words:
        text = text.replace(word, "")
    return text


def translate_q_to_query(q_type = "What",lst = None):
    query_key = lst[0]
    query_str = db_obj.query_build(query_key)
    return query_str,query_key


def update_db_rank(query_key,up_or_down):
    query_str = db_obj.update_query_build(query_key,up_or_down)


def process_question_list(cq_lst):
    if cq_lst[0] in wh_lst :
        q_type = wh_lst.index(cq_lst[0])
        # Assumin question is always "what is type, so
        query_str,query_key = translate_q_to_query(q_type,cq_lst[2:])
        result = db_obj.db_post_query(query_str)
        print ("Answer :")
        print (result)
        for str in result:
            print (HD_utils.safeStr(str[0]) + " : " +  HD_utils.safeStr(str[1]))
            answer = raw_input("Appropriate Answer?: ")
            if answer == "Yes" or answer == "yes":
                # data.execute("UPDATE sample SET rank = rank + 1 WHERE key=?", [inpt])
                db_obj.update_query_build(query_key,HD_utils.safeStr(str[3]),"+")
            if answer == "No" or answer == "no":
                # data.execute("UPDATE sample SET rank = rank - 1 WHERE key=?", [inpt])
                db_obj.update_query_build(query_key,HD_utils.safeStr(str[3]),"-")

    else:
        result = "Sorry, I didn't understand ! Could you Rephrase?"
        print (result)

    return result


def chat():
    while True:
        c_q = raw_input("Hello, What's your question?\n")
        if c_q == 'QUIT':
            break
        else:
            c_q_lst = tokenize(remove_spurious_words(c_q))
            c_ans = process_question_list(c_q_lst)


if __name__ == "__main__":
    print("Genchi Genbutsu \n")

    db_obj = HD_db.SqlLiteDb(db_path)
    chat()
    # while (1):
    # c_q = raw_input("Hello, What's your question?\n")
    # c_q_lst=tokenize(remove_spurious_words(c_q))
    # c_ans= process_question_list(c_q_lst)

