from datetime import datetime
from datetime import timedelta
import json   
import os

format = "%Y-%m-%d %I:%M %p"
class Timer:
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.current = datetime.now() - date
        self.longest = self.current
        
    def set_streaks(self):
        current = datetime.now() - self.date
        self.current = current
        if current > self.longest:
            self.longest = current

    def get_dict(self):
        return {"name":self.name, "date":self.date.strftime(format), "current":timedelta_strf(self.current), "longest":timedelta_strf(self.longest)}

def timedelta_strp(string):
    array = string.split(":")
    for i in range(len(array)):
        array[i] = int(array[i])
    return timedelta(days = array[0], seconds = array[1])

def timedelta_strf(delta):
    return f"{delta.days}:{delta.seconds}"

def extract_data(array):
    new_timers = []
    for dict in array:
        date = datetime.strptime(dict["date"], format)

        new_timer = Timer(dict["name"], date)
        new_timer.longest = timedelta_strp(dict["longest"])
        new_timers.append(new_timer)

    return new_timers

def save(timerlist):
    array = []
    for each in timerlist:
        array.append(each.get_dict())
    with open("daysclean.json", "w") as outfile:
        json.dump(array, outfile, indent=4)

def set_date():
    date = input("When was the last time you broke the streak? (MM/DD/YYYY)\n")

    u_i = input("Would you like to input a time? (y/n)\n")
    if u_i == 'y':
        time = input("Input a time (HH:MM AM/PM)\n")
    else: 
        time = "11:59 PM"

    return date + time

def display_choices(array):
    for i, t in enumerate(array):
        print(f'({i+1}) {t.name}')





timers = []
if not(os.path.exists("daysclean.json")):
    f = open("daysclean.json", "w")
    json.dump(timers, f)
    f.close()  
else:
    f = open("daysclean.json", "r")
    timers = json.load(f)
    f.close()

timers = extract_data(timers)



while True:
    print("What would you like to do?")
    tasks = ["Check your progress", 
             "Reset your progress", 
             "Create a new progress tracker", 
             "Remove a progress tracker", 
             "Edit a progress tracker", 
             "Quit"]
    
    for i, task in enumerate(tasks, 1):
        print(f'({i}) {task}')

    while True:
        try:
            u_i = int(input())
            selected = tasks[u_i - 1]
            break

        except:
            pass

    if selected == "Check your progress":
        for each in timers:
            t = each
            t.set_streaks()
            print(t.name + ":")
            print(f"\tCurrent Streak: {t.current.days} days {round(t.current.seconds / 3600)} hours")
            print(t.date.strftime('\t\tStarted %d %b %Y at %I%p'))
            print(f"\tLongest Streak: {t.longest.days} days {round(t.longest.seconds / 3600)} hours\n")

    elif selected == "Reset your progress":
        print("Select a timer to reset:")
        display_choices(timers)
        u_i = input()

        selected = timers[int(u_i)-1]
        selected.date = datetime.strptime(set_date(), "%m/%d/%Y%I:%M %p") 
        timers[int(u_i)-1] = selected
        save(timers)

    elif selected == "Create a new progress tracker":

        name = input("Name your tracker: ")
        loop = True
        while loop:
            exact_date = set_date()

            try:
                date = datetime.strptime(exact_date, '%m/%d/%Y%I:%M %p')
                loop = False
            except:
                print("ERROR: incorrect date/time input")
                loop = True

        new_timer = Timer(name, date)
        timers.append(new_timer)

        save(timers)

    elif selected == "Remove a progress tracker":
        print("Select a timer to delete:")
        display_choices(timers)
        u_i = input()
        
        try:
            timers.remove(timers[int(u_i)-1])
            save(timers)
        except:
            print("ERROR: invalid input")
        
    
    elif selected == "Edit a progress tracker":
        print("Select a timer to edit: ")
        display_choices(timers)
        u_i = input()

        try:
            selected = timers[int(u_i)-1]
            print("What would you like to edit?")
            print(f'(1) Name: {selected.name}')
            print(f'(2) Starting Date: {selected.date.strftime(format)}')
            print(f'(3) Longest Streak: {selected.longest.days} days, {round(selected.longest.seconds /3600)} hours')
            u_i = input()

            if u_i == '1':
                selected.name = input("Enter a new name: ")
            elif u_i == '2':
                print("Enter a new date:")
                selected.date = datetime.strptime(set_date(), '%m/%d/%Y%I:%M %p')
            elif u_i == '3':
                streak = input("Enter the number of days your streak lasted: ")
                selected.longest = timedelta(days = int(streak), seconds = 0)
            else: 
                print("ERROR: invalid input")
            save(timers)
        except:
            print("ERROR: invalid input")

    elif selected == "Quit":
        save(timers)
        break


    