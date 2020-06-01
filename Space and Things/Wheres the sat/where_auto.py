#!/usr/bin/env python3

import sys
import numpy as np
import datetime
import socket

from skyfield.api import EarthSatellite, load, Topos, utc

HOST = "where.satellitesabove.me"
PORT = 5021

FLAG = "ticket{charlie7635alpha:GM_c1iE2BSb8QX02eDAHpWhikpr9BGNZaK30dA0G08vpIf6OC_09sS-_pCwdkjoheg}"


def send_cmd(sock, cmd):
    cmd += "\n"
    print(cmd)
    sock.sendall(cmd.encode("utf-8"))


def readline(sock, debug=False):
    data = ""

    while True:
        read_char = sock.recv(1).decode("utf-8")

        if len(read_char) == 0:
            print(data)
            return None

        data += read_char
        if debug:
            print(data)

        if read_char == "\n":
            return data


# Text should be string or list of strings to match
def wait_for_resp(sock, text, debug=False):
    data = ""

    if not isinstance(text, list):
        text = [text]

    while True:
        partial_data = sock.recv(1).decode("utf-8")

        if len(partial_data) == 0:
            print(data)
            return None

        data += partial_data
        if debug:
            print(data)

        for item in text:
            if item in data:
                return data


def find_sat(target_pos, flyover_time):
    with open("stations.txt", "r") as tles:
        lines = tles.readlines()

    sats = []

    candidate_sat = None
    norm = 1e99

    ts = load.timescale()

    # Load sat names
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        sats.append(name)
        try:
            satellite = EarthSatellite(lines[i + 1], lines[i + 2], lines[i], ts)
            position = satellite.at(ts.utc(flyover_time)).position.km
            diff = position - target_pos
            curr_norm = np.linalg.norm(diff)
            if curr_norm < norm:
                candidate_sat = satellite
                norm = curr_norm

        except NotImplementedError:
            pass

    return candidate_sat


try:
    ts = load.timescale()

    ticket_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ticket_serv.connect((HOST, PORT))
    wait_for_resp(ticket_serv, "Ticket please:\n")

    print("Sending ticket")
    send_cmd(ticket_serv, FLAG)

    # Get date string
    time_str = wait_for_resp(ticket_serv, "\n").split(":")[1].strip()


    # strip parenthesis and convert to list of integers
    time_list = [int(float(i)) for i in time_str[1:-1].split(", ")]

    sat_start_time = datetime.datetime(*time_list, tzinfo=utc)

    # Get pos string
    pos_str = wait_for_resp(ticket_serv, "\n").split(":")[1].strip()

    # Strip parenthesis and convert to list
    pos = [float(i) for i in pos_str[1:-1].split(", ")]

    attempt_str = wait_for_resp(ticket_serv, "\n")

    for count in range(3):
        # Query format "What is the X coordinate at the time of:(2020, 3, 18, 12, 53, 20.0)?\n"
        query = wait_for_resp(ticket_serv, "?\n").strip()
        print(query)

        time_str = query.split(":(")[-1][:-2]
        time_list = [int(float(i)) for i in time_str.split(", ")]
        sat_query_time = datetime.datetime(*time_list, tzinfo=utc)

        sat = find_sat(pos, sat_start_time)

        position = sat.at(ts.utc(sat_query_time)).position.km
        send_cmd(ticket_serv, "{:0.8f}".format(position[0]))

        query = wait_for_resp(ticket_serv, "?\n").strip()
        print(query)

        send_cmd(ticket_serv, "{:0.8f}".format(position[1]))

        query = wait_for_resp(ticket_serv, "?\n").strip()
        print(query)

        send_cmd(ticket_serv, "{:0.8f}".format(position[2]))

    print(wait_for_resp(ticket_serv, "}"))

finally:
    print("Closing connection")
    ticket_serv.close()
