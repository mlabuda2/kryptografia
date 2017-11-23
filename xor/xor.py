"""

Program xor.py szyfruje
przygotowuje tekst oraz łamie kryptogram
zaszyfrowany metodą klucza jednorazowego(XOR).

Domyślna ilość linii do którego przycinany jest
tekst po funkcji prepare() to 30 linii. Możesz
zmienić to podając liczbę jako 2 parametr uruchamiania.
Przykład: python3 xor.py -p 40

Pierwszy parametr uruchamiania:
-p -> przygotowuje tekst i zapisuje do plain.txt
-e -> szyfruje tekst i zapisuje do crypto.txt
-k -> łamie szyfr bez klucza i zapisuje w decrypt.txt

Łamanie szyfru polega na znalezieniu spacji w
kryptogramie, dzięki czemu można znaleźć klucz którym
zaszyfrowana została dana kolumna tekstu.
Jeśli w kolumnie nie ma spacji to nie uda się rozszyfrować
kryptogramu.

Mateusz Labuda
Nr indeksu: 243 689
ROK 2017, LISTOPAD

"""


import sys

def fileRead(name):
    file = open(name, 'r')
    return file.read()

def fileWrite(name, saveText):
    file = open(name, 'w')
    file.write(saveText)

def printArr(arr, row, col):
    for r in range(0, row):
        for c in range(0, col):
            print(arr[r][c])

def clearFile(file):
    toClear = open(file, 'w')
    toClear.write('')




