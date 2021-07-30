#Teoria dos Numeros e Ciptografia 2021.1 - UNIFESP
#Daniel Barbosa Silva Costa 112185

from math import gcd
import string
import sys
import os

#conversion table day 0
conversionTable0 = {}
def createConversionTable0(tests):
    alphabet = list(string.ascii_uppercase)
    alphabet.append(' ')
    for key in range (len(alphabet)-1):
        conversionTable0[key+10] = alphabet[key]
    conversionTable0[99] = alphabet[key+1]
    for key in range (0, 10):
        conversionTable0[key] = '?'
    for key in range (36, 99):
        conversionTable0[key] = '?'
    for key in range (100, 1000):
        conversionTable0[key] = '?'
    if(tests == True):
        print("\nTabela de conversao dia 0 e 1")
        print (conversionTable0)

#conversion table day 2
conversionTable2 = {}
def createConversionTable2(tests):
    alphabet = list(string.ascii_uppercase)
    alphabet.append(' ')
    for key in range (len(alphabet)-1):
        conversionTable2[key+65] = alphabet[key]
    conversionTable2[11] = alphabet[key+1]
    for key in range (0, 11):
        conversionTable2[key] = '?'
    for key in range (12, 65):
        conversionTable2[key] = '?'
    for key in range (91, 1000):
        conversionTable2[key] = '?'
    if(tests == True):
        print("\nTabela de conversao dia 2")
        print (conversionTable2)

#(block of numbers decrypted, day of the mission)
def numbersToString(numbers, day):
    stringConverted = ''
    if (day == 0 or day == 1):
        for num in numbers:
            stringConverted+=conversionTable0[num]
    if (day == 2):
        for num in numbers:
            stringConverted+=conversionTable2[num]
    return stringConverted

#calculates the totient function
def phi(m):
    amtPrimesWithM = 0
    for i in range(1, m + 1):
            if gcd(m, i) == 1:
                amtPrimesWithM += 1
    return amtPrimesWithM


#calculates the modular multiplicative inverse: a * x = 1 (mod m) -> return x
def modInverse(a, m):
    for x in range(1, m):
        if (((a%m) * (x%m)) % m == 1):
            return x
    raise RuntimeError("15 nao é invertível para módulo 80!")

#RSA encoder
#encryption key (m, b)
def encodeRSA(m, b, rawBlocks):
    encryptedBlocks = []
    for blck in rawBlocks:
        encryptdBlck = (blck**b) % m
        encryptedBlocks.append(encryptdBlck)
    return encryptedBlocks

#RSA decoder
#decryption key (m, modInverseValue)
def decodeRSA(m, b, phi, encryptedBlocks):
    decryptedBlocks = []
    modInverseValue = modInverse(b, phi)
    for blck in encryptedBlocks:
        decryptdBlck = (blck**modInverseValue) % m
        decryptedBlocks.append(decryptdBlck)
    return decryptedBlocks

#RSA decoder
#decryption key (m, modInverseValue)
def decodeRSAwithPrivateKey(m, a, encryptedBlocks):
    decryptedBlocks = []
    for blck in encryptedBlocks:
        decryptdBlck = (blck**a) % m
        decryptedBlocks.append(decryptdBlck)
    return decryptedBlocks

#Tinia encode from
#Day 0
def tiniaTest(m, b, phi):
    print(">> Atividade 1 <<")
    tiniaBlocks = [29, 18, 23, 18, 10]
    tiniaEncrypted = encodeRSA(m, b, tiniaBlocks)
    tiniaDecrypted = decodeRSA(m, b, phi, tiniaEncrypted)
    print(tiniaBlocks, end = ' -> encode -> ')
    print(tiniaEncrypted, end = ' -> decode -> ')
    print(tiniaDecrypted)
    print(numbersToString(tiniaBlocks, 0), end = ' -> encode -> ')
    print(numbersToString(tiniaEncrypted, 0), end = ' -> decode -> ')
    print(numbersToString(tiniaDecrypted, 0))
    if(tiniaBlocks != tiniaDecrypted):
        raise RuntimeError("Sistema de criptografia e/ou descriptografia mal implementado!")
    else:
        print("Sistema de criptografia validado com sucesso!")
        print

