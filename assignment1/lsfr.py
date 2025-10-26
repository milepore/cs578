#start_state = 0b1001100001
# need to reverse the order of the bits in the start state to match the polynomial representation
start_state = 0b1000011001

lfsr = start_state
period = 0
bitstring = ""

while True:
    # polynomial is x^10 + x^3 + 1 ; taps at 10, 3
    # taps: 16 15 13 4; feedback polynomial: x^16 + x^15 + x^13 + x^4 + 1
    bit = (lfsr ^ (lfsr >> 7)) & 1
    
    lfsr = (lfsr >> 1) | (bit << 9)

    #print(f"bit: {bit} - lfsr: {lfsr:>010b}")
    #print(f"{bit}")
    if (period < 512):
        bitstring += f"{bit}"

    period += 1
    if lfsr == start_state:
        print("Period: ", period)
        break

print("First 512 bits: ", bitstring)

plaintext= "11101100000110111011010011111010"
key= bitstring[:len(plaintext)]
ciphertext = ''.join('1' if plaintext[i] != key[i] else '0' for i in range(len(plaintext)))
decrypttext = ''.join('1' if ciphertext[i] != key[i] else '0' for i in range(len(ciphertext)))

print("First 32 bits of stream: ", bitstring[:32])
print("Plaintext: ", plaintext)
print("Cyphertext: ", ciphertext)
print("Decrypted ciphertext: ", decrypttext)

assert(plaintext == decrypttext), "Decrypted text does not match original plaintext!"
