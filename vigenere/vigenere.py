"""
Program
- przygotowuje (func prepare())
- szyfruje  (func encrypt())
- deszyfruje (func decrypt())
- znajduje długość klucza (func ioc())
- wykonuje kryptoanalizę (func crack()) (oraz kilka funkcji wspomagających)
na podstawie szyfrogramu oraz długości klucza.

Projekt wykonał:
Mateusz Labuda - 10.2017
Nr indeksu: 243 689
"""

from collections import defaultdict
from itertools import cycle
import functools
import sys
from operator import itemgetter

ALPHA = 'abcdefghijklmnopqrstuvwxyz'

# Average letter occurence chances in English text.
p = {
    'A': .082, 'B': .015, 'C': .028, 'D': .043,
    'E': .127, 'F': .022, 'G': .020, 'H': .061,
    'I': .070, 'J': .002, 'K': .008, 'L': .040,
    'M': .024, 'N': .067, 'O': .075, 'P': .019,
    'Q': .001, 'R': .060, 'S': .063, 'T': .091,
    'U': .028, 'V': .010, 'W': .023, 'X': .001,
    'Y': .020, 'Z': .001
}


def fileRead(name):
    file = open(name, 'r')
    return file.read()

def fileWrite(name, saveFile):
    file = open(name, 'w')
    file.write(saveFile)

def prepare():
    orig = open("orig.txt", "r")
    plain = open("plain.txt", "w")
    text = ''
    for line in orig:
        line = line.lower()
        for i in line:
            if(ord(i) < 97 or ord(i) > 122):
                i = i.replace( i, "")
                text += i
            else:
                text += i
    plain.write(text)
    print("\nZapisano przygotowany tekst do plain.txt")


class Vigenere:

    def __init__(self):
        self.ciph = fileRead('crypto.txt')
        self.setAlphabet()


    def crack(self, cipher, m):
        cipher = cipher.upper()

        # Utworzenie grupek szyfru(ilość grupek zależy od key_length)
        y = defaultdict(list)
        for i, char in enumerate(cipher):       #enumerate tworzy liste tupli: [(0, 'z'), (1, 's')...]
            y[i % m].append(char)

        # analiza sekcji osobno
        for si in range(len(y)):
            section = y[si]
            section_len = len(section)

            # policzenie liter. Tworzy c-> słownik liter i liczy wystąpienia
            c = dict((key, 0) for key in p) #for key in p: dict((key, 0)
            for char in section:
                c[char] += 1

            # udziały liter - Ilość wystąpień / ilość całkowitą liter w sekcji
            h = dict((key, float(c[key]) / section_len) for key in c)

            # main
            gs = []
            for g in range(26):
                r = 0
                letter_g = chr(g + 65)
                for i in range(26):
                    p_i = p[chr(i + 65)]
                    h_ig = h[chr(((i + g) % 26) + 65)]
                    r += p_i * h_ig
                gs.append((letter_g, r))

            # wyciagnij najlepiej pasujaca wartosc
            desirable = .065
            nearest_value = 999
            nearest_index = 0
            for i, g in enumerate(gs):
                difference = abs(desirable - g[1])
                if difference < nearest_value:
                    nearest_value = difference
                    nearest_index = i
            yield gs[nearest_index][0]


    def encrypt(self, key, plaintext):
        pairs = zip(plaintext, cycle(key))  # cycle('ABCD') --> A B C D A B C D ...
        # print(list(pairs))  # zip tworzy liste tupli-> [(1,2),(3,5).. w Python 2 tworzy liste w Python 3 iterable obj
        result = ''
        for pair in pairs:
            total = functools.reduce(lambda x, y: ALPHA.index(x) + ALPHA.index(y), pair)
            result += ALPHA[total % 26]
        print("\nZapisano zaszyfrowany tekst do crypto.txt")
        return result.lower()


    def decrypt(self, key, ciphertext):
        pairs = zip(ciphertext, cycle(key))
        result = ''
        for pair in pairs:
            total = functools.reduce(lambda x, y: ALPHA.index(x) - ALPHA.index(y), pair)
            result += ALPHA[total % 26]
        print("\nZapisano odszyfrowany tekst do decrypt.txt")
        return result


    def analyze(self, cipher, kw_len):
        print('Cracking the Vigenere cipher.\n')
        keyword = ''.join(self.crack(cipher, kw_len))
        keyword = keyword.lower()
        print(' -> Znaleziony klucz: "%s"\n' % keyword)
        fileWrite('key-crypto.txt', keyword)
        print("Nowy klucz zapisano do key-crypto.txt")


    def ioc(self, guess):
        self.makeSubstrings(guess)
        self.avg = 0.0
        # print("Substrings: ")
        # print(", ".join(self.substrings))
        # print("Average index of coincidences: ")
        for i in range(guess):
            self.iocCalc(self.substrings[i])
            self.avg += self.result
        self.avg = self.avg / float(guess)
        print(self.avg)

    def makeSubstrings(self, guess):
        self.substrings = [''] * guess
        for i in range(len(self.ciph)):
            self.substrings[(i % guess)] = self.substrings[(i % guess)] + self.ciph[i]


    def iocCalc(self, text):
        count = self.makecount(text)
        strLength = len(text)
        self.result = 0
        for letter, nr in count:
            self.result = self.result + (nr * (nr - 1))
        divisor = (strLength * (strLength - 1))
        self.result = float(float(self.result) / float(divisor))

    def makecount(self, text=""):
        if (text == ""):
            text = self.ciph
        count = []
        for char in self.alphabet:
            count.append([char, self.numberOfInstances(text, char)])
        count.sort(key=itemgetter(1), reverse=True)
        return count

    # number of instances of a letter or small phrase (th, the, etc...) in a text
    def numberOfInstances(self, ciph, phrase):
        num = 0
        lenarray = len(ciph) - len(phrase)  # to not end up outside array
        for i in range(lenarray):
            if (ciph[i:(i + len(phrase))]) == phrase:
                num = num + 1
        return num

    def setAlphabet(self):
        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t", "u", "v", "w", "x", "y", "z"]

    def analyzeKeyLength(self, ciph):
        self.highest = 0
        for i in range(2, 11):
            print("IOC dla klucza długości %d wynosi: " % i)
            self.ioc(i)
            if self.avg > self.highest:
                self.highest = self.avg
                self.foundKeyLength = i
        print(self.highest)
        print("Znaleziona długość klucza to: %d" % self.foundKeyLength)
        self.analyze(ciph, self.foundKeyLength)


def main(argv):
    vg = Vigenere()
    key = fileRead('key.txt')
    if argv[0] == "-e":
        plain = fileRead('plain.txt')
        crypted = vg.encrypt(key, plain)
        fileWrite('crypto.txt', crypted)
    if argv[0] == "-d":
        crypted = fileRead('crypto.txt')
        decrypted = vg.decrypt(key, crypted)
        fileWrite('decrypt.txt', decrypted)
    if argv[0] == "-p":
        prepare()
    # if argv[0] == "-l":
    #     crypted = fileRead('crypto.txt')
    #     vg.analyzeKeyLength(crypted)
    if argv[0] == "-k":
        crypted = fileRead('crypto.txt')
        vg.analyzeKeyLength(crypted)

if __name__ == "__main__":
    main(sys.argv[1:])


