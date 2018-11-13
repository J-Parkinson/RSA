from random import randint
from math import sqrt, ceil, log, floor

#These are the private keys the bank uses
bankPrime1 = 6619319052850372576671203008980947142174030778088896832879139788043990604607
bankPrime2 = 89981040860183284202926925086489690550566335265876097787978356913003610730551
#This is the public key
clientPrime1 = 0
clientPrime2 = 0

#FOR FUNCTIONALITY
bankPrime = bankPrime1
clientPrime = bankPrime2

#Calculate modulus
modulus = bankPrime * clientPrime

#Calculate totient of modulus
totient = (bankPrime - 1)*(clientPrime - 1)

#Creates random numbers until it passes Euclid's algorithm with the GCD being 1 - coprime generator

def XGCD(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0

while True:
    pubkeyexponent = randint(3, ceil(sqrt(totient)))
    gcd, prikeyexponent = XGCD(pubkeyexponent, totient)
    if prikeyexponent < 0:
        prikeyexponent += totient
    if gcd == 1:
        break

print("Totient n", totient)
print("Private Key d", prikeyexponent)
print("Public Key e", pubkeyexponent)
print("Modulus", modulus)
print()
print("Type the message you want to encrypt:")
message = input(">:")

encrypted = 0
for x in range(len(message)):
    encrypted += (256**x) * ord(message[x])
print(encrypted)

networkmessage = pow(encrypted, pubkeyexponent, modulus)
print("The number message sent over the network to the bank is this:", networkmessage)
encrypted = pow(networkmessage, prikeyexponent, modulus)
print("The number message sent back to the client is this:", encrypted)

length = ceil(log(encrypted, 256))
decrypted = ""
for x in range(length-1, -1, -1):
    num = floor(encrypted / (256**x))
    decrypted = chr(num) + decrypted
    encrypted -= (num * (256**x))
print(decrypted)
