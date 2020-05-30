#!/usr/bin/env python3
import re
import math
import os

import nclib
import numpy as np
from scipy.spatial.transform import Rotation as R


def solveArrays(catalog, observations):
    """
    # TRIAD (2nd try):
    # Based on "Attitude Determination Using Two Vector Measurements":
    # https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19990052720.pdf
    # Page 1 and 2
    # Does work but was only discovered after solving the challenge using an SVD
    obs1 = np.array([float(f) for f in observations[0][1:]])
    obs2 = np.array([float(f) for f in observations[1][1:]])

    star_id1 = observations[0][0]
    star_id2 = observations[1][0]

    star_data1 = catalog[int(star_id1)]
    star_data2 = catalog[int(star_id2)]

    star_loc1 = np.array([float(f) for f in star_data1[:3]])
    star_loc2 = np.array([float(f) for f in star_data2[:3]])

    b1 = np.reshape(obs1,(-1, 3))
    b2 = np.reshape(obs2,(-1, 3))
    b3 = np.cross(b1, b2) / np.linalg.norm(np.cross(b1, b2))
    r1 = np.reshape(star_loc1,(-1, 3))
    r2 = np.reshape(star_loc2,(-1, 3))
    r3 = np.cross(r1, r2) / np.linalg.norm(np.cross(r1, r2))

    A = b1*r1.T + b3*r3.T + np.cross(b1, b3) * np.cross(r1, r3).T
    """

    #"""
    # Based on https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19990104598.pdf
    # Slides 1 and 4
    B = np.zeros((3,3))
    # First two observations are actually enough
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
    #"""

    q = R.from_matrix(A).as_quat()
    print(f"Attitude: (x:{q[0]}, y:{q[1]}, z:{q[2]}, w:{q[3]})")
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

    print("Connecting...")
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
        sendInput = "%f,%f,%f,%f" %(q[0], q[1], q[2], q[3])
        nc.send(bytes(sendInput,'utf-8')+b'\n')
        outBuf=nc.recv()
        observations = []
        getBuf=outBuf.decode('UTF-8')
        getBuf=getBuf.split('\n')[3:]
        for eachBuf in getBuf:
            newEach = re.split('\t|:',eachBuf.replace(' ','').replace(',',''))
            if '' not in newEach:
                observations.append(newEach)
