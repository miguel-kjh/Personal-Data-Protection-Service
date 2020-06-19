from app.main.util.fileUtils import isDni

import random

def encode(text: str) -> str:
    return "*" * len(text)

def markInHtml(text: str) -> str:
    return '<mark style="background: #7aecec;">' + text + '</mark>'

def disintegration(text:str) -> str:
    if isDni(text):
        chars      = list(text)
        chars[0:3] = 3*'*'
        chars[7:]  = 2*'*'
        return ''.join(chars)
    else:
        return encode(text)

def dataObfuscation(text:str) -> str:
    if isDni(text):
        chars      = list(text)
        chars[1:7] = 7*'*'
        return ''.join(chars)
    else:
        result = map(
            lambda name: '%s%s' %(name[0],len(name[1:])*'*'),
            text.split()
        )
        return ' '.join(result)