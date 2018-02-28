"""
A simple programe to make emergency call via voice interface via SMS message

This is the single threaded version for Raspbian.

Python 2.7 is used on both Ubuntu 16.04 and Raspbian

@TODO: 
- replace printf with voice output

"""

import os
import sys
import signal
import time
import logging

import config as config
import ecCommon as ec

logging.basicConfig(level=config.LOG_LEVEL,
                    format='%(asctime)s %(levelname)s >> %(message)s'
                    #filename='./log,txt',
                    #filemode='w'
                    )

stop_program = False

import snowboydecoder
# ========================================

def on_detected_help():
    global stop_program
    stop_program = True

kws = {}
kws['help'] = {'pmdl':"help.pmdl",'obj':None,'cb':on_detected_help}

models,cbs = config.loadCfg(kws)

# ========================================

def interrupt_callback():
    global stop_program
    return stop_program

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, ec.signal_handler)

ec.prepTTS()

detector = snowboydecoder.HotwordDetector(models, sensitivity=0.5)

logging.info('Listening... Press Ctrl+C to exit')

# main loop

detector.start(detected_callback=cbs,
            interrupt_check=interrupt_callback,
            sleep_time=0.03)

detector.terminate()
time.sleep(0.1)

# perform tts after all the snowboy thing is done and closed
ec.tts(sms=False)    
