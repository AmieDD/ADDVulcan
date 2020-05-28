#!/usr/bin/env python3
import re
import math
import os

import nclib
import numpy as np
from pyquaternion import Quaternion


def solveArrays(catalog, observations):
    # Based on https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19990104598.pdf
    # Slides 1 and 4
    B = np.zeros((3,3))
    # First three observations are actually enough
    for obs in observations:
        star_id = obs[0]
        obs = np.array([float(f) for f in obs[1:]])
        star_data = catalog[int(star_id)]
        star_loc = np.array([float(f) for f in star_data[:3]])
        star_mag = float(star_data[3])

        ai = star_mag
        bi = np.reshape(obs,(-1, 3))
        ri = np.reshape(star_loc,(-1, 3))
        print(f"Observed star {star_id} at {bi}. Catalog vector: {ri}");

        B += ai * bi * ri.T

    u, s, vh = np.linalg.svd(B, full_matrices=True)
    C = np.diag([1, 1, np.linalg.det(u) * np.linalg.det(vh)])
    A = u @ C @ vh

    # A is an orthogonal rotation matrix and translates nicely into a normalized quaternion
    q = Quaternion(matrix=A)
    print(f"Attitude: (x:{q.x}, y:{q.y}, z:{q.z}, w:{q.w})")
    return q

if __name__ == '__main__':
    catalog = []# Read from catalog
    f=open('test.txt','r')
    catalog_lines = f.readlines()
    for eachLine in catalog_lines:
        createVector = re.split('\t',eachLine.replace(',','').replace('\n',''))
        if '' not in createVector:
            catalog.append(createVector)
    print("Catalog Loaded...")

    observations = []
    nc = nclib.Netcat(('attitude.satellitesabove.me', 5012), verbose=True)
    nc.recv()
    nc.send(b'ticket{charlie47226alpha:GDIXRN78-6xCK34RmdUj_8lTV5t9hxwHiny8skzTpU7h6mnKPmpqYZfmJGu0G2yn7Q}\n')
    outBuf=nc.recv()
    getBuf=outBuf.decode('UTF-8')
    getBuf=getBuf.split('\n')[2:]

    for eachBuf in getBuf:
        newEach = re.split('\t|:',eachBuf.replace(' ','').replace(',',''))
        if '' not in newEach:
            observations.append(newEach)

    for x in range(0,20):
        q=solveArrays(catalog, observations)
        sendInput = "%f,%f,%f,%f" %(q.x, q.y, q.z, q.w)
        nc.send(bytes(sendInput,'utf-8')+b'\n')
        outBuf=nc.recv()
        observations = []
        getBuf=outBuf.decode('UTF-8')
        getBuf=getBuf.split('\n')[3:]
        for eachBuf in getBuf:
            newEach = re.split('\t|:',eachBuf.replace(' ','').replace(',',''))
            if '' not in newEach:
                observations.append(newEach)
