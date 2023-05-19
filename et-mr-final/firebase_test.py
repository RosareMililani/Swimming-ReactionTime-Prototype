import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
import time

cred = credentials.Certificate("reaction-time-ba131-firebase-adminsdk-d9ei0-0b00f99ce8.json")
firebase_admin.initialize_app(cred)


name = input("Enter your name: ")
time = input("Enter reaction time: ")


namePath = "test4/name/" + name + "/reaction_time"
avgPath = "test4/name/" + name + "/average"

ref = db.reference(path="test4", url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
refName = db.reference(path=namePath, url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")
refAvg = db.reference(path=avgPath, url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")


ref.child("name").child(name).child("reaction_time").push(time)


snapshot = refName.get()
runningTotal = 0
timeCount = 0
print(name + "'s Reaction Time Values:")
for key, val in snapshot.items():
    intConvert = int(val)
    timeCount += 1
    runningTotal += intConvert 
    print(str(timeCount) + ". " +val)

prevAverage = str(refAvg.get())
newAverage = str(runningTotal/timeCount)
print("Average: " + newAverage)
print("Old Average: " + prevAverage)


selected = db.reference(path="finalproject/selectedGraph", url="https://reaction-time-ba131-default-rtdb.firebaseio.com/")

selectedGraph = input("Whose graph would you like to see?: ")
selected.set(selectedGraph)

refAvg.set(newAverage)
