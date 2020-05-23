Track-a-Sat RF Side Channel Detector
====================================

We lost our direct access to control the Track-a-Sat groundstation antenna (see earlier challenge), but we have a new source of information on the groundstation. From outside the compound, we have gathered 3 signal recordings of radio emissions from the cables controlling the antenna motors. We believe the azimuth and elevation motors of each antenna are controlled the same way as the earlier groundstation we compromised, using a PWM signal that varies between 5% and 35% duty cycle to move one axis from 0 degrees to 180 degrees. We need to use these 3 recordings to determine where each antenna was pointing, and what satellite it was tracking during the recording period.

To help you in your calculations, we have provided some example RF captures from a different groundstation with a similar antenna system, where we know what satellites were being tracked. You will want to use that known reference to tune your analysis before moving on to the unknown signals. The example files are in a packed binary format. We have provided a script you can use to translate it to a (large) CSV if you like. The observations are sampled at a rate of 102400Hz and there are two channels per sample (one for azimuth, the other for elevation).

