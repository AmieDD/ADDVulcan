# Track-a-sat


We have obtained access to the control system for a groundstation's satellite antenna. The azimuth and elevation motors are controlled by PWM signals from the controller. Given a satellite and the groundstation's location and time, we need to control the antenna to track the satellite. The motors accept duty cycles between 2457 and 7372, from 0 to 180 degrees. 

Some example control input logs were found on the system. They may be helpful to you to try to reproduce before you take control of the antenna. They seem to be in the format you need to provide. We also obtained a copy of the TLEs in use at this groundstation.

## Solution

On connect we're given the groundstation location, satellite to track, and the start time:

```
$ nc trackthesat.satellitesabove.me 5031       
Ticket please:
ticket{papa81666echo:GOhS4jUEwN0qqyRhm4zYrpISPTyKMTW6Bpk6LIcrxAU6M3rZHU93ynmjSOicpmt5Cg}
Track-a-sat control system
Latitude: -3.21
Longitude: 40.1
Satellite: IRIDIUM 103
Start time GMT: 1586622367.368198
720 observations, one every 1 second
Waiting for your solution followed by a blank line...
```

No information is given about the format of the solution, but we can check one of the example solutions and see that we should produce `<timestamp>, <PWM0>, <PWM1>`:

```
$ head solution0.txt                
1586789933.820023, 6001, 2579
1586789934.820023, 5999, 2581
1586789935.820023, 5997, 2583
1586789936.820023, 5995, 2585
1586789937.820023, 5994, 2587
1586789938.820023, 5992, 2589
1586789939.820023, 5990, 2591
1586789940.820023, 5988, 2593
1586789941.820023, 5987, 2594
1586789942.820023, 5985, 2596
```

We wrote a Python script using `pyorbital` that calculates the look angles for each of the observation times, converts the angles into the servo PWM range, and prints them all out:

```python
from pyorbital.orbital import Orbital
import datetime

orb = Orbital('IRIDIUM 103', tle_file='active.txt')

time = 1586622367.368198

def angle_to_servos(angle):
    val = angle / 180.0
    val = int(val * (7372 - 2457))
    val += 2457
    return val

for i in range(720):
    ts = time+i
    t = datetime.datetime.utcfromtimestamp(ts)
    angles = orb.get_observer_look(t, 40.1, -3.21, 0)

    a0 = angle_to_servos(angles[0])
    a1 = angle_to_servos(angles[1])
    print(f"{ts}, {a0}, {a1}")
```

The output is pasted into netcat and we get the flag:

```
Waiting for your solution followed by a blank line...

1586622367.368198, 2811, 2786
1586622368.368198, 2812, 2789
[...]
1586623085.368198, 7165, 2481
1586623086.368198, 7165, 2479

Congratulations: flag{papa81666echo:GKv8F33MXydFGvekVaXuuooNx3mlIToFvJXma9gV9oezgL4p3ne6pETKyVz8YGVGVVYtAhiDuOTG4C7Go94d780}
```