class Xor:

    def __init__(self):
        self.iloscLinii = 30
        self.iloscZnakow = self.iloscLinii * 35
        self.iloscZnakowBin = self.iloscZnakow * 8

    def setLine(self, linie):
        self.iloscLinii = linie
        self.iloscZnakow = self.iloscLinii * 35
        self.iloscZnakowBin = self.iloscZnakow * 8


    def prepare(self):
        orig = fileRead('orig.txt')
        text = ''
        for line in orig:
            line = line.lower()
            for i in line:
                if ((ord(i) < 32 or ord(i) > 32) and (ord(i) < 97 or ord(i) > 122)):
                    i = i.replace(i, "")
                    text += i
                else:
                    text += i
        i = 0
        prepared = ''
        ltext = len(text)
        if (ltext > self.iloscZnakow):
            ltext = self.iloscZnakow
        elif (ltext < self.iloscZnakow):
            print("\nChcę tekst dlugosci conajmniej 700 znakow!\n")
            sys.exit(1)

        # Dziele na substringi
        while (i < ltext):
            prepared += text[i:i + 35]
            i += 35
            if (i < self.iloscZnakow):
                prepared += '\n'
        # print(prepared)

        fileWrite('plain.txt', prepared)
        print("\nZapisano przygotowany tekst do plain.txt")

    def xor(self, content, key):
        klen = len(key)
        decoded = ''
        i = 0

        for line in content:
            for c in line:
                if(c == '\n'): break
                xorbin = ord(c) ^ ord(key[i])
                xorbin = '{0:08b}'.format(xorbin)
                i += 1
                i = i % klen
                decoded += xorbin
                # decoded += '\n'
            # decoded += '\n'
        print("\nSzyfr zapisano w 'crypto.txt'.\n")
        return decoded

    def toArr(self, text):
            binArr = [[] for y in range(self.iloscLinii)]
            z = 0
            for i in range(0, self.iloscLinii):
                while(z < self.iloscZnakowBin):
                    binArr[i].append(text[z:z+8])
                    z += 8
                    if(len(binArr[i]) == 35):
                        break
            return binArr

    def findSpace(self, array):
        try:
            spacje = [[0 for x in range(35)] for y in range(self.iloscLinii)]
            for row in range(0, self.iloscLinii):
                for i in range(0, 33):
                    a = int(array[row][i], 2)
                    b = int(array[row][i+1], 2)
                    c = int(array[row][i+2], 2)
                    xorek1 = a ^ b
                    xorek2 = b ^ c
                    xorek1 = '{0:08b}'.format(xorek1)
                    xorek2 = '{0:08b}'.format(xorek2)
                    if( xorek1[0:3] == '010' and xorek2[0:3] == '010' ):
                        # print("ten znak w plain w wierszu %d to spacja: %d" %(row, (i+1)))
                        spacje[row][i+1] = 'spacja'
                    if( i == 0 and xorek1[0:3] == '010' and xorek2[0:3] != '010' ):
                        # print("ten znak w plain w wierszu %d to spacja: 0" %row)
                        spacje[row][0] = 'spacja'
                    if(i == 32 and  xorek1[0:3] != '010' and xorek2[0:3] == '010' ):
                        # print("ten znak w plain w wierszu %d to spacja: 34" %row)
                        spacje[row][34] = 'spacja'
            return spacje

        except ValueError:
            print("\nWywołaj program z takim samym argumentem jak przy '-p'!\n")
            sys.exit(1)


    def decryptCol(self, spacje, lista, x):
        doneArr = [0 for x in range(35)]
        decrypted = ['' for x in range(self.iloscLinii)]
        for col in range(0, 35):
            for row in range(0, self.iloscLinii):
                if(spacje[row][col] == 'spacja'):
                    if(doneArr[col] == 'done' ):break
                    doneArr[col] = 'done'
                    a = int(lista[row][col], 2) # sxorowana kluczem spacja
                    # for i in range(0, 20):
                    b = int(lista[x][col], 2) # przyrownuj po kolei
                    xorek = a ^ b
                    xorek = '{0:08b}'.format(xorek)
                    if(xorek == '01000001'):
                        print("znak %d w wierszu %d to 'a'" %(col, x))
                        decrypted[x] = decrypted[x] + 'a'
                    if(xorek == '01000010'):
                        print("znak %d w wierszu %d to 'b'" %(col, x))
                        decrypted[x] = decrypted[x] + 'b'
                    if(xorek == '01000011'):
                        print("znak %d w wierszu %d to 'c'" %(col, x))
                        decrypted[x] = decrypted[x] + 'c'
                    if(xorek == '01000100'):
                        print("znak %d w wierszu %d to 'd'" %(col, x))
                        decrypted[x] = decrypted[x] + 'd'
                    if(xorek == '01000101'):
                        print("znak %d w wierszu %d to 'e'" %(col, x))
                        decrypted[x] = decrypted[x] + 'e'
                    if(xorek == '01000110'):
                        print("znak %d w wierszu %d to 'f'" %(col, x))
                        decrypted[x] = decrypted[x] + 'f'
                    if(xorek == '01000111'):
                        print("znak %d w wierszu %d to 'g'" %(col, x))
                        decrypted[x] = decrypted[x] + 'g'
                    if(xorek == '01001000'):
                        print("znak %d w wierszu %d to 'h'" %(col, x))
                        decrypted[x] = decrypted[x] + 'h'
                    if(xorek == '01001001'):
                        print("znak %d w wierszu %d to 'i'" %(col, x))
                        decrypted[x] = decrypted[x] + 'i'
                    if(xorek == '01001010'):
                        print("znak %d w wierszu %d to 'j'" %(col, x))
                        decrypted[x] = decrypted[x] + 'j'
                    if(xorek == '01001011'):
                        print("znak %d w wierszu %d to 'k'" %(col, x))
                        decrypted[x] = decrypted[x] + 'k'
                    if(xorek == '01001100'):
                        print("znak %d w wierszu %d to 'l'" %(col, x))
                        decrypted[x] = decrypted[x] + 'l'
                    if(xorek == '01001101'):
                        print("znak %d w wierszu %d to 'm'" %(col, x))
                        decrypted[x] = decrypted[x] + 'm'
                    if(xorek == '01001110'):
                        print("znak %d w wierszu %d to 'n'" %(col, x))
                        decrypted[x] = decrypted[x] + 'n'
                    if(xorek == '01001111'):
                        print("znak %d w wierszu %d to 'o'" %(col, x))
                        decrypted[x] = decrypted[x] + 'o'
                    if(xorek == '01010000'):
                        print("znak %d w wierszu %d to 'p'" %(col, x))
                        decrypted[x] = decrypted[x] + 'p'
                    if(xorek == '01010001'):
                        print("znak %d w wierszu %d to 'q'" %(col, x))
                        decrypted[x] = decrypted[x] + 'q'
                    if(xorek == '01010010'):
                        print("znak %d w wierszu %d to 'r'" %(col, x))
                        decrypted[x] = decrypted[x] + 'r'
                    if(xorek == '01010011'):
                        print("znak %d w wierszu %d to 's'" %(col, x))
                        decrypted[x] = decrypted[x] + 's'
                    if(xorek == '01010100'):
                        print("znak %d w wierszu %d to 't'" %(col, x))
                        decrypted[x] = decrypted[x] + 't'
                    if(xorek == '01010101'):
                        print("znak %d w wierszu %d to 'u'" %(col, x))
                        decrypted[x] = decrypted[x] + 'u'
                    if(xorek == '01010110'):
                        print("znak %d w wierszu %d to 'v'" %(col, x))
                        decrypted[x] = decrypted[x] + 'v'
                    if(xorek == '01010111'):
                        print("znak %d w wierszu %d to 'w'" %(col, x))
                        decrypted[x] = decrypted[x] + 'w'
                    if(xorek == '01011000'):
                        print("znak %d w wierszu %d to 'x'" %(col, x))
                        decrypted[x] = decrypted[x] + 'x'
                    if(xorek == '01011001'):
                        print("znak %d w wierszu %d to 'y'" %(col, x))
                        decrypted[x] = decrypted[x] + 'y'
                    if(xorek == '01011010'):
                        print("znak %d w wierszu %d to 'z'" %(col, x))
                        decrypted[x] = decrypted[x] + 'z'
                    if(xorek == '00000000'):
                        print("znak %d w wierszu %d to ' '" %(col, x))
                        decrypted[x] = decrypted[x] + ' '
        return decrypted

    def analyze(self, space, binList):
        for i in range(0, self.iloscLinii):
            decrypt = self.decryptCol(space, binList, i)
            with open("decrypt.txt", "a") as decryptFile:
                decryptFile.write(decrypt[i])
                decryptFile.write('\n')
        decryptFile.close()

