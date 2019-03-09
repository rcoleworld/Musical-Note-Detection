"""
FIRST REAL IMPLEMENTATION THAT WASN'T JUST COPY PASTED FROM OTHE INTERNET
This is the implementation of what was gathered from other code. This should
give the frequency of a sound. For the c note tested it registers near a C5.
The percent error of this test is less than 1% if this is not a mere
coincidence.
The webpage below is used to compare frequencies:
http://pages.mtu.edu/~suits/notefreqs.html

UPDATE 3/6/18 2:03PM: THIS ALSO WORKS WITH AN A NOTE!!
We need to get this to work with more than just a single note at a time!

UPDATE 3/8/18 6:00PM: Other notes implemented. Can now return a note value.
Still needs adjustments, F would not work.
"""
import wave
import numpy as np

DEBUGGING = False
def get_frequency(file):
    # this was tested using a chunk of 2048
    # and a chunk of 4096
    # play with this value at will
    chunk = 2048

    wave_file = wave.open(file, 'rb')
    sample_width = wave_file.getsampwidth()
    rate = wave_file.getframerate()
    # had to multiply the chunk by 2 here (1)
    # not sure why or what chunk even means
    window = np.blackman(chunk*2)

    data = wave_file.readframes(chunk)
    if DEBUGGING:
        print(len(data))
        print(2*chunk*sample_width)

    # unpack data and mult by window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/sample_width),\
                                        data))*window
    # take fft and square each element
    fft_data = abs(np.fft.rfft(indata)) ** 2
    # find the max frequency
    max = fft_data[1:].argmax() + 1

    # quadratic interpolation
    if max != len(fft_data)-1:
        y0,y1,y2 = np.log(fft_data[max-1:max+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (max+x1)*rate/chunk
        # print("IN IF")
        return thefreq
    else:
        thefreq = max*rate/chunk
        # print("IN ELSE")
        return thefreq
"""
This hard coded function will manually check if sound frequencies
are close to to real note frequencies. THIS WILL BE IMPOROVED!!
"""
def check_notes(frequency):
    if 430 < frequency < 450:
        return "A4"
    elif 480 < frequency < 500:
        return "B4"
    elif 515 < frequency < 530:
        return "C5"
    elif 580 < frequency < 600:
        return "D5"
    else:
        return "Nothing found"
##################################
# Main Part of Program
##################################
f = 'piano_c.wav'
freq = get_frequency(f)
note = check_notes(freq)
print(note)
