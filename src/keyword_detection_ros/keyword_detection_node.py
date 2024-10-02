#!/usr/bin/env python3

import rospy
import rospkg
import os

#Import service messages and data types
from std_msgs.msg import String
from audio_common_msgs.msg import AudioData


# ros independent imports
import os
import pvporcupine
from struct import unpack_from
from queue import Queue, Empty

DEBUG = False

class KeywordDetection(object):
    def __init__(self):
        if not DEBUG:
            rospy.init_node('keyword_detection_node')
        else:
            rospy.init_node('keyword_detection_node', log_level=rospy.DEBUG)

        # get an instance of RosPack with the default search paths
        self.rospack = rospkg.RosPack()

        #Publishers
        self.keyword_pub = rospy.Publisher(rospy.get_param("~output_topic", "/mbot_speech_recognition/event_in"),
                                           String, queue_size = 5)

        #Subscriptions
        self.event_sub = rospy.Subscriber('~event_in', String, self.event_in_callback)
        self.audio_sub = rospy.Subscriber(rospy.get_param("~audio_topic", "/microphone_node/audio"),
                                          AudioData, self.audio_callback)

        self.rate = rospy.Rate(2)
        self.listening = False

        # Buffers for audio data and recordings
        self.audio_buffer = Queue(maxsize=2)
        self.audio_bytes_buffer = []

        # Load porcupine access key
        with open(self.rospack.get_path('keyword_detection')+"/src/keyword_detection_ros/access_key") as f: 
            self.key = f.read()

        # Get path of keywords
        self.keyword_models = [self.rospack.get_path('keyword_detection') + "/models/" + f for f in os.listdir(self.rospack.get_path('keyword_detection') + "/models") if f.endswith(".ppn")]

        rospy.loginfo("Keyword detection initialized")

        self.event_in_callback(String("e_start"))

    def main(self):
        while not rospy.is_shutdown():
            if self.listening:
                # Read frame from queue
                try:
                    frame = self.audio_buffer.get(block=True, timeout=1)
                except Empty:
                    continue

                # Process frame
                pcm = unpack_from("h" * self.frame_length, frame)
                keyword_index = self.porcupine.process(pcm)

                # Keyword detected, record audio and recognize it
                if keyword_index >= 0:
                    rospy.loginfo(f"Keyword {keyword_index} detected")

                    self.keyword_pub.publish("e_record")

            else:
                self.rate.sleep()
            
    def event_in_callback(self, msg):
        if msg.data == "e_stop" and self.listening:
            self.listening = False

            # Close porcupine instance before exiting
            self.porcupine.delete()

            rospy.loginfo("Stopped listening")

        elif msg.data == "e_start" and not self.listening:
            # Wait 5 seconds for a microphone
            time_start = rospy.Time.now()
            timeout_duration = rospy.Duration(secs=5)
            while self.audio_sub.get_num_connections() == 0:
                # Timeout
                if rospy.Time.now() - time_start > timeout_duration:
                    rospy.logerr("No microphone node detected, did you launch it?")
                    return
                
                rospy.sleep(0.5)
            
            # Check if microphone is recording
            if rospy.has_param("/microphone_node/recording"):
                if not rospy.get_param("/microphone_node/recording"):
                    rospy.logwarn("Microphone is not recording")

            # Get frame length from parameter server
            if rospy.has_param("/microphone_node/frame_length"):
                self.frame_length = rospy.get_param("/microphone_node/frame_length")
            else:
                self.frame_length = 512
                rospy.logwarn(f"Frame length not set. Using default value of {self.frame_length}")

            # Create porcupine instance
            self.porcupine = pvporcupine.create(
                access_key=self.key,
                # keywords=['picovoice', 'computer', 'bumblebee'],
                keyword_paths=self.keyword_models
            )

            self.listening = True
            rospy.loginfo(f"Listening for keyword (sample_rate: {self.porcupine.sample_rate}, frame_len: {self.porcupine.frame_length})")

        rospy.logdebug(f"listening: {self.listening}")

    def audio_callback(self, msg):
        if self.listening:
            self.audio_buffer.put(bytes(msg.data))

def main():
    my_obj = KeywordDetection()
    my_obj.main()
