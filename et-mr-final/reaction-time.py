# Reaction time python file
# Used to connect the two Arduinos and record the time to the database

import serial
import time
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db

# Serial ports for the starter system and the timer system -- make sure these match the ports in Arduino
serStarter = serial.Serial('/dev/cu.usbmodem101', 115200, timeout=.1) #starter
serTimer = serial.Serial('/dev/cu.usbmodem21101', 115200, timeout=.1) #timer

# Firebase credentials 
cred = credentials.Certificate("reaction-time-ba131-firebase-adminsdk-d9ei0-0b00f99ce8.json")
firebase_admin.initialize_app(cred)

# Function to get the name of the person testing the system 
def get_name():
    # global variable so we can use it outside the function
    global name
    name = input("\nWhat is your name?\n")
    read_uart()


# Listen for the START command from arduino, then write to second arduino to listen for the touch sensor 
def read_uart():
    value = serStarter.readline().decode('utf-8').strip()
    if value == "START":
        serTimer.write(b'S')
        # read reaction time 
        read_reaction()
    else:
        # continue looping until it receives start command 
        read_uart()


# read in reaction time and determine if it was a false start or not
def read_reaction():
    value2 = serTimer.readline().decode('utf-8').strip()
    if value2 == "TIME":
        reaction = serTimer.readline().decode('utf-8').strip()
        print(name + "'s Reaction time: " + str(reaction))
        # read_uart()

        # check if it is a false start
        # global variable so we can use it outside the function
        global flagTime
        flagTime = int(reaction)

        # if false start, send a signal to the timer arduino to set off the false start alarm 
        if flagTime <= 100:
           # serStarter.write(b'F')
            serTimer.write(b'F')
            print("False Start - data not added to database")
            # call false start count function to add to the database
            false_start_count()
        else:
            # only save data if not false start
            save_data()  
    else:
        # if the arduino is not sending TIME, continue looping until it does. 
        # the reaction time value is sent after time TIME command is sent 
        read_reaction()



# Function to get the number of false starts from the database
def false_start_count():
    ref = db.reference(path="finalproject", url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
    # the path to the number of false starts, based on the user's name 
    fStartPath = "finalproject/name/" + name + "/false_start"
    refFalse = db.reference(path=fStartPath, url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")

    # get the previous number, if available. 
    # add one to the number, if a previous number does not exist, set to 1
    prevNum = refFalse.get()
    if prevNum is not None:
        global newNum
        newNum = int(prevNum) + 1
        ref.child("name").child(name).child("false_start").set(newNum)
    else:
        ref.child("name").child(name).child("false_start").set(1)

    print("Number of false starts: " + str(newNum))

    
# Function to save the data to the database
# saves reaction time value and calculates and saves current average
def save_data():
    # paths for references
    namePath = "finalproject/name/" + name + "/reaction_time"
    avgPath = "finalproject/name/" + name + "/average"

    # database references for the final project reference, name reference, average reference
    ref = db.reference(path="finalproject", url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
    refName = db.reference(path=namePath, url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
    refAvg = db.reference(path=avgPath, url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")    
    # push reaction time data / instantiate data structure
    ref.child("name").child(name).child("reaction_time").push(flagTime)
    snapshot = refName.get()
    runningTotal = 0
    timeCount = 0
   
    # add times to each other to calculate new average
    for key, val in snapshot.items():
        intConvert = int(val)
        timeCount += 1
        runningTotal += intConvert 

    # get old average and calculate new average
    prevAverage = str(refAvg.get())
    newAverage = str(runningTotal/timeCount)
    print("Average: " + newAverage)
    print("Old Average: " + prevAverage)

    # save new average
    refAvg.set(newAverage)

    # set selected graph to the name of the user so it prints the correct graph in react
    selectedRef = db.reference(path="finalproject/selectedGraph", url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
    selectedRef.set(name)

    

# start the process by prompting for name 
get_name()
