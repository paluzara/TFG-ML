from enum import Enum
class idioma(Enum):
    ESP=0
    ENG=1




def get_idiomas():
    f = open("idiomas.txt", "r")
    idiomas = []

    with open("idiomas.txt", 'r') as f:
        for line in f:
            frases = line.split(";")
            idiomas.append(frases)
    return idiomas

f = open("idiomas.txt", "r")
idiomas = []

with open("idiomas.txt", 'r') as f:
    for line in f:
        frases = line.split(";")
        idiomas.append(frases)

