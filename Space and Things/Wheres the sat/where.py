#!/usr/bin/env python3
import sys
import numpy as np
from skyfield.api import EarthSatellite,load,utc
import datetime

# Paste these in from challenge (no decimal points for the dates!)
target_pos = [3325.9551365233465, 5661.247530021378, -1686.7302721732608]
initial_time = (2020, 3, 18, 7, 58, 40)
check_time = (2020, 3, 18, 17, 29, 3)

with open("stations.txt", "r") as tles:
    lines = tles.readlines()

sats = []

ts = load.timescale()
candidate_sat = None
norm = 1e99

# Load sat names and find closest sat
for i in range(0,len(lines),3):
    name = lines[i].strip()
    sats.append(name)
    t = datetime.datetime(*initial_time, tzinfo=utc) # From, prompt
    try:
        satellite = EarthSatellite(lines[i+1],lines[i+2],lines[i], ts)
        position = satellite.at(ts.utc(t)).position.km

        diff = position - target_pos
        curr_norm = np.linalg.norm(diff)
        if curr_norm < norm:
            candidate_sat = satellite
            norm = curr_norm
            # print(name, position, target_pos)
    except NotImplementedError:
        pass

print("Selected sat", candidate_sat)
t = datetime.datetime(*check_time, tzinfo=utc) # Change this from challenge
position = candidate_sat.at(ts.utc(t)).position.km
print(position)
