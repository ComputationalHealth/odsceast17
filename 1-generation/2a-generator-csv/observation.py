#!/usr/bin/env python
import random

from datetime import datetime
from datetime import timedelta

# random lab function
def oru():

    CMP = {
        'components':{
        'sodium': {'value':int(),'unit':'mmol/L'},
        'potassium':{'value':int(),'unit':'mmol/L'},
        'chloride':{'value':int(),'unit':'mmol/L'},
        'bicarb':{'value':int(),'unit':'mmol/L'},
        'bun':{'value':int(),'unit':'mg/dL'},
        'creatinine':{'value':int(),'unit':'mg/dL'},
        'glucose':{'value':int(),'unit':'mg/dL'},
        },
        'method':str(),
        'service_id':str()

    }

    CBC = {
        'components':{
        'hemoglobin':{'value':int(),'unit':'g/dL'},
        'hematocrit':{'value':int(),'unit':'%'},
        'wbc':{'value':int(),'unit':'x1000/uL'},
        'platelet':{'value':int(), 'unit':'x1000/uL'},
        },
        'method':str(),
        'service_id':str()
    }

    x = random.randint(0, 1)
    if x == 1:
        CMP['components']['sodium']['value'] = random.uniform(120, 160)
        CMP['components']['potassium']['value'] = random.uniform(3, 6)
        CMP['components']['chloride']['value'] = random.uniform(85, 115)
        CMP['components']['bicarb']['value'] = random.uniform(16, 30)
        CMP['components']['bun']['value'] = random.uniform(15,60)
        CMP['components']['creatinine']['value'] = random.uniform(0.6, 3.0)
        CMP['components']['glucose']['value'] = random.uniform(40, 400)

        CMP['service_id'] = 'COMPREHENSIVE METABOLIC PANEL'
        CMP['method'] = 'YH DPP RS1'

        return CMP
    
    else:
        CBC['components']['hemoglobin']['value'] = random.uniform(7, 15)
        CBC['components']['hematocrit']['value'] = random.uniform(28, 54)
        CBC['components']['wbc']['value'] = random.uniform(2, 20)
        CBC['components']['platelet']['value'] = random.uniform(90, 400)

        CBC['service_id'] = 'COMPLETE BLOOD COUNT'
        CBC['method'] = 'SYSMEX'
        
        return CBC


# result object
class Observation:

    def __init__(self):
        self.oru  = oru()
        self.universal_service_id = self.oru['service_id']
        self.method = self.oru['method']

        # time objects
        self.msh_time = datetime.now()
        self.obx_time = (self.msh_time - timedelta(minutes=random.uniform(7, 13)))
        self.obs_end_time = (self.obx_time - timedelta(minutes=random.uniform(1, 3)))
        self.req_time = (self.obs_end_time - timedelta(minutes=random.uniform(12, 30)))
           
        # result status
        self.result_status = 'Verified'