def timeSent():
    diaEHora = []
    diaEHora.append(2630%30)
    diaEHora.append(1431%24)
    return  diaEHora

#Day 1
def day1(m, a, phi):
    print("\n>> Atividade 2 <<")
    encryptedBlocks = [147, 9, 140, 18, 147, 73, 207, 215, 140, 214, 215, 140, 73,
                        122, 222, 225, 23, 147, 29]
    numbersDecrypted = decodeRSAwithPrivateKey(m, a, encryptedBlocks)
    print('(SEQUENCIA CRIPTOGRAFADA)')
    print(encryptedBlocks)
    print('\n(SEQUENCIA DESCRIPTOGRAFADA)')
    print(numbersDecrypted)
    msgDecrypted = numbersToString(numbersDecrypted, 1)
    print("\nMensagem enviada:")
    print('Dia ' + str(timeSent()[0]) + ' às ' + str(timeSent()[1]) + 'horas')
    print(msgDecrypted)


#Day 2
def day2(m, a, phi):
    #first message sent
    print("\n>> Atividade 3 <<")
    encryptedBlocks = [175, 134, 175, 89, 175, 48, 176, 134, 176, 243, 228, 176, 134, 176,
                        243, 228, 176, 185, 101, 243, 243, 241, 176, 206, 228, 176, 212,
                        115, 48, 175, 228]
    numbersDecrypted = decodeRSAwithPrivateKey(m, a, encryptedBlocks)
    print('(SEQUENCIA CRIPTOGRAFADA)')
    print(encryptedBlocks)
    print('\n(SEQUENCIA DESCRIPTOGRAFADA)')
    print(numbersDecrypted)
    msgDecrypted = numbersToString(numbersDecrypted, 2)
    print("\nMensagem enviada:")
    print(msgDecrypted)
    #second message sent (use TIVIA public or secret key: private 247, 5)
    print("\n>> Atividade 4 <<")
    encryptedBlocks = [147, 29, 147, 225, 23, 147, 73, 147, 214, 73]
    numbersDecrypted = decodeRSAwithPrivateKey(247, 5, encryptedBlocks)
    print('\n(SEQUENCIA CRIPTOGRAFADA)')
    print(encryptedBlocks)
    print('\n(HORARIO CRIPTOGRAFADA)')
    print('[3033]')
    print('\n(SEQUENCIA DESCRIPTOGRAFADA)')
    print(numbersDecrypted)
    print('\n(HORARIO DESCRIPTOGRAFADO)')
    print('['+str(3033%24)+']')
    msgDecrypted = numbersToString(numbersDecrypted, 0)
    msgDecrypted+=str(3033%24)
    print("\nMensagem enviada:")
    print(msgDecrypted)


if __name__ == '__main__':

    original = sys.stdout
    outputFileName = 'result.txt'
    output = open(outputFileName,'w')
    sys.stdout = output

    print('Pyhton ' + str(sys.version)[:5] + '\n')

    tests = False

    #T55 mission days
    ########## Day 0 ##########
    #create conversion table from day 0
    createConversionTable0(tests)
    # m = pq = 247; b = 173 (public key)
    m0 = 247
    b0 = 173
    phi0 = phi(m0)
    #cryptography system test
    tiniaTest(m0, b0, phi0)

    ########## Day 1 ##########
    # m = pq = 247; a = 5 (private key)
    m1 = 247
    a1 = 5
    phi1 = phi(m1)
    day1(m1, a1, phi1)

    ########## Day 2 ##########
    # m = pq = 253; a = 7 (private key)
    createConversionTable2(tests)
    m2 = 253
    a2 = 7
    phi2 = phi(m2)
    day2(m2, a2, phi2)

    sys.stdout = original
    print('Resultados em ' + os.getcwd() + '\outputFileName')
    output.close()
