#!/usr/bin/env python3

import rospy
import message_filters # To Achieve Multiple subscriber
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from std_msgs.msg import String
import threading
import tkinter as tk
import tkinter.font as tkfont
import time

class state_machine_node(object):
    def __init__(self):

        self.forwardSpeed=1000.0
        self.turnSpeed=200.0
        self.turnSpeed=200.0
        self.mode="manual"

        rospy.init_node("state_machine_node", anonymous=True, disable_signals=True)

        # Rate
        self.loop_rate = rospy.Rate(60)
        

        #get VESC path
        vesc1_ns = 'wheel_left'
        vesc2_ns = 'wheel_right'
        if not rospy.has_param('~vesc1_ns'):
            #rospy.signal_shutdown('Please specific the namespace of VESC 1')
            rospy.loginfo("Something Wrong %s", vesc1_ns)
        else:
            vesc1_ns=rospy.get_param('~vesc1_ns')

        if not rospy.has_param('~vesc2_ns') :
            #rospy.signal_shutdown('Please specific the namespace of VESC 2')
            rospy.loginfo("Something Wrong %s", vesc1_ns)
        else:
            vesc2_ns=rospy.get_param('~vesc2_ns')

        rospy.loginfo("vesc 1 namespace: %s", vesc1_ns)
        rospy.loginfo("vesc 2 namespace: %s", vesc2_ns)

        # Node is subscribing to the topic
        self.vesc1_sub = message_filters.Subscriber('vesc1_speed', Float64)
        self.vesc2_sub = message_filters.Subscriber('vesc2_speed', Float64)
        self.state_sub = message_filters.Subscriber('state', String)
        #self.vesc1_sub = rospy.Subscriber('vesc1_speed', Float32, self.callback)
        #self.vesc2_sub = rospy.Subscriber('vesc2_speed', Float32, self.callback)


        # Node is publishing to the topic
        self.vesc1_pub = rospy.Publisher(vesc1_ns + '/commands/motor/speed', Float64, queue_size=10)
        self.vesc2_pub = rospy.Publisher(vesc2_ns + '/commands/motor/speed', Float64, queue_size=10)
        rospy.loginfo("vesc 1 node: %s", vesc1_ns)
        rospy.loginfo("vesc 2 node: %s", vesc2_ns)

        self.state = "C"
        self.inputSpeed_v1=0.0
        self.inputSpeed_v2=0.0

        self.turn= "L"


    def callback(self,vesc1_data, vesc2_data, state_sub):
        if self.mode == "auto":
            #rospy.loginfo("vesc1 speed: %s", vesc1_data.data)
            self.inputSpeed_v1 = vesc1_data.data
            #rospy.loginfo("vesc2 speed: %s", vesc2_data.data)
            self.inputSpeed_v2 = vesc2_data.data
            rospy.loginfo("State :%s", state_sub.data)
            self.state = state_sub.data
        elif self.mode == "hard":
            if state_sub.data in {"L","R"}:
                self.turn= state_sub.data
                rospy.loginfo("Turn :%s", state_sub.data)


    def autoMode(self):
        rospy.loginfo("Change to Auto Mode")
        self.mode="auto"
        self.stop()
    
    def hardcodeMode(self):
        rospy.loginfo("Change to Semi Hardcode Mode")
        self.mode="hard"
        self.stop()
    
    def manualMode(self):
        rospy.loginfo("Change to Manual Mode")
        self.mode="manual"
        self.stop()

    def leftForward(self):
        rospy.loginfo("Manual:Q")
        self.state="Q"
    
    def forward(self):
        rospy.loginfo("Manual:W")
        self.state="W"
    
    def rightForward(self):
        rospy.loginfo("Manual:E")
        self.state="E"
    
    def left(self):
        rospy.loginfo("Manual:A")
        self.state="A"
    
    def stop(self):
        rospy.loginfo("Manual:X")
        self.state="X"
    
    def right(self):
        rospy.loginfo("Manual:D")
        self.state="D"
    
    def fastForward(self):
        rospy.loginfo("Manual:Fast Forward")
        self.state="fastForward"

    #hardcode stuff
    def stiar(self):
        self.fastForward()
        time.sleep(1)
        self.stop()

    
    def stairHandler(self):
        hardcordestate = threading.Thread(target = self.stiar,daemon = True)
        hardcordestate.start()

    
    def rockyRoad(self):
        self.forward()
        time.sleep(1)
        self.stop()

    
    def rockyRoadHandler(self):
        hardcordestate = threading.Thread(target = self.rockyRoad,daemon = True)
        hardcordestate.start()

    def turnLeft(self):
        self.forward()
        time.sleep(1)
        self.stop()
        self.left()
        time.sleep(1.6)
        self.forward()
        time.sleep(1)
        self.stop()

    
    def turnLeftHandler(self):
        hardcordestate = threading.Thread(target = self.turnLeft,daemon = True)
        hardcordestate.start()

    def turnRight(self):
        self.forward()
        time.sleep(1)
        self.stop()
        self.right()
        time.sleep(1.6)
        self.forward()
        time.sleep(1)
        self.stop()

    
    def turnRightHandler(self):
        hardcordestate = threading.Thread(target = self.turnRight,daemon = True)
        hardcordestate.start()



    def gui(self):

        root = tk.Tk()
        root.title("State Machine the GUI")

        #title 
        titlef = tk.Frame(root)
        menubar = tk.Menu(root)
        menuList = tk.Menu(menubar, tearoff=0)
        menuList.add_command(label="Exit", command=lambda:root.destroy())
        menubar.add_cascade(label="Menu", menu=menuList)
        root.config(menu=menubar)

        #title style
        title_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")

        #title body
        title = tk.Label(titlef, text="State Machine the GUI", font=title_font, anchor="e" )
        title.grid(row=0, column=1,sticky="")
        titlef.grid(row=0, column=0, columnspan=5,sticky="")

        #Select Mode
        target = tk.LabelFrame(root, text="Target Mode",width=200)
        target.grid(row=1, column=0, columnspan=5,sticky="W")

        autoModeBut = tk.Button(target, text="Auto", width=10,bd=2, cursor="exchange", command = lambda: self.autoMode())
        autoModeBut.grid(row=1, column=0, columnspan=1) 

        semiHardModeBut = tk.Button(target, text="HardCode", width=10,bd=2, cursor="exchange", command = lambda: self.hardcodeMode())
        semiHardModeBut.grid(row=1, column=1, columnspan=1)

        manualModeBut = tk.Button(target, text="Manual", width=10,bd=2, cursor="exchange", command = lambda: self.manualMode())
        manualModeBut.grid(row=1, column=2, columnspan=1)

        #manualState
        manualSate = tk.LabelFrame(root, text="manualState",width=200)
        manualSate.grid(row=2, column=0, columnspan=5,sticky="W")

        forwardBut = tk.Button(manualSate, text="FastForward", width=10,bd=2, cursor="exchange", command = lambda: self.fastForward())
        forwardBut.grid(row=0, column=0, columnspan=3)

        leftForwardBut = tk.Button(manualSate, text="Q", width=10,bd=2, cursor="exchange", command = lambda: self.leftForward())
        leftForwardBut.grid(row=1, column=0, columnspan=1)

        forwardBut = tk.Button(manualSate, text="W", width=10,bd=2, cursor="exchange", command = lambda: self.forward())
        forwardBut.grid(row=1, column=1, columnspan=1)

        rightForwardBut = tk.Button(manualSate, text="E", width=10,bd=2, cursor="exchange", command = lambda: self.rightForward())
        rightForwardBut.grid(row=1, column=2, columnspan=1)

        leftBut = tk.Button(manualSate, text="A", width=10,bd=2, cursor="exchange", command = lambda: self.left())
        leftBut.grid(row=2, column=0, columnspan=1)

        forwardBut = tk.Button(manualSate, text="Stop", width=10,bd=2, cursor="exchange", command = lambda: self.stop())
        forwardBut.grid(row=2, column=1, columnspan=1)

        rightBut = tk.Button(manualSate, text="D", width=10,bd=2, cursor="exchange", command = lambda: self.right())
        rightBut.grid(row=2, column=2, columnspan=1)

        #hardcode realted
        hardmesh = tk.LabelFrame(root, text="Hard Code",width=200)
        hardmesh.grid(row=3, column=0, columnspan=5,sticky="W")

        stairBut = tk.Button(hardmesh, text="Stair", width=40,bd=2, cursor="exchange", command = lambda: self.stairHandler())
        stairBut.grid(row=1, column=0, columnspan=4)

        rockyBut = tk.Button(hardmesh, text="Rocky Road", width=40,bd=2, cursor="exchange", command = lambda: self.rockyRoadHandler())
        rockyBut.grid(row=2, column=0, columnspan=4)

        hardTurnLeftBut = tk.Button(hardmesh, text="Hardcode Left", width=20,bd=2, cursor="exchange", command = lambda: self.turnLeftHandler())
        hardTurnLeftBut.grid(row=3, column=0, columnspan=2)

        hardTurnRightBut = tk.Button(hardmesh, text="Hardcode Right", width=20,bd=2, cursor="exchange", command = lambda: self.turnRightHandler())
        hardTurnRightBut.grid(row=3, column=2, columnspan=2)
    
        root.mainloop()
        

    def start(self):

        # Tells rospy the name of the node.
        # Anonymous = True makes sure the node has a unique name. Random
        # numbers are added to the end of the name. 

        #Only for multiple subscribers
        ts = message_filters.ApproximateTimeSynchronizer([self.vesc1_sub, self.vesc2_sub, self.state_sub], 10, 0.01, allow_headerless=True)
        ts.registerCallback(self.callback)

        # spin() simply keeps python from exiting until this node is stopped
        while not rospy.is_shutdown():
            rospy.loginfo("Mode: %s State: %s",self.mode, self.state)
            if self.state == "C":#custom speed for PID
                rospy.loginfo(" \nvesc1 speed: %s\n vesc2 speed: %s", self.inputSpeed_v1, self.inputSpeed_v2)
                self.vesc1_pub.publish(self.inputSpeed_v1)
                self.vesc2_pub.publish(self.inputSpeed_v2)
            elif self.state == "W": #forward
                self.vesc1_pub.publish(self.forwardSpeed)
                self.vesc2_pub.publish(self.forwardSpeed)
            elif self.state == "E": #forward + right
                self.vesc1_pub.publish(self.forwardSpeed+self.turnSpeed)
                self.vesc2_pub.publish(self.forwardSpeed)
            elif self.state == "Q": #forward + left
                self.vesc1_pub.publish(self.forwardSpeed)
                self.vesc2_pub.publish(self.forwardSpeed+self.turnSpeed)
            elif self.state == "S": #Stop
                self.vesc1_pub.publish(0)
                self.vesc2_pub.publish(0)
            elif self.state == "A": #rotaed left
                self.vesc1_pub.publish(-self.forwardSpeed)
                self.vesc2_pub.publish(self.forwardSpeed)
            elif self.state == "D": #rotaed right
                self.vesc1_pub.publish(self.forwardSpeed)
                self.vesc2_pub.publish(-self.forwardSpeed)
            elif self.state == "X": #backword
                self.vesc1_pub.publish(0)
                self.vesc2_pub.publish(0)
            elif self.state == "fastForward":
                self.vesc1_pub.publish(2000)
                self.vesc2_pub.publish(2000)
            
                
        
        #while not rospy.is_shutdown():
            #self.vesc1_pub.publish(1.0324)
            #self.vesc2_pub.publish(9.7777)

        #    self.loop_rate.sleep()
        

if __name__ == '__main__':
    my_node = state_machine_node()
    t = threading.Thread(target = my_node.gui,daemon = True)
    t.start()
    my_node.start()
    
