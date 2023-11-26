from src.randomized_iterative_affine_cipher import RandomizedIterativeAffineCipher
from time import time
round = 1
start_time = time()
for _ in range(round):
	key = RandomizedIterativeAffineCipher.generate_keypair(key_round=5)

	scale = -3.1
	a = 5.33
	c = -3.55
	scale_c = 2.5
	A = key.encrypt(a)
	B = A * scale
	b = key.decrypt(B)
	real_b = a * scale
	
	#print("real b = {}".format(real_b))
	#print("b = {}".format(b))
	
	R = scale * key.encrypt(a) + scale_c * key.encrypt(c)
	r = key.decrypt(R)
	real_r = scale * a + scale_c * c
end_time = time()
msTime = (end_time - start_time) * 1000
print("Time consumption: {0:.6f}ms / {1} = {2:.6f}us. ".format(msTime, round, msTime * 1000 / round))