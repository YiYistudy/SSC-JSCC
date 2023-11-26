from sys import argv, exit
import heapq
from collections import defaultdict
from time import sleep, time
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
defaultTime = 3
round = 10000


# handle Huffman #
class HuffmanNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None
	def __lt__(self, other):
		return self.freq < other.freq

def build_huffman_tree(data):
	freq_map = defaultdict(int)
	for char in data:
		freq_map[char] += 1
	pq = []
	for char, freq in freq_map.items():
		node = HuffmanNode(char, freq)
		heapq.heappush(pq, node)
	while len(pq) > 1:
		left = heapq.heappop(pq)
		right = heapq.heappop(pq)
		merge_node = HuffmanNode(None, left.freq + right.freq)
		merge_node.left = left
		merge_node.right = right
		heapq.heappush(pq, merge_node)
	return pq[0]

def generate_codes(node, code, codes):
	if node.char is not None:
		codes[node.char] = code
	else:
		generate_codes(node.left, code + "0", codes)
		generate_codes(node.right, code + "1", codes)

def huffman_encode(data):
	codes = {}
	root = build_huffman_tree(data)
	generate_codes(root, "", codes)
	encoded_data = ""
	for char in data:
		encoded_data += codes[char]
	return encoded_data, codes

def huffman_decode(encoded_data, codes):
	decoded_data = ""
	current_code = ""
	for bit in encoded_data:
		current_code += bit
		for char, code in codes.items():
			if code == current_code:
				decoded_data += char
				current_code = ""
				break

	return decoded_data


# handle channel #
def channel_encode(x, series):
	binX = [0 if ch == '0' else 1 for ch in x]
	binarySeries = [0 if ch == '0' else 1 for ch in series]
	x_length = len(binX)
	series_length = len(binarySeries)
	min_length = min(x_length, series_length)
	return "".join(['0' if bt == 0 else '1' for bt in [binX[i % x_length] ^ binarySeries[i % series_length] for i in range(x_length)]])

def channel_decode(x, series):
	binX = [0 if ch == '0' else 1 for ch in x]
	binarySeries = [0 if ch == '0' else 1 for ch in series]
	x_length = len(binX)
	series_length = len(binarySeries)
	min_length = min(x_length, series_length)
	return "".join(['0' if bt == 0 else '1' for bt in [binX[i % x_length] ^ binarySeries[i % series_length] for i in range(x_length)]])


# handle modulate #
def modulate(x, modulation_scheme):
	bits = [0 if ch == '0' else 1 for ch in x]
	if modulation_scheme == "BPSK":
		symbols = [-1 if bit == 0 else 1 for bit in bits]
	elif modulation_scheme == "QPSK":
		symbols = []
		for i in range(0, len(bits), 2):
			bit1 = bits[i]
			bit2 = bits[i + 1]
			if bit1 == 0 and bit2 == 0:
				symbols.append(-1-1j)
			elif bit1 == 0 and bit2 == 1:
				symbols.append(-1+1j)
			elif bit1 == 1 and bit2 == 0:
				symbols.append(1-1j)
			elif bit1 == 1 and bit2 == 1:
				symbols.append(1+1j)
	elif modulation_scheme == "16QAM":
		symbols = []
		for i in range(0, len(bits), 4):
			bit1 = bits[i]
			bit2 = bits[i + 1]
			bit3 = bits[i + 2]
			bit4 = bits[i + 3]
			if bit1 == 0 and bit2 == 0 and bit3 == 0 and bit4 == 0:
				symbols.append(-3-3j)
			elif bit1 == 0 and bit2 == 0 and bit3 == 0 and bit4 == 1:
				symbols.append(-3-1j)
			elif bit1 == 0 and bit2 == 0 and bit3 == 1 and bit4 == 0:
				symbols.append()
			elif bit1 == 0 and bit2 == 0 and bit3 == 1 and bit4 == 1:
				symbols.append()
			elif bit1 == 0 and bit2 == 1 and bit3 == 0 and bit4 == 0:
				symbols.append()
			elif bit1 == 0 and bit2 == 1 and bit3 == 0 and bit4 == 1:
				symbols.append()
			elif bit1 == 0 and bit2 == 1 and bit3 == 1 and bit4 == 0:
				symbols.append()
			elif bit1 == 0 and bit2 == 1 and bit3 == 1 and bit4 == 1:
				symbols.append()
			elif bit1 == 1 and bit2 == 0 and bit3 == 0 and bit4 == 0:
				symbols.append()
			elif bit1 == 1 and bit2 == 0 and bit3 == 0 and bit4 == 1:
				symbols.append()
			elif bit1 == 1 and bit2 == 0 and bit3 == 1 and bit4 == 0:
				symbols.append()
			elif bit1 == 1 and bit2 == 0 and bit3 == 1 and bit4 == 1:
				symbols.append()
			elif bit1 == 1 and bit2 == 1 and bit3 == 0 and bit4 == 0:
				symbols.append()
			elif bit1 == 1 and bit2 == 1 and bit3 == 0 and bit4 == 1:
				symbols.append()
			elif bit1 == 1 and bit2 == 1 and bit3 == 1 and bit4 == 0:
				symbols.append(3+1j)
			elif bit1 == 1 and bit2 == 1 and bit3 == 1 and bit4 == 1:
				symbols.append(3+3j)
	else:
		raise ValueError("Unsupported modulation scheme")
	return symbols