class Main(Xor):

    def main(self, argv):
        if (len(argv) > 1): # do tego potrzebowałem klase
            # xc = Xor(argv[1])
            lines = int(argv[1])
            super().setLine(lines)
        # else:
        #     xc = Xor()

        key = fileRead('key.txt')
        if argv[0] == "-e":
            plain = fileRead('plain.txt')
            encoded = super().xor(plain, key)
            fileWrite('crypto.txt', encoded)
        elif argv[0] == "-p":
            # if (argv[1]): xc.iloscLinii = argv[1]  # do tego potrzebowałem klase
            super().prepare()
        elif argv[0] == "-k":
            clearFile('decrypt.txt')
            crypted = fileRead('crypto.txt')
            binList = super().toArr(crypted) #dwuwymiarowa lista [20][35] (20 linii po 35 znakow) zawietra xory binarne kazdego znaku
            space = super().findSpace(binList) #dwuwymiarowa lista jw. zawiera 'spacja' gdy jest spacja w tym miesjcu lub 0
            super().analyze(space, binList)
        else:
            print("\nPodano zły parametr/argument!\n")
            sys.exit(1)

if __name__ == "__main__":
    print("\nProgram przygotowuje tekst, szyfruje go i łamie szyfr.\nFunkcje -p możesz wywołać z argumentem ilości linii tekstu.\nPrzyklad: python3 xor.py -p 20 (domyslnie 30). ")
    start = Main()
    start.main(sys.argv[1:])
