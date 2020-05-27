# Attitude Adjustment

Our star tracker has collected a set of boresight reference vectors, and identified which stars in the catalog they correspond to. 
Compare the included catalog and the identified boresight vectors to determine what our current attitude is.
![](https://media.giphy.com/media/LMQ8I9hrBTQjWe3Yaw/giphy.gif)

Note: The catalog format is unit vector `(X,Y,Z)` in a celestial reference frame and the magnitude (relative brightness)

### Ticket

Present this ticket when connecting to the challenge:

```
ticket{charlie47226alpha:GDIXRN78-6xCK34RmdUj_8lTV5t9hxwHiny8skzTpU7h6mnKPmpqYZfmJGu0G2yn7Q}
```

Don't share your ticket with other teams.

### Connecting

Connect to the challenge on
```
attitude.satellitesabove.me:5012
```
Using netcat, you might run
```
nc attitude.satellitesabove.me 5012
```

Sample data as received from challenge:
```
  ID : X,		Y,		Z
--------------------------------------------------
 280 : 0.031398,	0.364757,	0.930573
 356 : -0.068045,	0.271002,	0.960171
 491 : -0.154224,	0.403861,	0.901727
 551 : 0.033056,	0.387761,	0.921167
 632 : 0.042576,	0.227912,	0.972750
 724 : -0.093958,	0.209336,	0.973319
 810 : -0.065109,	0.213299,	0.974815
 868 : 0.017352,	0.233411,	0.972223
 927 : -0.129317,	0.289766,	0.948321
 975 : 0.129272,	0.403796,	0.905670
1016 : -0.129423,	0.266476,	0.955113
1113 : -0.122308,	0.390462,	0.912458
1212 : 0.064682,	0.262305,	0.962815
1378 : 0.044127,	0.216175,	0.975357
1452 : -0.011817,	0.388316,	0.921450
1604 : -0.149580,	0.263641,	0.952953
1649 : -0.115449,	0.462235,	0.879210
1816 : 0.075783,	0.259549,	0.962752
1913 : 0.140753,	0.393908,	0.908309
2005 : -0.001519,	0.385355,	0.922767
2206 : 0.045324,	0.361944,	0.931097
2452 : 0.133572,	0.341204,	0.930450
2489 : -0.126057,	0.291270,	0.948299
```

### Files

You'll need these files to solve the challenge.

[Download Files](https://github.com/AmieDD/ADDVulcan/blob/master/Astronomy%20Astrophysics%20Astrometry%20Astrodynamics%20AAAA/Attitude%20Adjustment/test.txt)

### Solving

Your team's flag for this challenge will look something like flag{charlie47226alpha:___a bunch of unguessable stuff___} .
