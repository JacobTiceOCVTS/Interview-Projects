import time

taskList = []
optionsList = ["print", "add", "remove", "complete", "exit"]

print("Welcome to my To-Do App")

loopProgram = True

class Task:

    def __init__(self, taskDescription, priority):
        self.taskDescription = taskDescription
        self.priority = priority
        self.status = False

    def printSelf(self):
        time_delay = 0.05
        time.sleep(time_delay)
        print(f"Task: {self.taskDescription}")
        time.sleep(time_delay)
        print(f"Priority: {self.priority}")
        time.sleep(time_delay)
        print(f"Completed: {self.status}")
        time.sleep(time_delay)
        print("<====================================>")
        

def printTasks(list):
    print("<====================================>")
    for task in list:
        task.printSelf()

def addTask():
    print("Input task description: ")
    taskDesc = input(">>")
    print("Input task priority: ")
    taskPrio = input(">>")
    taskList.append(Task(taskDesc, taskPrio))
    print("Task Created")

def removeTask():
    printTasks(taskList)
    print("What number task would you like removed")
    taskToRemove = int(input(">>"))
    if taskToRemove <= len(taskList) and taskToRemove > 0:
        taskList.pop(taskToRemove-1)
    else:
        print("Task not found")

def completeTask():
    printTasks(taskList)
    print("What number task would you like to mark complete")
    taskToComplete = int(input(">>"))
    if taskToComplete <= len(taskList) and taskToComplete > 0:
        taskList[taskToComplete-1].status = True
    else:
        print("Task not found")

while (loopProgram):
    print("What would you like to do?")
    print(", ".join(optionsList))
    userInput = input(">>")
    match userInput:
        case "print":
            printTasks(taskList)
        case "add":
            addTask()
        case "remove":
            removeTask()
        case "complete":
            completeTask()
        case "exit":
            loopProgram = False
        case _:
            print("Invalid Command")