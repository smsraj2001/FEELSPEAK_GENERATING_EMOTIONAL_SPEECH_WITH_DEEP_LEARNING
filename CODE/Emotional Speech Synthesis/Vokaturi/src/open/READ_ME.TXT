READ_ME.TXT

- OpenVokaturi version 4.0, 2020-08-23:
For real-time applications with a separate audio capturing thread,
you used to have to supply an external ring buffer with locks or memory barriers.
You can now synchronize VokaturiVoice_fill() and VokaturiVoice_extract() simply by
switching on a multithreading flag in VokaturiVoice_create().
On MacOS, we now also support ARM (Apple Silicon) processors.
We added example code for real-time use with Python.

- OpenVokaturi version 3.4, 2020-02-20:
Bug fix in VokaWav.h for stereo files.

- OpenVokaturi version 3.3, 2019-06-02:
We always had a function that fills the VokaturiVoice with 64-bit floating-point data.
Now you can also fill the VokaturiVoice directly with 32-bit floating point data,
16-bit integer data, or 32-bit integer data, without first converting.
You can now also directly send interleaved stereo data to two VokaturiVoices,
in all four supported formats.

- OpenVokaturi version 3.0a, 2018-05-08:
We included libraries for the Raspberry Pi.

- OpenVokaturi version 3.0, 2018-02-20:
We now support more platforms (Android; ARM64 Linux).
Some source files have clearer names,
and we include more example code and binaries.

- OpenVokaturi version 2.2a, 2017-09-17:
The analysis runs 2.2 times faster than in version 2.1,
although the resulting output has stayed exactly the same.

- OpenVokaturi version 2.1c, 2017-07-13:
The example software `WavFile.h`, as well as `MeasureWav_win64.exe`,
now recognizes even more types of WAV files.

- OpenVokaturi version 2.1b, 2017-01-31:
The example software `WavFile.h`, as well as `MeasureWav_win64.exe`,
now recognizes more types of WAV files.

- OpenVokaturi version 2.1a, 2017-01-25:
The example files `measure_wav_win64.py` and the like in the SDK were corrected
so as to be similar to the example file that you can read on the website.
The incorrect example files would report zero emotion probabilities
because they did not test for "quality".

- OpenVokaturi version 2.1, 2017-01-16.

- OpenVokaturi version 2.0, 2017-01-02:
We increased the number of cues from 5 to 9;
this raised the quality by approximately 5 percent.
We trained the network on two databases
(EmoDB and Savee: 768 recordings annotated for the five main emotions),
instead of only on EmoDB; this raised the capability of generalization
to new sounds tremendously.
The network is no longer based on linear discriminant analysis;
instead, we now use an articificial neural network that converts
from 9 cues to 5 emotion probabilities via two hidden layers
of 100 and 20 nodes, respectively.
The classification on 5 emotions is now 66.5 percent on two databases,
as measured by leave-one-out cross-validation, repeated 3 times
(i.e. training 3 times on each possible subset of 767 recordings
and testing each time the remaining single recording).

- OpenVokaturi version 1.3, 2016-12-11:
We added libraries for Linux. Also, you can now compile the source code
under C++ as well as C99.

- OpenVokaturi version 1.2, 2016-09-03:
We added Vokaturi_setRelativePriorProbabilities () to allow for worlds where
not all of the five emotions are equally likely,
and Vokaturi_reset () to start with an empty slate,
as long as the sampling frequency and buffer length stay the same
(this is faster than doing Vokaturi_destroy followed by Vokaturi_create).
There were also some bug removals:
a "NaN" that did not work on all compilers was removed,
and a potential crash after recording for a long time was repaired.

- OpenVokaturi version 1.1, 2016-04-29:
The classification is now 61.4 percent. This is lower than in version 1.0,
but it signals an improvement. The classification model now has equal
cue standard deviations within each emotion class.
In version 1.0, the standard deviation of *pitSlo* was approximately
9.1 semitones per second for Neutral and 18.4 for Sadness,
leading to a high probability for Sadness for recordings that were
on the far super-neutral side of the Neutral-Sadness continuum.
This is a well-known problem in linear discriminant analysis
and Gaussian mixture techniques.
In 1.1 we pool the standard deviations over all emotions;
the same standard deviation of *pitSlo* therefore becomes
approximately 12.9 semitones per second,
independently from the emotion class.
We can say that the model now uses
many fewer adjustable parameters, and that it is more robust,
i.e. the mistakes it makes are less surprising.

- OpenVokaturi version 1.0, 2016-04-14:
Given speech that comes in as a sampled sound,
the Vokaturi software computes five acoustic cue strengths:
*pitAve*, *pitSlo*, *intAve*, *intSlo*, *spcSlo*.
From these cues, the software computes probabilities for the five main emotions:
**neutrality**, **happiness**, **sadness**, **anger**, **fear**.
The method is linear discriminant analysis,
with all off-diagonal cells of the covariance matrix set to zero.
Trained and tested on EmoDB, with ten-fold cross-validation,
classification is correct in 62.7 percent of the cases
(with homogeneous priors, i.e. each of the five emotions is equally likely a priori).
