"""
A simple programe to make emergency call via voice interface via SMS message

This is based on Snowboy demo_threaded.

Python 2.7 is used on both Ubuntu 16.04 and Raspbian

@TODO: 
- add Twillo interface
- replace printf with voice output
- add a decent console

"""

import os
import sys
import signal
import time
import logging

import config as config
import ecCommon as ec

import snowboythreaded

logging.basicConfig(level=config.LOG_LEVEL,
                    format='%(asctime)s %(levelname)s >> %(message)s'
                    #filename='./log,txt',
                    #filemode='w'
                    )

stop_program = False

# ========================================

def on_detected_help():
    logging.debug("detected! Pausing hotword detection for TTS")
    threaded_detector.pause_recog()
    ec.tts()
    logging.debug("Resume hotword detection after TTS")
    threaded_detector.start_recog(sleep_time=0.03, detected_callback=cbs)


kws = {}
kws['help'] = {'pmdl':"help.pmdl",'obj':None,'cb':on_detected_help}

models,cbs = config.loadCfg(kws)

# ========================================

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, ec.signal_handler)

ec.prepTTS()

# Initialize ThreadedDetector object and start the detection thread
threaded_detector = snowboythreaded.ThreadedDetector(models, sensitivity=0.5)
threaded_detector.start()

logging.info('Listening... Press Ctrl+C to exit')

# main loop
threaded_detector.start_recog(sleep_time=0.03, detected_callback=cbs)

# Let audio initialization happen before requesting input
time.sleep(1)

# Do a simple task separate from the detection - addition of numbers
while not stop_program:
    
    try:
        resp = raw_input("<aidex> ")
        if resp == 'q':
            print("existing ...")
            global stop_program
            stop_program = True
    except ValueError:
        logging.error("ValueError:raw_input")

threaded_detector.terminate()
