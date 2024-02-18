from itertools import chain
import string
import re

rusconst = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_" #
#rusconst = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
engconst = "abcdefghijklmopqrstuvwxyz_" 
alphabetRus = {a[0]: a[1] for a in zip(rusconst, range(len(rusconst)))}
alphabetRusnms = {a[1]: a[0] for a in zip(rusconst, range(len(rusconst)))}
alphabetEn = {a[0]: a[1] for a in zip(string.ascii_uppercase, range(len(string.ascii_uppercase)))}
alphabetEn['_'] = 26
alphabetEnnms = {a[1]: a[0] for a in zip(string.ascii_uppercase, range(len(string.ascii_uppercase)))}
alphabetEnnms[26] = '_'

def rusFind(path): 
    alflen = len(alphabetRus)
    filer = open(path, encoding='utf-8')
    keyLen = int(filer.readline())
    massage = filer.readline()
    subalphabets = []
    subalflenth = []
    for i in range(keyLen):
        subalphabets.append({a[1]: 0 for a in alphabetRus.items()})
        subalflenth.append(0)
    for i in range(len(massage)):
        subalphabets[i % keyLen][alphabetRus[massage[i]]] += 1
        subalflenth[i % keyLen] += 1
    for i in subalphabets:
        print(i)
    print(subalflenth)
    moved = []
    for line in range(1, keyLen):
        moved.append([])
        for mv in range(1, alflen):
            sum = 0
            for i in range(alflen):
                ind = (i - mv) % alflen
                if ind < 0:
                    ind = alflen - ind
                sum += subalphabets[0][i] * subalphabets[line][ind]
            MIc = sum /(subalflenth[0] * subalflenth[line])
            if MIc < 0.07 and MIc > 0.053:
                moved[line-1].append([mv, MIc])
    for i in range(len(moved)):
        print(i, moved[i])
    passws = []
    itm = max(subalphabets[0].items(), key=lambda x: x[1])[0] + 1
    for variant in range(alflen):
        passw = alphabetRusnms[variant]
        for i in range(len(moved)):
            if len(moved[i]) >= 1:
                ind = variant - moved[i][0][0]
                if ind < 0:
                    ind = alflen + ind
                passw += alphabetRusnms[ind]
            else: break
        passws.append(passw)
    print(passws)
    print(passws[itm])
    return passws[itm]
        
def decoderus(path, key):
    alflen = len(alphabetRus)
    filer = open(path, encoding='utf-8')
    keyLen = int(filer.readline())
    massage = filer.readline()
    msj = ''
    for i in range(len(massage)):
        ind = (alphabetRus[massage[i]] - alphabetRus[key[i % keyLen]]) % alflen
        if ind < 0:
            ind = alflen - ind
        msj += alphabetRusnms[ind]
    print(msj)

def engFind(path): 
    alflen = len(alphabetEn)
    filer = open(path, encoding='utf-8')
    keyLen = int(filer.readline())
    massage = filer.readline().upper()
    subalphabets = []
    subalflenth = []
    for i in range(keyLen):
        subalphabets.append({a[1]: 0 for a in alphabetEn.items()})
        subalflenth.append(0)
    for i in range(len(massage)):
        subalphabets[i % keyLen][alphabetEn[massage[i]]] += 1
        subalflenth[i % keyLen] += 1
    for i in subalphabets:
        print(i)
    print(subalflenth)
    moved = []
    for line in range(1, keyLen):
        print("d")
        moved.append([])
        for mv in range(1, alflen):
            sum = 0
            for i in range(alflen):
                ind = (i - mv) % alflen
                if ind < 0:
                    ind = alflen - ind
                sum += subalphabets[0][i] * subalphabets[line][ind]
            MIc = sum /(subalflenth[0] * subalflenth[line])
            if MIc > 0.066:
                moved[line-1].append([mv, MIc])
    for i in range(len(moved)):
        print(i, moved[i])
    passws = []
    for variant in range(alflen):
        passw = alphabetEnnms[variant]
        for i in range(len(moved)):
            if len(moved[i]) >= 1:
                ind = variant - moved[i][0][0]
                if ind < 0:
                    ind = alflen + ind
                passw += alphabetEnnms[ind]
            else: break
        passws.append(passw)
    print(passws)
    itm = max(subalphabets[0].items(), key=lambda x: x[1])[0] + 1
    print(passws[itm])
    return passws[itm]
        
