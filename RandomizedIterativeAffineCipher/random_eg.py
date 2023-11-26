import random

from src.randomized_iterative_affine_cipher import RandomizedIterativeAffineCipher

key = RandomizedIterativeAffineCipher.generate_keypair(key_round=3, encode_precision=1)

plaintexts = [random.randrange(0, 10000) for _ in range(100)]
real_sum = sum(plaintexts)

ciphertexts = []
for i in range(len(plaintexts)):
    ciphertexts.append(key.encrypt(plaintexts[i]))
cipher_sum = key.encrypt(0)
for i in range(len(ciphertexts)):
    cipher_sum += ciphertexts[i]

computed_sum = key.decrypt(cipher_sum)

pass
