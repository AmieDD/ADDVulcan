#!/usr/bin/env python3

import sys
import crcmod

def escape(d):
	result = []

	escape = False
	for c in d:
		if escape:
			result.append(c ^ (1 << 5))
			escape = False
		elif c == 0x7d:
			escape = True
		else:
			result.append(c)

	return bytearray(result)

# crc_fn = crcmod.mkCrcFun(0x11021, 0x0000, True, 0x0000)
# print(hex(crc_fn("123456789".encode())))

for line in sys.stdin:
	line = line.strip()

	if line == '':
		continue

	if line[0] == '#':
		if 'HI:' in line:
			direction = 'I'
		if 'LO:' in line:
			direction = 'O'
		continue

	d = bytes.fromhex(line)

	# print('raw: {:s}'.format(line))

	# if d[0] == 0x7e and d[-1] == 0x7e:
	no_flags = d[1:-1]
	crc_data = no_flags[:-2]
	crc_value = no_flags[-2:]
	escaped = escape(crc_data)

	address, control = escaped[0:2]

	crc_fn = crcmod.mkCrcFun(0x11021, 0xffff, False, 0xffff)
	crc_calc = crc_fn(crc_data)

	escaped_hex = ' '.join(['{:02x}'.format(v) for v in escaped + crc_value])
	# print(direction)
	print('0000: {:s}'.format(escaped_hex))
		# print('esc: {:s}'.format(escaped_hex))
		# print('ppp: {:02x} {:02x}'.format(
		# 	address, control,
		# ))
	print('crc: {:02x}{:02x} ?= {:04x}'.format(
		crc_value[0], crc_value[1], crc_calc,
	))
	# else:
	# 	print('invalid')
	# print()
