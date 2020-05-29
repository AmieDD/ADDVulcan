#!/usr/bin/env python3

import pandas as pd
import socket
import stars_improved
import numpy as np
from angle import angle_between

HOST = "myspace.satellitesabove.me"
PORT = 5016
TICKET = 'ticket{golf97715papa:GGz1HVIpuaglFCc1bMVUgZ91qKgBPQPIhQDUgl75jxnKQZCI7OBJobShmJI-wWEGEw}'


def send_cmd(sock, cmd):
    cmd += "\n"
    sock.sendall(cmd.encode("utf-8"))

def wait_for_resp(sock, text, debug=True):
    data = ""
    while True:
        partial_data = sock.recv(1024).decode("utf-8")
        if len(partial_data) == 0:
            raise IOError("I think we got disconnected")
        data += partial_data
        if debug:
            print(data)

        if text in data:
            return data

# SAY HI
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting...")
server.connect((HOST, PORT))
print("Connected.")
wait_for_resp(server, "Ticket please", debug=False)
send_cmd(server, TICKET)  # send ticket

iteration = 0
while True:
    data = ''
    while 'Guesses' not in data:
        data += server.recv(2024).decode("utf-8")  # rcv data

    # PARSE INCOMING DATA
    data = data.replace('\t', '')  # remove tabs
    data = data.split('\n\n')[0]  # truncate chars after strings
    data = data.splitlines()  # split into list
    # print(data)
    cleaned_data = []
    for line in data:
        # list comp would be easier.. >_>
        line = line.split(',')
        cleaned_data.append(line)

    # create a list of dicts and make a dataframe out of it
    data_dict_list = []
    for row in cleaned_data:
        row_dict = {}
        row_dict['x'] = float(row[0])
        row_dict['y'] = float(row[1])
        row_dict['z'] = float(row[2])
        row_dict['m'] = float(row[3])
        data_dict_list.append(row_dict)

    ref_vectors = pd.DataFrame(data_dict_list)
    print("\nWE RCVD:")
    print(ref_vectors)

    indexes = []
    for i,rowt in ref_vectors.iterrows():
        star_obs = np.array([rowt['x'], rowt['y'], rowt['z']])

        # Find the closest two stars in the observation
        next_1_a = np.inf
        next_1_i = None
        next_1_p = None
        next_2_a = np.inf
        next_2_i = None
        next_2_p = None
        for i_t, rowt_t in ref_vectors.iterrows():
            if i == i_t:
                continue
            star_obs_t = np.array([rowt_t['x'], rowt_t['y'], rowt_t['z']])
            a = angle_between(star_obs, star_obs_t)
            if a < next_1_a:
                next_2_a = next_1_a
                next_2_i = next_1_i
                next_2_p = next_1_p
                next_1_a = a
                next_1_i = i_t
                next_1_p = star_obs_t
            elif a < next_2_a:
                next_2_a = a
                next_2_i = i_t
                next_2_p = star_obs_t

        print(f"Two closest stars next to {i} are {next_1_i} and {next_2_i}")
        index, error = stars_improved.find_by_angles(next_1_a, next_2_a, angle_between(next_1_p, next_2_p))
        print(f"Matched catalog star: {index} (Error: {error:.6})")
        indexes.append((index, error))

    # Take the 5 best matches and build a string
    indexes.sort(key = lambda x: x[1])
    indexes = indexes[:5]
    indexes = np.array([str(i[0]) for i in indexes])
    index_string = ','.join(indexes)


    print("\nWE SENT")
    print(index_string)
    send_cmd(server, index_string)
    data = server.recv(1024).decode("utf-8")
    print(data)
