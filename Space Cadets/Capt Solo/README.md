# Capt Solo
## Space Cadets
![](https://media.giphy.com/media/rB1JNx9AxMno4/giphy.gif)

*5 points, 1139 solves*

# Challenge Description

In this CTF, questions may come in one of three different flavors. The third is a service running on an external host that will instruct you to connect to a different external host, usually with a program installed on your computer. Connect to the first host, give it your ticket, get the connection string, connect to the second host, solve the problem it asks of you, get the flag, and submit it to the scoreboard to score points. You will only have a short amount of time to be connected to either server, so programming may be required.

### Ticket

Present this ticket when connecting to the challenge:

```
ticket{yankee67900juliet:___a bunch of unguessable stuff___}
```

Don't share your ticket with other teams.

### Connecting

Connect to the challenge on
```
intro3.satellitesabove.me:5002
```

Using netcat, you might run
```
nc intro3.satellitesabove.me 5002
```

### Solving

Your team's flag for this challenge will look something like ```flag{yankee67900juliet:___a bunch of unguessable stuff___}``` .
