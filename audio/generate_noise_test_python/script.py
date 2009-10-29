import wave
import random
import struct
import datetime

SAMPLE_LEN = 44100 * 300 # 300 seconds of noise, 5 minutes

print "Create file using wave and writeframes twice in each iteration"

noise_output = wave.open('noise.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

d1 = datetime.datetime.now()

for i in range(0, SAMPLE_LEN):
	value = random.randint(-32767, 32767)
	packed_value = struct.pack('h', value)
	noise_output.writeframes(packed_value)
	noise_output.writeframes(packed_value)

d2 = datetime.datetime.now()
print (d2 - d1), "(time for writing frames)"

noise_output.close()

d3 = datetime.datetime.now()
print (d3 - d2), "(time for closing the file)"

# --------------

print "Create a file directly writing to the file twice in each iteration"

noise_file = open('noise.raw', 'w')

d1 = datetime.datetime.now()

for i in range(0, SAMPLE_LEN):
	value = random.randint(-32767, 32767)
	packed_value = struct.pack('h', value)
	noise_file.write(packed_value)
	noise_file.write(packed_value)

d2 = datetime.datetime.now()
print (d2 - d1), "(time for writing frames)"

noise_file.close()

d3 = datetime.datetime.now()
print (d3 - d2), "(time for closing the file)"

# --------------

print "Create file using wave, storing frames in an array and using writeframes only once"

noise_output = wave.open('noise2.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

d1 = datetime.datetime.now()
values = []

for i in range(0, SAMPLE_LEN):
	value = random.randint(-32767, 32767)
	packed_value = struct.pack('h', value)
	values.append(packed_value)
	values.append(packed_value)

value_str = ''.join(values)
noise_output.writeframes(value_str)

d2 = datetime.datetime.now()
print (d2 - d1), "(time for writing frames)"

noise_output.close()

d3 = datetime.datetime.now()
print (d3 - d2), "(time for closing the file)"



