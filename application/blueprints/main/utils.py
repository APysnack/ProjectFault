import re
import string


def validateInput(name, pw):
    name = name.replace(" ", "")
    pw = pw.replace(" ", "")
    p = re.compile("[" + re.escape(string.punctuation) + "]")
    name = p.sub("", name)
    if ((4 <= len(name) <= 20) and (6 <= len(pw) <= 20)):
        return name, pw, True
    else:
        return name, pw, False
