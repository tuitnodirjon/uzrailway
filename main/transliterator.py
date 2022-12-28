"""
Helper classes for our apps
Sources:
 - https://bitbucket.org/isehrob/moses_smt/src/master/moses_smt/helpers/helper_cls.py
 - https://bitbucket.org/isehrob/moses_smt/src/master/moses_smt/base/Transliterator.py
"""


class Transliterator:

    def __init__(self, orientation='crl2ltn'):
        self.orientation = orientation

    def lat_2_cyr(self, inp, trs):
        translited = []
        if not inp:
            return ""
        for word in inp.split():
            for i, l in enumerate(word):
                try:
                    if i == 0 and l in ['e', 'E']:
                        word = trs.e_disambugate(i, word)
                    elif word[i] in ['e', 'E']:
                        word = trs.e_replace(i, word)
                    elif word[i] and trs.is_sound(i, word):
                        old = word[i] + word[i + 1]
                        word = word.replace(old, trs.sounds[old], 1)
                    elif word[i] and trs.is_quote(i, word):
                        word = trs.quotate(i, word)
                    elif word[i] and trs.is_u(i, word):
                        old = word[i] + word[i + 1]
                        word = word.replace(old, trs.us[old], 1)
                    elif word[i]:
                        try:
                            word = word.replace(word[i], trs.alphabet[word[i]], 1)
                        except KeyError:
                            # raise
                            continue
                except IndexError:
                    # raise
                    break
            translited.append(word)
        return ' '.join(translited)

    def cyr_2_lat(self, inp, trs):
        translited = []
        if not inp:
            return ""
        for word in inp.split():
            for i, l in enumerate(word):
                try:
                    if i == 0 and l in ['е', 'Е']:
                        word = trs.e_disambugate(word)
                    else:
                        try:
                            word = word.replace(l, trs.alphabet[l], 1)
                        except KeyError:
                            continue
                except IndexError:
                    # raise
                    break
            translited.append(word)
        return ' '.join(translited)

    def trans(self, inp):
        if self.orientation == 'ltn2crl':
            return self.lat_2_cyr(inp, Cyrillic())
        elif self.orientation == 'crl2ltn':
            return self.cyr_2_lat(inp, Latinic())
        else:
            return False


class Cyrillic:
    alphabet = {
        "a": "а", "b": "б", "d": "д", "e": ["е", "э"], "f": "ф", "g": "г", "h": "ҳ", "i": "и", "j": "ж", "k": "к",
        "l": "л", "m": "м", "n": "н", "o": "о", "p": "п", "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в",
        "x": "х", "y": "й", "z": "з", "A": "А", "B": "Б", "D": "Д", "E": ["Е", "Э"], "F": "Ф",
        "G": "Г", "H": "Ҳ", "I": "И", "J": "Ж", "K": "К", "L": "Л", "M": "М", "N": "Н", "O": "О", "P": "П", "Q": "Қ",
        "R": "Р", "S": "С", "T": "Т", "U": "У", "V": "В", "X": "Х", "Y": "Й", "Z": "З",
    }

    sounds = {
        'yo': 'ё', 'yu': 'ю', 'ya': 'я', 'ye': 'е', 'Yo': 'Ё', 'Yu': 'Ю', 'Ya': 'Я', 'YA': 'Я', 'Ye': 'Е', "ch": "ч",
        "Сh": "Ч", "CH": "Ч", "sh": "ш", "SH": "Ш", "ng": "нг", "NG": "НГ", 'ts': "ц", 'TS': "Ц", "Sh": "Ш",
    }

    misc = {
        "'": [["ь", "ъ"], ["Ь", "Ъ"]],
        "’": [["ь", "ъ"], ["Ь", "Ъ"]],
    }

    us = {
        "G`": "Ғ", "O`": "Ў", "g`": "ғ", "o`": "ў", "G'": "Ғ", "O'": "Ў", "g'": "ғ", "o'": "ў",
        "G‘": "Ғ", "O‘": "Ў", "g‘": "ғ", "o‘": "ў",
    }

    vowels = ['a', 'o', 'i', 'u', "o'", 'e']

    def is_sound(self, i, inp):
        try:
            if inp[i] + inp[i + 1] in [x for x in self.sounds.keys()]:
                return True
        except IndexError:
            return False
        return False

    def is_u(self, i, inp):
        try:
            if inp[i] + inp[i + 1] in self.us.keys():
                return True
        except IndexError:
            return False
        return False

    def is_quote(self, i, inp):
        if inp[i] == "'" and inp[i - 1] not in ['o', 'O', 'g', 'G']:
            return True
        return False

    def quotate(self, i, inp):
        if inp[i - 1] in self.vowels:
            if inp.isupper():
                return inp.replace(inp[i], self.misc[inp[i]][1][1])
            else:
                return inp.replace(inp[i], self.misc[inp[i]][0][1])
        else:
            if inp.isupper():
                return inp.replace(inp[i], self.misc[inp[i]][1][0])
            else:
                return inp.replace(inp[i], self.misc[inp[i]][0][0])

    def e_disambugate(self, i, inp):
        return inp.replace(inp[i], self.alphabet[inp[i]][1], 1)

    def e_replace(self, i, inp):
        return inp.replace(inp[i], self.alphabet[inp[i]][0], 1)


class Latinic:
    alphabet = {
        'а': "a", 'б': "b", 'в': "v", 'г': "g", 'д': "d", 'е': "e", 'ё': "yo", 'ж': "j", 'з': "z", 'й': "y", 'и': "i",
        'к': "k", 'л': "l", 'м': "m", 'н': "n", 'о': "o", 'п': "p", 'р': "r", 'с': "s", 'т': "t", 'у': "u", 'ф': "f",
        'ц': "ts", 'ч': "ch", 'ш': "sh", 'ъ': "'", 'ь': "'", 'э': "e", 'ю': "yu", 'я': "ya", 'ў': "o`", 'қ': "q",
        'ғ': "g`", 'ҳ': "h",
        'А': "A", 'Б': "B", 'В': "V", 'Г': "G", 'Д': "D", 'Е': "E", 'Ё': "Yo", 'Ж': "J", 'З': "Z", 'Й': "Y", 'И': "I",
        'К': "K", 'Л': "L", 'М': "M", 'Н': "N", 'О': "O", 'П': "P", 'Р': "R", 'С': "S", 'Т': "T", 'У': "U", 'Ф': "F",
        'Ц': "TS", 'Ч': "Ch", 'Ш': "Sh", 'Ъ': "'", 'Ь': "'", 'Э': "E", 'Ю': "Yu", 'Я': "Ya", 'Ў': "O`", 'Қ': "Q",
        'Ғ': "G`", 'Ҳ': "H",
    }

    def e_disambugate(self, inp):
        if inp.isupper():
            return inp.replace(inp[0], 'Ye', 1)
        else:
            return inp.replace(inp[0], 'ye', 1)


class Lat2Cyr(Transliterator):

    def trans(self, inp):
        return self.lat_2_cyr(inp, Cyrillic())

    def detect(self, inp):
        # if true then this is latin text
        # and we need to transliterate it
        other = 0
        for chr in inp:
            if chr in Cyrillic.alphabet:
                other += 1
        return other / len(inp) > 0.5


class Cyr2Lat(Transliterator):

    def trans(self, inp):
        return self.cyr_2_lat(inp, Latinic())

    def detect(self, inp):
        # if true then this is cyrillic text
        # and we need to transliterate it
        other = 0
        for chr in inp:
            if chr in Latinic.alphabet:
                other += 1
        return other / len(inp) > 0.5
