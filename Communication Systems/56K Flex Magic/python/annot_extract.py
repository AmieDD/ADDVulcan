#!/usr/bin/env python3

import sys
import re

sample_rate = 44100
ignore_until = sample_rate * 7

re_byte = re.compile(r'(?P<start>\d+)-(?P<end>\d+) UART: RX: (?P<data>.+)')

result = []
for line in sys.stdin:
	match = re_byte.match(line)
	if match:
		start = int(match['start'])
		end = int(match['end'])

		if end < ignore_until:
			continue

		data = match['data']
		if data in ('Start bit', 'Stop bit'):
			continue
		# print(match['start'], match['end'], '>' + match['data'] + '<')
		# if len(data) == 4:
		# 	if data[0] == '[' and data[3] == ']':
		# 		result.append(data[1:3])
		# 	else:
		# 		print(line)
		# 		raise RuntimeError()
		elif len(data) == 2:
			result.append(data)
		# elif len(data) == 1:
		# 	result.append('{:02X}'.format(ord(data)))
		else:
			print(line)
			raise RuntimeError()
	# if len(s) == 2:
	# 	s = s[1]
	# 	if s in ('Start bit', 'Stop bit'):
	# 		continue
	# 	if len(s) == 1:
	# 		result.append('{:02x}'.format(ord(s)))
	# 	elif s[0] == '[' and s[3] == ']':
	# 		result.append(s[1:3])
	# 	else:
	# 		print(s)
	# 		raise RuntimeError()
	# 	# b = int(s[1][:2], 16)
	# 	# b = '{:08b}'.format(b)
	# 	# b = b[::-1]
	# 	# b = int(b, 2)
	# 	# b = '{:02x}'.format(b)

# print(result)
s = ' '.join(result)
# b = bytes.fromhex(s)
print(s)

# open('out.bin', 'wb').write(b)
