"""
Common routines for emergency call
"""

import config as config

import logging
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

logging.basicConfig(level=config.LOG_LEVEL,
                    format='%(asctime)s %(levelname)s >> %(message)s'
                    #filename='./log,txt',
                    #filemode='w'
                    )

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

def prepTTS():
    # prepare TTS
    logging.debug("A moment of silence, please...")
    with m as source: 
        r.adjust_for_ambient_noise(source)
        logging.info("Set minimum energy threshold to {}".format(r.energy_threshold))

def tts():
    logging.info("Any message you want to add?")
    with m as source: 
        audio = r.listen(source)
        logging.debug("Got it!") 
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)

        # we need some special handling here to correctly print unicode characters to standard output
        if str is bytes:  # this version of Python uses bytes for strings (Python 2)
            logging.info(u"You said {}".format(value).encode("utf-8"))
        else:  # this version of Python uses unicode for strings (Python 3+)
            logging.info("You said {}".format(value))

    except sr.UnknownValueError:
        # this is the tricky part, is the user:
        # - unable to speak (go ahead and send a default msg?)
        # - the mic not working or not receiving (go ahead and send a default msg?)
        # - help triggered by mistake? (cancel the request?)
        # here is where secondary input comes in, like the puff sensor
        secondConfirm()    
        
    except sr.RequestError as e:
        logging.error("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

def secondConfirm():
    logging.warning("Can't get user input, ask for confirmation / sencondary input [TODO]")
    pass
