# Motion Sleeve
HealthBuilder is a hardware/software project that aims to improve the rehabilitation of stroke survivors.

# Motivation
FES(Functional Electronic Stimulation) devices are commonly used during the rehabilitation process of patients with neurological conditions that affect their motor functions. This report focuses on developing a wearable and flexible FES system that will offer more customizability for a lower price than the available options, investigating various FES techniques and devices. The research documents the development process of a full-stack web application made in conjuncture with the device to make it brighter. The system introduces an array of IMUs (Inertial Measurement Units) to track the flexion and extension of the fingers and feeds the data to the controller driving multiple FES channels, which allows for performing more dexterous fingers and hand movements. This project achieved an accurate motion tracking system that can differentiate the wrist, hand joint flexion levels and an extendable FES controller capable of driving multiple FES output channels.

# Tech Stack
Software:

* React
* Three.Js
* MongoDB
* Flask
* Blender

Hardware:
* Raspberry Pi 3B
* MPU9250

# System Architecture
Below is a high-level diagram of the system:

![This is an image](/graphs/diagram.png)

This architecture fully meets the application requirements and will provide efficient operation. 
Each component is isolated and independent from the other, giving the system the necessary level of maintainability.
The data flows striclty from one component in the pipeline to the next.

# User Stories( Functionality )
- [x] User can register and login.
- [x] User can create motion presets.
- [x] User can move individual fingers in the 3d model.
- [x] User can store finger positions in the motion preset using controls.
- [x] User can reproduce the wrist motion on hardware.
- [x] User can reproduce the finger motion on hardware.

# Demonstration

# Index finger control
![this is an image](https://media.giphy.com/media/GxZn9zZTGNzLAcRTip/giphy.gif)
<img src="/graphs/index50_web.png" data-canonical-src="/graphs/index50_web.png " height="480" />

# Wrist control
![this is an image](https://media.giphy.com/media/em5TiJ2sKa7B3ALfnU/giphy.gif)

# Multiple finger control (Grab or Pinch)
![this is an image](https://media.giphy.com/media/kuDLJ7hnMOmzlZehRj/giphy.gif)
