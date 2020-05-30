#!/usr/bin/env python3
import re
import math
import os

import nclib
import numpy as np
from pyquaternion import Quaternion

from quat import quat

def solveArrays(xArrays,yArrays):

    """
    # TRIAD (1st try):
    # Does not work :(
    Asub = []
    for x in range(0,3):
        obs = np.array([float(f) for f in yArrays[x][1:]])

        star_id = yArrays[x][0]
        star_data = xArrays[int(star_id)]
        star_loc = np.array([float(f) for f in star_data[:3]])

        bi = np.reshape(obs,(-1, 3))
        ri = np.reshape(star_loc,(-1, 3))

        Asub.append(ri.T * bi)
    A = Asub[0]+Asub[1]+Asub[2]
    """

    # SVD:
    # Based on https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19990104598.pdf
    # Slides 1 and 4
    B = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]])
    for obs in yArrays:
        star_id = obs[0]
        obs = np.array([float(f) for f in obs[1:]])
        star_data = xArrays[int(star_id)]
        star_loc = np.array([float(f) for f in star_data[:3]])
        star_mag = float(star_data[3])

        ai = star_mag
        bi = np.reshape(obs,(-1, 3))
        ri = np.reshape(star_loc,(-1, 3))
        print(f"Observed star {star_id} at {bi}. Catalog vector: {ri}");

        B += ai * bi * ri.T

    u, s, vh = np.linalg.svd(B, full_matrices=True)
    C = [[1, 0, 0], [0, 1, 0], [0, 0, np.linalg.det(u) * np.linalg.det(vh)]]
    A = np.matmul(np.matmul(u, C), vh)


    qx, qy, qz, qw = quat(A)
    q = Quaternion(qw, qx, qy, qz).normalised
    print(f"Attitude: (x:{q.x}, y:{q.y}, z:{q.z}, w:{q.w})")
    return q

if __name__ == '__main__':
    xArrays = []# Read from catalog
    f=open('test.txt','r')
    catalog = f.readlines()
    for eachLine in catalog:
        createVector = re.split('\t',eachLine.replace(',','').replace('\n',''))
        if '' not in createVector:
            xArrays.append(createVector)
    print("Catalog Loaded...")

    yArrays = []

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
            yArrays.append(newEach)

    for x in range(0,20):
        q=solveArrays(xArrays,yArrays)
        sendInput = "%f,%f,%f,%f" %(q.x, q.y, q.z, q.w)
        nc.send(bytes(sendInput,'utf-8')+b'\n')
        outBuf=nc.recv()
        yArrays = []
        getBuf=outBuf.decode('UTF-8')
        getBuf=getBuf.split('\n')[3:]
        for eachBuf in getBuf:
            newEach = re.split('\t|:',eachBuf.replace(' ','').replace(',',''))
            if '' not in newEach:
                yArrays.append(newEach)