def demodulate(symbols, modulation_scheme):
	bits = []
	if modulation_scheme == "BPSK":
		for symbol in symbols:
			bit = 0 if symbol < 0 else 1
			bits.append(bit)
	elif modulation_scheme == "QPSK":
		for symbol in symbols:
			if symbol == -1-1j:
				bits.extend([0, 0])
			elif symbol == -1+1j:
				bits.extend([0, 1])
			elif symbol == 1-1j:
				bits.extend([1, 0])
			elif symbol == 1+1j:
				bits.extend([1, 1])
	elif modulation_scheme == "16QAM":
		for symbol in symbols:
			if symbol.real < -2:
				bits.extend([0, 0, 0, 0])	
			elif symbol.real < 0:
				if symbol.imag < -2:
					bits.extend([0, 0, 1, 0])
				elif symbol.imag < 0:	
					bits.extend([0, 0, 1, 1])
				elif symbol.imag < 2:
					bits.extend([0, 1, 1, 0])	
				elif symbol.imag >= 2:
					bits.extend([0, 1, 1, 1])	
				else:
					bits.extend([0, 1, 0, 1])
			elif symbol.real < 2:
				if symbol.imag < -2:
					bits.extend([0, 0, 0, 1])
				elif symbol.imag < 0:
					bits.extend([0, 0, 0, 1])
				elif symbol.imag < 2:
					bits.extend([1, 1, 1, 0])
				elif symbol.imag >= 2:
					bits.extend([1, 1, 1, 1])
				else:
					bits.extend([1, 1, 0, 1])
			else:
				bits.extend([1, 1, 1, 1])
	else:
		raise ValueError("Unsupported modulation scheme")
	return "".join(['0' if bt == 0 else '1' for bt in bits])



# main #
def preExit(countdownTime = defaultTime) -> None: # we use this function before exiting instead of getch since getch is not OS-independent
	try:
		cntTime = int(countdownTime)
		length = len(str(cntTime))
	except:
		return
	print()
	while cntTime > 0:
		print("\rProgram ended, exiting in {{0:>{0}}} second(s). ".format(length).format(cntTime), end = "")
		sleep(1)
		cntTime -= 1
	print("\rProgram ended, exiting in {{0:>{0}}} second(s). ".format(length).format(cntTime))

def printHelp() -> None:
	print("Python script for joint source-channel coding. ", end = "\n\n")
	print("Option: ")
	print("\t[/m|-m|m|/message|--message|message]: Specify that the following option is the message. ")
	print("\t[/s|-s|s|/series|--series|series]: Specify that the following option is the series for channel operation. ")
	print("\t[/scheme|--scheme|scheme]: Specify that the following option is the modulation scheme (BPSK, QPSK, or 16QAM). ", end = "\n\n")
	print("Format: ")
	print("\tpython jscc.py [/m|-m|m|/message|--message|message] message [/s|-s|s|/series|--series|series] series [/scheme|--scheme|scheme] scheme", end = "\n\n")
	print("Example: ")
	print("\tpython jscc.py /m \"Hello, World! \" /s 10101010 /scheme BPSK", end = "\n\n")

