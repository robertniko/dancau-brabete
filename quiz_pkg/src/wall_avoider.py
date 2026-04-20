#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class DB_WallAvoider:
    def __init__(self):
        rospy.init_node('db_wall_avoider_node')
        
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.twist_msg = Twist()
        
        rospy.loginfo("DB's Wall Avoider Node Started. Listening to /scan and publishing to /cmd_vel...")

    def scan_callback(self, msg):
        total_ranges = len(msg.ranges)
        
        front_idx = 0
        left_idx = total_ranges // 4
        right_idx = (total_ranges * 3) // 4
        
        front_reading = msg.ranges[front_idx]
        left_reading = msg.ranges[left_idx]
        right_reading = msg.ranges[right_idx]

        if left_reading < 1.0:
            self.twist_msg.linear.x = 0.0
            self.twist_msg.angular.z = -0.5
            rospy.loginfo("[DB] Obstacle on LEFT. Turning RIGHT.")

        elif right_reading < 1.0:
            self.twist_msg.linear.x = 0.0
            self.twist_msg.angular.z = 0.5
            rospy.loginfo("[DB] Obstacle on RIGHT. Turning LEFT.")

        elif front_reading < 1.0:
            self.twist_msg.linear.x = 0.0
            self.twist_msg.angular.z = 0.5
            rospy.loginfo("[DB] Obstacle in FRONT. Turning LEFT.")

        else:
            self.twist_msg.linear.x = 0.3
            self.twist_msg.angular.z = 0.0
            rospy.loginfo("[DB] Path clear. Moving FORWARD.")

        self.cmd_pub.publish(self.twist_msg)

if __name__ == '__main__':
    try:
        DB_WallAvoider()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
