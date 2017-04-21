#!/usr/bin/env python
import json
import uuid
import random

from datetime import datetime
from datetime import timedelta


# random lab function
def lab():

    CMP = {
        'sodium':int(),
        'potassium':int(),
        'chloride':int(),
        'bicarb':int(),
        'bun':int(),
        'creatinine':int(),
        'glucose':int()
    }

    CBC = {
        'hemoglobin':int(),
        'hematocrit':int(),
        'wbc':int(),
        'platelet':int()
    }

    x = random.randint(0, 1)
    if x == 0:
        CMP['sodium'] = random.randint(111,180)
        CMP['potassium'] = random.randint(2,9)
        CMP['chloride'] = random.randint(53,140)
        CMP['bicarb'] = random.randint(15,32)
        CMP['bun'] = random.randint(2,221)
        CMP['creatinine'] = random.randint(1, 20)
        CMP['glucose'] = random.randint(10, 266)

        return CMP
    
    else:
        CBC['hemoglobin'] = random.randint(5,29)
        CBC['hematocrit'] = random.randint(30,70)
        CBC['wbc'] = random.randint(1,300)
        CBC['platelet'] = random.randint(2,999)
        return CBC

# result object
class Result:

    def __init__(self):
        self.Id = str(uuid.uuid4())
        self.eid = str(random.randint(120000000, 500000000))
        self.pid = str(random.randint(10000000, 40000000))
        self.age = str(random.randint(18, 99))
        self.sex = gender()
        self.oid = str(random.randint(600000000, 700000000))
        self.pr_code = "LAB17"
        self.pr_name = "COMPREHENSIVE METABOLIC PANEL"

        # time objects
        self.r_ts = datetime.now()

        # New_Datetime = Datetime_now - (timeDelta from result time)
        self.c_ts = (datetime.now() - (self.r_ts - (datetime.now() - timedelta(hours=random.randint(1,2)))))
        self.o_ts = (self.c_ts - timedelta(hours=random.randint(1,2)))
        self.tat = (self.r_ts - self.o_ts).seconds
        self.lab= lab()
        self.result_str = str(self.result_int)
        self.camp = str("yale")

    # dumps Result object in json
    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)