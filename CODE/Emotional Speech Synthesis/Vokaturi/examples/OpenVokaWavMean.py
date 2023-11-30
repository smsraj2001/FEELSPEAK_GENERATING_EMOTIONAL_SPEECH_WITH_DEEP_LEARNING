# OpenVokaWavMean.py
# public-domain sample code by Vokaturi, 2022-08-23
#
# A sample script that uses the VokaturiPlus library to extract the emotions from
# a wav file on disk. The file can contain a mono or stereo recording.
#
# Call syntax:
#   python3 examples/OpenVokaWavMean.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#	Neutral: 0.760
#	Happy: 0.000
#	Sad: 0.238
#	Angry: 0.001
#	Fear: 0.000

import sys
import scipy.io.wavfile

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

print ("Reading sound file...")
file_name = sys.argv[1]
(sample_rate, samples) = scipy.io.wavfile.read(file_name)
print ("   sample rate %.3f Hz" % sample_rate)

print ("Allocating Vokaturi sample array...")
buffer_length = len(samples)
print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.float64array(buffer_length)
if samples.ndim == 1:  # mono
	c_buffer[:] = samples[:] / 32768.0  # mono
else:  # stereo
	c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0  # stereo

print ("Creating VokaturiVoice...")
voice = Vokaturi.Voice (sample_rate, buffer_length, 0)

print ("Filling VokaturiVoice with samples...")
voice.fill_float64array(buffer_length, c_buffer)

print ("Extracting emotions from VokaturiVoice...")
quality = Vokaturi.Quality()
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.extract(quality, emotionProbabilities)

if quality.valid:
	print ("Neutral: %.3f" % emotionProbabilities.neutrality)
	print ("Happy: %.3f" % emotionProbabilities.happiness)
	print ("Sad: %.3f" % max(emotionProbabilities.sadness, emotionProbabilities.fear))
	print ("Angry: %.3f" % emotionProbabilities.anger)
	# print ("Fear: %.3f" % emotionProbabilities.fear)
else:
	print ("Not enough sonorancy to determine emotions")

voice.destroy()
