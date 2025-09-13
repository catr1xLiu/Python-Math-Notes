import sys
from ics import Calendar, Event
from datetime import date, time, datetime
from rich.console import Console
from rich.table import Table

console = Console()

component_types = ["LEC", "TUT", "LAB"]

class Component:
    def __init__(self, number:int, section:int, componentType:str, 

class Course:
    def __init__(self, code:str, name:str, status:str, units:float, grading:str, )

def processCourse(courseSchedule:str) -> :
    

def main():
    console.print(":wave: Welcome to quest calender converter!!!")
    
    classScheduleText = ""
    with open("./schedule.txt", "r") as f:
        classScheduleText = f.read()
   
    


if __name__ == '__main__':
    main()
