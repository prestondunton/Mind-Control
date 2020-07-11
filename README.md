# mind-control
Term Project for CS370 (Operating Systems) at Colorado State University.  Developed with partner [Andrew Fiel](https://github.com/andrew-fiel).

## Overview

This project connects a Star Wars Force Trainer II headset to social media posts via **mind control**!

The headset is wired to a Raspberry Pi, where brain waves are parsed into a "concentration level".  This concentration level is sent to the project's server, which creates a message (generated randomly from content taught to CS370 students) and posts it to [Reddit](https://www.reddit.com/user/quality-content-bot/).  

This repository has code that reads data from the headset into a Raspberry Pi, and then transmits the request to the server.  For the server side repository, please see my project partner's repository [here](https://github.com/andrew-fiel/mind-control).

## Limitations and Pre-Recorded Data

Because of the COVID-19 pandemic, the wire connecting the headset and the Raspberry Pi could not be soldered to the headset.  This resulted in unreliable performance.  To solve this problem, branwave data was pre recorded using [brain_test.py](https://github.com/prestondunton/mind-control/blob/master/tests/brain_test.py) and cleaned up into the file [byte_stream.txt](https://github.com/prestondunton/mind-control/blob/master/byte_stream.txt).  Inside [Mind_Control.py](https://github.com/prestondunton/mind-control/blob/master/MindControl.py) you will find code that allows for live brainwave data or reading the pre recorded data.  

## Arduino Brain Library

The file [pybrain.py](https://github.com/prestondunton/mind-control/blob/master/pybrain.py) contains a class used to parse the byte stream sent from the headset into different brain wave values.  It is adapted from another project's repository, [Arduino Brain](https://github.com/kitschpatrol/Brain#:~:text=Brain%20is%20an%20Arduino%20Library,from%20Neurosky%2Dbased%20EEG%20headsets.&text=It's%20designed%20to%20make%20it,directly%20in%20your%20Arduino%20sketch.), which was originally written in C++.  All credits due to original authors.




![Project Architecture](https://lh6.googleusercontent.com/B-rpPeLOYhOHS8QmEzBQKBgYecElZS0cA10dlzwLBPbjaZ-hJ0MQzxvE36IQFvUxzh6i0gAMLOdjd_1KzWTet6MmKShN-X_TBVWUm9xm1q4GkOgQCxcKzzUA3zMmjBLxeF9vT8ii6gE)
![User Interface](https://lh5.googleusercontent.com/ZYY-XfKfnV11ZAn_w9qtEh9T4ZcH0M1kGkv3iEgOd6Bh3BSSzCMDemRUDsZqtC9cj2HTlDCmUxLvHUxR8BAI0ltgvw4deFq7RiYW4ukU)
![Example Post](https://user-images.githubusercontent.com/43427035/80314297-f227ad80-87ad-11ea-9b74-37dfa2018cc3.png)