def decodeeng(path, key):
    alflen = len(alphabetEn)
    filer = open(path, encoding='utf-8')
    keyLen = int(filer.readline())
    massage = filer.readline().upper()
    msj = ''
    for i in range(len(massage)):
        ind = (alphabetEn[massage[i]] - alphabetEn[key[i % keyLen]]) % alflen
        if ind < 0:
            ind = alflen - ind
        msj += alphabetEnnms[ind]
    print(msj)

def findKeyLen(path, pathout):
    alflen = len(alphabetRus)
    filer = open(path, encoding='utf-8')
    massage = filer.readline().upper()
    msglen = len(massage)
    sameplaces = {}
    ind = 0
    while (ind + 3 ) < msglen:
        substrlen = 3
        reslen = 10
        while reslen > 3 and msglen - ind > substrlen:
            substr = massage[ind: ind + substrlen]
            result = [_.start() for _ in re.finditer(substr, massage)]
            reslen = len(result)
            if reslen > 3:
                sameplaces[substr] = result
            substrlen += 1
        ind += 1
    print(sameplaces)
    distances = {}
    for i in sameplaces:
        distances[i] = []
        for j in range(1, len(sameplaces[i])):
            distances[i].append(sameplaces[i][j] - sameplaces[i][j-1])
    diffvars = {}
    for i in distances:
        st = " ".join([str(i) for i in distances[i]])
        if not diffvars.get(st):
            diffvars[st] = 1
        else:
            diffvars[st] += 1
    print(diffvars)
    distance = max(diffvars.items(), key=lambda x: x[1])[0].split(" ")
    print(distance)
    nod = binaryGcd(int(distance[0]), int(distance[1]))
    for i in range(2, len(distance)):
        nod = binaryGcd(nod, int(distance[i]))
    print(nod)
    filew = open(pathout, 'w', encoding='utf-8')
    filew.write(str(int(nod)) + '\n')
    filew.write(massage)
    filew.close()

def binaryGcd(a, b):
    if a == b or b == 0 : 
        return a
    if a == 0 : 
        return b 
    if a % 2 == 0 :
        if b % 2 == 0 : 
            return binaryGcd(a / 2, b / 2) * 2
        else:
            return binaryGcd(a / 2, b)
    if b % 2 == 0 : 
        return binaryGcd(a, b / 2)
    if a > b : 
        return binaryGcd((a - b) / 2, b)
    return binaryGcd((b - a) / 2, a)


# engFind('inputeng.txt')
# decodeeng('inputeng.txt', 'fox')

#task 2:
# findKeyLen('inputfind.txt', 'input.txt')
# rusFind('input.txt')
#decoderus('input.txt', 'МИР')

# findKeyLen('inputfind.txt', 'inputeng.txt')
# engFind('inputeng.txt')
# decodeeng('inputeng.txt', 'sport')

#all in time rus
findKeyLen('C:/Users/mauro/OneDrive/Documents/Documentos universidad 5 semestre/CRYPTO/input.txt', 'C:/Users/mauro/OneDrive/Documents/Documentos universidad 5 semestre/CRYPTO/input2.txt')
word = rusFind('C:/Users/mauro/OneDrive/Documents/Documentos universidad 5 semestre/CRYPTO/input2.txt')
decoderus('C:/Users/mauro/OneDrive/Documents/Documentos universidad 5 semestre/CRYPTO/input2.txt', word)

#all in time eng
#findKeyLen('inputfind.txt', 'inputeng.txt')
#word = engFind('inputeng.txt')
#decodeeng('inputeng.txt', word)