def handleCommandline() -> dict:
	for arg in argv[1:]:
		if arg.lower() in ("/h", "-h", "h", "/help", "--help", "help", "/?", "-?", "?"):
			printHelp()
			return True
	if len(argv) > 1 and len(argv) not in (3, 5, 7):
		print("The count of the commandline options is incorrect. Please check your commandline. ")
		return False
	dicts = {"m":"Hello, World! ", "s":"10101010", "scheme":"BPSK"}
	pointer = None
	for arg in argv[1:]:
		if arg.lower() in ("/m", "-m", "m", "/message", "--message", "message"):
			pointer = "m"
		elif arg.lower() in ("/s", "-s", "s", "/series", "--series", "series"):
			pointer = "s"
		elif arg.lower() in ("/scheme", "--scheme", "scheme"):
			pointer = "scheme"
		elif pointer is None:
			print("Error handling commandline, please check your commandline. ")
			return False
		else:
			dicts[pointer] = arg
			pointer = None # reset
	if len(dicts["m"]) > 1:
		if dicts["m"][1::] == dicts["m"][:-1:]:
			print("The message should not be a loop of a character. ")
			return False
	else:
		print("The length of the message is too short. ")
		return False
	if dicts["s"]:
		for ch in dicts["s"]:
			if ch not in ("0", "1"):
				print("The series should only contain 0 and 1. ")
				return False
	if dicts["scheme"] not in ("BPSK","QPSK", "16QAM"):
		print("Only BPSK, QPSK, and 16QAM are supported. ")
		return False
	return dicts

def main() -> int:
	# handle input #
	commandlineArgument = handleCommandline()
	if type(commandlineArgument) == bool:
		return EXIT_SUCCESS if commandlineArgument else EXIT_FAILURE
	message = commandlineArgument["m"]
	series = commandlineArgument["s"]
	modulation_scheme = commandlineArgument["scheme"]
	status = EXIT_SUCCESS
	
	# handle process #
	start_time = time()
	for _ in range(round):
		huffman_encoded_message, huffman_codes = huffman_encode(message)
	for _ in range(round):
		huffman_encoded_message, huffman_codes = huffman_encode(message)
		channel_encoded_message = channel_encode(huffman_encoded_message, series)
	for _ in range(round):
		huffman_encoded_message, huffman_codes = huffman_encode(message)
		channel_encoded_message = channel_encode(huffman_encoded_message, series)
		try:
			modulated_symbols = modulate(channel_encoded_message, modulation_scheme)
			demodulated_symbols = demodulate(modulated_symbols, modulation_scheme)
			channel_decoded_message = channel_decode(demodulated_symbols, series)
		except:
			modulated_symbols = "Not available"
			demodulated_symbols = "Not available"
			channel_decoded_message = channel_decode(channel_encoded_message, series)
			status = EXIT_FAILURE
	for _ in range(round):
		huffman_encoded_message, huffman_codes = huffman_encode(message)
		channel_encoded_message = channel_encode(huffman_encoded_message, series)
		try:
			modulated_symbols = modulate(channel_encoded_message, modulation_scheme)
			demodulated_symbols = demodulate(modulated_symbols, modulation_scheme)
			channel_decoded_message = channel_decode(demodulated_symbols, series)
		except:
			modulated_symbols = "Not available"
			demodulated_symbols = "Not available"
			channel_decoded_message = channel_decode(channel_encoded_message, series)
			status = EXIT_FAILURE
		huffman_decoded_message = huffman_decode(channel_decoded_message, huffman_codes)
	end_time = time()
	msTime = (end_time - start_time) * 1000
	
	# handle output #
	print("Message: {0}".format(message))
	print("Source encoded message: {0}".format(huffman_encoded_message))
	print("Channel encoded message: {0}".format(channel_encoded_message))
	print("Modulated symbols: {0}".format(modulated_symbols))
	print("Demodulated symbols: {0}".format(demodulated_symbols))
	print("Channel decoded message: {0}".format(channel_decoded_message))
	print("Source decoded message: {0}".format(huffman_decoded_message))
	print("Time consumption: {0:.6f}ms / {1} = {2:.6f}us. ".format(msTime, round, msTime * 1000 / round))
	preExit()
	return status




if __name__ == "__main__":
	exit(main())