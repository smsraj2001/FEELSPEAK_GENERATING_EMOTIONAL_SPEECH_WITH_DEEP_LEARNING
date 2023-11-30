# OpenVokaListen.py
# public-domain sample code by Vokaturi, 2022-08-23
# (note that the Vokaturi library that is loaded is not public domain itself)
#
# A sample script that uses the OpenVokaturi library to extract the emotions from
# speech in real time.
#
# Call syntax:
#   python3 examples/OpenVokaListen.py

import sys
sys.path.append("api")
import Vokaturi

print ("Loading library...")
import platform
import struct
if platform.system() == "Darwin":
	assert struct.calcsize ("P") == 8
	Vokaturi.load("lib/open/macos/OpenVokaturi-4-0-mac.dylib")
elif platform.system() == "Windows" or platform.system() == "CYGWIN_NT-10.0-19044":
	if struct.calcsize ("P") == 4:
		Vokaturi.load("lib/open/win/OpenVokaturi-4-0-win32.dll")
	else:
		assert struct.calcsize ("P") == 8
		Vokaturi.load("lib/open/win/OpenVokaturi-4-0-win64.dll")
elif platform.system() == "Linux":
	assert struct.calcsize ("P") == 8
	Vokaturi.load("lib/open/linux/OpenVokaturi-4-0-linux.so")
print ("Analyzed by: %s" % Vokaturi.versionAndLicense())

import numpy as np
import pyaudio
import time

p = pyaudio.PyAudio()
c_buffer = Vokaturi.float32array(10000)   # usually 1024 would be big enough

def callback(in_data, frame_count, time_info, flag):
	audio_data = np.frombuffer(in_data, dtype=np.float32)
	c_buffer[0 : frame_count] = audio_data
	voice.fill_float32array(frame_count, c_buffer)
	return (in_data, pyaudio.paContinue)

print ("Creating VokaturiVoice...")
sample_rate = 44100
buffer_duration = 10 # seconds
buffer_length = sample_rate * buffer_duration
voice = Vokaturi.Voice(
	sample_rate,
	buffer_length,
	True   # because fill() and extract() will be called from different threads
)

print ("PLEASE START TO SPEAK...")
stream = p.open(
	rate=sample_rate,
	channels=1,
	format=pyaudio.paFloat32,
	input=True,
	output=False,
	start=True,
	stream_callback=callback
)

approximate_time_elapsed = 0.0   # will not include the processing time of extract()
time_step = 0.5   # seconds

while stream.is_active():   # i.e. forever
	time.sleep(time_step)

	quality = Vokaturi.Quality()
	emotionProbabilities = Vokaturi.EmotionProbabilities()
	voice.extract(quality, emotionProbabilities)
	approximate_time_elapsed = approximate_time_elapsed + time_step
	
	if quality.valid:
		print ("%5.1f time" % approximate_time_elapsed,
			"%5.0f N" % (100 * emotionProbabilities.neutrality),
			"%5.0f H" % (100 * emotionProbabilities.happiness),
			"%5.0f S" % (100 * emotionProbabilities.sadness),
			"%5.0f A" % (100 * emotionProbabilities.anger),
			"%5.0f F" % (100 * emotionProbabilities.fear))
