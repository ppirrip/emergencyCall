"""
basic config parameters
"""
import os
import logging
LOG_LEVEL = logging.DEBUG

model_path = './resources'

# setup key words
# @TODO
# - read this from a config file

def loadCfg(kws):
    models = []
    cbs = []
    for c,k in enumerate(kws):
        kk = kws[k]
        models.append(os.path.join(model_path, kk['pmdl']))
        cbs.append(kk['cb'])
    
    return models,cbs