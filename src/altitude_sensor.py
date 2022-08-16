import sys
sys.path.insert(0, '../..')

import rospy
import numpy as np

from serial import Serial as device
from std_msgs.msg import String, Float64
# from altitude_sensor.msg import sensor_data
from panda3d.core import StringStream

REPLY_SIZE = 20
TIMEOUT = 1000
PORT = 'loop://'

serial_port = "/dev/ttyUSB0"
msg_shift = 0
alt_msg_begin = msg_shift
alt_msg_end = msg_shift+6
volt_msg_begin = msg_shift + 8
volt_msg_end = msg_shift + 15

rep = np.array(range(0,21,1))
reply = chr(rep[REPLY_SIZE])

sensor_frequency = 60   # sensor freq in hz

def talker():
  pub = rospy.Publisher('standoff', Float64, queue_size=10)
  rospy.init_node('so_sensor', anonymous=True)
  r = rospy.Rate(sensor_frequency)
  msg = Float64()

  while not rospy.is_shutdown():

    try: 
      device.open(PORT)
    except rospy.ROSException as e:
      print("Interrupted")
      pass

    for x in range(alt_msg_begin,alt_msg_end):
      ss1 = reply[x]
    standoff = ss1
    msg.data = standoff
    # msg.altitude = standoff
    # msg.voltage = 0
    # msg.header.frame_id="standoff sensor"
      
    rospy.loginfo(msg)
    pub.publish(msg)

    if (reply[msg_shift+7]!='m'):
      msg_shift = msg_shift + msg_shift

      volt_msg_begin = msg_shift+10
      volt_msg_end = msg_shift+14
      alt_msg_begin = msg_shift
      alt_msg_end = msg_shift+5

      if (msg_shift >= 20): msg_shift = msg_shift - 20
      if (volt_msg_begin>=20): volt_msg_begin = volt_msg_begin - 20
      if (volt_msg_end>=20): volt_msg_end = volt_msg_end - 20 
      if (alt_msg_begin>=20): alt_msg_begin = alt_msg_begin - 20
      if (alt_msg_end>=20): alt_msg_end = alt_msg_end - 20
    
    r.sleep()

  rospy.spin()

if __name__ == "__main__":
  try: talker()
  except rospy.ROSInterruptException:
    pass