import paho.mqtt.client as paho
import time
import serial

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your IP
host = "192.168.43.214"
topic = "Mbed"
angle = 0
count = 0

serdev = '/dev/ttyACM0'                # use the device name you get from `ls /dev/ttyACM*`
s = serial.Serial(serdev, 9600)


# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))
    global count
    count = 0


def on_message(mosq, obj, msg):
    global count
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    if(msg.topic == "confirm_angle"):
        temp = msg.payload.decode("utf-8")
        angle = int(str(temp[0:1]))
        time.sleep(1.5)
        ret = mqttc.publish(topic, "GestureUI_STOP", qos=0)
        print("get angle" + str(s))
        if (ret[0] != 0):
            print("Publish failed")
        s.write(bytes("/Tilt_Angle_Detection_START/run/\r", 'UTF-8'))
    elif(msg.topic == "over"):
        count += 1
        print(count)
        if(count >= 10):
            ret = mqttc.publish(topic, "Tilt_Angle_Detection_STOP", qos=0)
            print("Publish Tilt_Angle_Detection_STOP")
            if (ret[0] != 0):
                print("Publish failed")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)
mqttc.subscribe("confirm_angle", 0)
mqttc.subscribe("over", 0)

s.write(bytes("/GestureUI_START/run/\r", 'UTF-8'))
count = 0
# Publish messages from Python
# num = 0
# while True:
#     # ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
#     # if (ret[0] != 0):
#     #         print("Publish failed")
#     mqttc.loop()
#     # time.sleep(1.5)
    # num += 1
# mqttc.publish(topic, "GestureUI_STOP", qos=0)
# Loop forever, receiving messages
mqttc.loop_forever()