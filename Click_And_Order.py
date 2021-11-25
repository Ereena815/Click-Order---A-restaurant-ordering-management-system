##
#    Embedded Systems Development
#    Project - Click & Order
#    Name : Ereena Bagga
#    Student ID : 2010993040
##

## Import Statements

# Importing random library to generate random Client IDs for the MQTT broker
import random

# Importing time and datetime libraries to calculate pickup time for each order
import time
from datetime import datetime
from datetime import timedelta

# Importing library for MQTT Client
from paho.mqtt import client as mqtt_client

# Importing libraries to work with LEDs and LCD screen
import RPi.GPIO as GPIO
from gpiozero import LED

# Importing tkinter library and its associated font to create a GUI
from tkinter import *
import tkinter.font as FONT

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

## Pin Definitions

redLED = LED(12)
yellowLED = LED(7)
greenLED = LED(8)

## Broker Definitions

broker = 'broker.hivemq.com'
port = 1883
topic = "ClickOrder"

# Generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

username = 'Ereena'
password = 'Welcome@deakin05'

## GUI Defintions

win = Tk()
win.title("CLICK & ORDER")
myFont = FONT.Font(family = 'Helvetica', size = 14, weight = 'bold')

## GUI Frame Definitions

rightFrame = Frame(win)
rightFrame.pack(side = RIGHT)

middleFrame = Frame(win)
middleFrame.pack(side = RIGHT)

# Counts the number of orders
counter = 0

## Event Functions

# This method connects to the MQTT broker and returns the client
def connectMqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("\nConnected to MQTT Broker!")
        else:
            print("\nFailed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# This method subscribes to a particular topic and prints the received message onto the GUI
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        now = datetime.now()
        pickup_time = now + timedelta(minutes = 15)
        pickup_time_string = pickup_time.strftime("%d/%m/%Y %H:%M:%S")
        global counter
        counter +=1
        yellowLED.off()
        greenLED.off()
        redLED.on()
        orders.insert(counter, "Order ID - " + str(counter) + ", Received Items - " + str(msg.payload.decode()) + ", Pickup Time - " + str(pickup_time_string))
        redLED.off()
        yellowLED.on()
        
    client.subscribe(topic)
    client.on_message = on_message

# This method loops the client forever in order to keep on receiving messages from the broker
def run():
    client = connectMqtt()
    greenLED.on()
    time.sleep(5)
    subscribe(client)
    rc = 0
    
    while (rc == 0):
        client.loop_forever()

# This method destroys the window and sets the GPIO pins back to their intial settings
def close():
    GPIO.cleanup()
    orders.pack( side = LEFT, fill = BOTH )
    win.destroy()
    
## Widget Definitions

heading = Label(middleFrame, text = " ***************************=============************************* WELCOME TO CLICK & ORDER ***************************=============*************************", font = myFont, fg = 'brown')
heading.pack(side = TOP)

viewOrdersButton = Button(middleFrame, text = 'VIEW ORDERS', font = "30", command = run, bg = 'brown', height = 1, width = 10)
viewOrdersButton.pack(side = TOP)

scrollBar = Scrollbar(rightFrame)
scrollBar.pack(side = RIGHT, fill = Y)

orders = Listbox(middleFrame, yscrollcommand = scrollBar.set)
orders.pack( side = LEFT, fill = BOTH )
  
scrollBar.config(command = orders.yview )

exitButton = Button(middleFrame, text = 'EXIT', font = myFont, command = close, bg = 'bisque2', height = 1, width = 5)
exitButton.pack(side = BOTTOM)

win.protocol("WM_DELETE_WINDOW",close) # exit cleanly

win.mainloop() # loop forever
