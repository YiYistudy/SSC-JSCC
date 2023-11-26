from src.randomized_iterative_affine_cipher import RandomizedIterativeAffineCipher

key = RandomizedIterativeAffineCipher.generate_keypair(key_round=5)

plaintexts = [3, 96, 93, 93, 2, 67, 88, 5, 95, 70, 73, 55, 92, 1,  85]
ciphertexts = []

for plaintext in plaintexts:
    ciphertexts.append(key.encrypt(plaintext))

pass
