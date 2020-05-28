# Track-a-sat


We have obtained access to the control system for a groundstation's satellite antenna. The azimuth and elevation motors are controlled by PWM signals from the controller. Given a satellite and the groundstation's location and time, we need to control the antenna to track the satellite. The motors accept duty cycles between 2457 and 7372, from 0 to 180 degrees. 

Some example control input logs were found on the system. They may be helpful to you to try to reproduce before you take control of the antenna. They seem to be in the format you need to provide. We also obtained a copy of the TLEs in use at this groundstation.

```python
from pyorbital import tlefile
from pyorbital.orbital import Orbital
import datetime

tle = tlefile.read('IRIDIUM 103', 'active.txt')
orb = Orbital('IRIDIUM 103', tle_file='active.txt')

time = 1586622367.368198

def angle_to_servos(angle):
    val = angle / 180.0
    val = int(val * (7372 - 2457))
    val += 2457
    return val

for i in range(720):
    t = datetime.datetime.utcfromtimestamp(time+i)
    angles = orb.get_observer_look(t, 40.1, -3.21, 0)

    ts = time+i
    a0 = angle_to_servos(angles[0])
    a1 = angle_to_servos(angles[1])
    print(f"{ts}, {a0}, {a1}")
    ```
    
    
