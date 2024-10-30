# Keyword Detection Node

## Overview

The Keyword Detection Node is responsible for detecting specific keywords in audio data and publishing events to a ROS topic. This node is designed to work seamlessly with other speech processing nodes in the TIAGo robot's speech recognition pipeline.

## Features
- **Keyword Detection**: Detects predefined keywords in the audio stream.
- **ROS Integration**: Publishes detection events to a ROS topic for use by other nodes.

## Requirements

- ROS version: Noetic
- Dependencies:
    - [audio_common](https://wiki.ros.org/audio_common)
    - [pvporcupine](https://github.com/Picovoice/porcupine)

## Installation

### 0. Install the audio_common package

```bash
sudo apt-get install ros-noetic-audio-common
```

### 1. Clone the repository
```bash
cd ~/<your_workspace>/src
git clone https://github.com/socrob/keyword_detection.git
```

### 2. Install dependencies

Navigate to the cloned repository and install the required dependencies:

```bash
cd keyword_detection
pip install pvporcupine
```

### 3. Build the workspace
Navigate to your catkin workspace and build the package:

```bash
cd ~/<your_workspace>
catkin build
```

### 4. Source the setup file
After building, source the workspace to update the environment:

```bash
source ~/<your_workspace>/devel/setup.bash
```

### 5. Create a Picovoice access key and porcupine model.
Signup or Login to [Picovoice Console](https://console.picovoice.ai/signup) to get your access key. This key should be stored in `src/keyword_detection_ros/access_key`.

Then, in the same console you can create and download the `.ppn` models to recognize custom keywords. These models should be stored in the `models` folder.

## Usage

### Launching the Node

To launch the keyword detection node, use the following command:

```bash
roslaunch keyword_detection keyword_detection.launch
```

#### Launch File Arguments

The launch file `keyword_detection.launch` accepts several arguments to customize the behavior of the keyword detection node:

- `audio_topic`: Specifies the ROS topic for audio data. Default is `"/microphone_node/audio"`.
- `output_topic`: Specifies the ROS topic for detection events. Default is `"/mbot_speech_recognition/event_in"`.
- `keyword_models`: Path to the keyword models. Default is `"models"`.

These arguments allow you to tailor the keyword detection node's behavior to match your specific requirements and environment.
