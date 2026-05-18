#!/usr/bin/env python3
import rospy
import actionlib
from drone_action_quiz.msg import DroneMoveAction, DroneMoveFeedback, DroneMoveResult
from std_msgs.msg import Empty

class DroneActionServer:
    def _init_(self):
        # Inițializăm serverul de acțiune
        self._as = actionlib.SimpleActionServer(
            "drone_action_msg", 
            DroneMoveAction, 
            execute_cb=self.execute_callback, 
            auto_start=False
        )
        self._as.start()

        # Publisheri pentru controlul dronei ardrone
        self.pub_takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.pub_land = rospy.Publisher('/ardrone/land', Empty, queue_size=1)

        # Variabile pentru feedback și rezultat
        self._feedback = DroneMoveFeedback()
        self._result = DroneMoveResult()

        rospy.loginfo("Serverul de actiune pentru drona a pornit.")

    def execute_callback(self, goal):
        r = rospy.Rate(1) # 1 Hz -> O data pe secunda
        success = True
        command = goal.command.upper() # Convertim în litere mari pentru siguranță

rospy.loginfo(f"Comanda primita: {command}")

        # Logica pentru TAKEOFF
        if command == "TAKEOFF":
            self._feedback.status = "take off"
            # Trimitem comanda de decolare dronei
            self.pub_takeoff.publish(Empty())

            # Simulăm procesul de decolare (ex: durează 4 secunde în care dăm feedback)
            for i in range(4):
                if self._as.is_preempt_requested():
                    rospy.loginfo("Comanda a fost anulata!")
                    self._as.set_preempted()
                    success = False
                    break
                self._as.publish_feedback(self._feedback)
                r.sleep() 
        # Logica pentru LAND
        elif command == "LAND":
            self._feedback.status = "landing"
            # Trimitem comanda de aterizare dronei
            self.pub_land.publish(Empty())

            # Simulăm procesul de aterizare
            for i in range(4):
                if self._as.is_preempt_requested():
                    rospy.loginfo("Comanda a fost anulata!")
                    self._as.set_preempted()
                    success = False
                    break
                self._as.publish_feedback(self._feedback)
                r.sleep()
        else:
            rospy.logwarn("Comanda invalida! Foloseste TAKEOFF sau LAND.")
            success = False

        # Dacă totul a decurs cu succes, setăm starea finalizată (fără rezultat întors conform cerinței)
        if success:
            rospy.loginfo(f"Actiunea {command} s-a finalizat cu succes.")
            self._as.set_succeeded(self._result)

if _name_ == '_main_':
    rospy.init_node('drone_action_server_node')
    server = DroneActionServer()
    rospy.spin()
