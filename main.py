import snowboythreaded
import sys
import signal
import time
import os

import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

stop_program = False

# This a demo that shows running Snowboy in another thread

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

# ========================================

model_path = './resources'

def tts():
    #print("performing TTS ...")
    #time.sleep(1)
    #print("TTS done! ...")
    print(">> Say something!")
    with m as source: 
        audio = r.listen(source)
    print(">> Got it! Now to recognize it...")
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)

        # we need some special handling here to correctly print unicode characters to standard output
        if str is bytes:  # this version of Python uses bytes for strings (Python 2)
            print(u">> You said {}".format(value).encode("utf-8"))
        else:  # this version of Python uses unicode for strings (Python 3+)
            print(">> You said {}".format(value))
    except sr.UnknownValueError:
        print(">> Oops! Didn't catch that")
        # here should just send out an generic help message anyway
    except sr.RequestError as e:
        print(">> Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

def on_detected_help():
    print("detected! Pausing hotword detection for TTS")
    threaded_detector.pause_recog()
    tts()
    print("Resume hotword detection after TTS")
    threaded_detector.start_recog(sleep_time=0.03, detected_callback=cbs)

kws = {}
kws['help'] = {'pmdl':"help.pmdl",'obj':None,'cb':on_detected_help}

models = []
cbs = []
for c,k in enumerate(kws):
    kk = kws[k]
    models.append(os.path.join(model_path, kk['pmdl']))
    cbs.append(kk['cb'])


# ========================================

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# prepare TTS
print("A moment of silence, please...")
with m as source: 
    r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))


# Initialize ThreadedDetector object and start the detection thread
threaded_detector = snowboythreaded.ThreadedDetector(models, sensitivity=0.5)
threaded_detector.start()

print('Listening... Press Ctrl+C to exit')

# main loop
threaded_detector.start_recog(sleep_time=0.03, detected_callback=cbs)

# Let audio initialization happen before requesting input
time.sleep(1)

# Do a simple task separate from the detection - addition of numbers
while not stop_program:
    
    try:
        resp = raw_input("<aidex> ")
        #print "<aidex> {}".format(resp)
        if resp == 'q':
            print("existing ...")
            global stop_program
            stop_program = True
    except ValueError:
        print "error!"

threaded_detector.terminate()
