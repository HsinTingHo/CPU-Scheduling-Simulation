class Task: #A process is divided into tasks by CPU bust time in the trace
    ProcessName = ''
    StartTime = 0 #The time I/O is finished
    ProcessTime = 0 #CPU burst
    IOtime = 0
    TimeOnCPU = 0 #used in MLFQ to record the amount of time has been spend on CPU
    QueLevel = 0 #All process starts at Q1
    DownGraded =False #Marked to true when downgraded to a lower queue
    CPUburst = 0 #Used as a copy of Process Time in MLFQ
    def __init__(self, start, process, io, pName): #initialize a task
        self.StartTime = start
        self.ProcessTime = process
        self.IOtime = io
        self.ProcessName = pName
        self.QueLevel = 1
        self.CPUburst = process
        print('ProcessName: '+pName)

def addtoReadySorted(readyList, P):#add to readyList with ascending CPU burst
    index = 0

    if len(readyList) == 0:
        print('adding to empty list')
        readyList.append(P)
    else:

        for w in readyList:
            #print('w '+str(w.StartTime))
            if P.ProcessTime < w.ProcessTime:    #if process start time is smaller, insert
                index = readyList.index(w)
                readyList.insert(index, P)
                break
            elif w == readyList[-1]:      #if process start time is the largest, append
                readyList.append(P)
                break
            else:
                continue
    return readyList

def addtoListSorted(anyList, P):#add to readyList with ascending StartTime
    index = 0
    print('adding '+P.ProcessName+' to waitingList')
    if len(anyList) == 0:
        print('adding to empty list')
        anyList.append(P)
    else:

        for w in anyList:
            #print('w '+str(w.StartTime))
            if P.StartTime < w.StartTime:    #if process start time is smaller, insert
                index = anyList.index(w)
                anyList.insert(index, P)
                break
            elif w == anyList[-1]:      #if process start time is the largest, append
                anyList.append(P)
                break
            else:
                continue
    return anyList

def makeProcessStack(traceDic):#Divide process trace by its CPU burst. Store each CPU burst, I/O in a Task object.
    processStackList = []      #Store all the tasks in order in a dictionary. use process name as key.
    cpu = io = 0
    for P in traceDic:
        processStack = []
        trace= traceDic[P]
        last = len(trace)-1
        count = 0
        for time in trace:
            if count%2 == 0:
                cpu = time
                if count == last:
                    task =  Task(0, cpu, 0, P)
                    processStack.append(task)
            else:
                io = time
                task =  Task(0, cpu, io, P)
                processStack.append(task)
            count += 1
        processStackList.append(processStack)
    return processStackList#processStackList = [[{P1,cpu, io}...],[{P2,cpu, io}...],...,[{P8, cpu, io}]]

def display(CPUruntime, timeUnit, CurrentProcess, waitingList, readyList):#Display info for each context switch
    print('Current time: '+str(timeUnit))
    if len(readyList)>0:
        print('Next Process on the CPU: '+ readyList[0].ProcessName)
    else:
        print('Next Process on the CPU: None')
    print('\n******************************************************************\n')
    print('List of processes in the ready queue:\n')
    print(' Processes    Burst    Queue')
    if len(readyList) == 0:
        print('    '+'[ empty ]\n')
    else:
        for r in readyList[1:]:
            print('    '+r.ProcessName+'        '+str(r.ProcessTime)+'        Q'+str(r.QueLevel))
    print('******************************************************************\n')
    print('List of processes in the I/O:\n')
    print(' Processes    Remaining I/O time')
    if len(waitingList) == 0:
        print('    '+'[ empty ]\n')
    else:
        for w in waitingList:
          ioRemain = w.StartTime-timeUnit
          print('    '+w.ProcessName+'        '+str(ioRemain))
    print('\n******************************************************************')
    print('******************************************************************\n')

def calcResult(timeUnit, downTime, cpuTime, startTimeDic, finishTimeDic, WaitTimeDic):#Calculat average turnaround time, average waitting time, and average response time and store result in a dictionary
    resultDic = {}
    Ttr =0
    totalTtr = 0
    waitTime = 0
    resTime = 0
    resultDic['cpuUtil'] = (float(cpuTime)/float(timeUnit))*100
    print('*******************************************************')
    print('The Simulation is Ended.')
    print('Total time used: '+str(timeUnit)+' time units')
    print('*******************************************************')
    for key in startTimeDic: #add part to handle a list of start times and a list of end times
        if len(startTimeDic[key]) > 1:
            Ttr = finishTimeDic[key][-1]#-startTimeDic[key][1]
            resultDic[key] = 'Tw:'+ str(WaitTimeDic[key]) + ' / Ttr: '+str(Ttr) + ' /Tr: '+ str(startTimeDic[key][1])
            totalTtr += Ttr
            resTime += startTimeDic[key][1]
        waitTime += WaitTimeDic[key]

    resultDic['avgTtr'] = float(totalTtr)/8.0
    resultDic['avgTw']=float(waitTime)/8.0
    resultDic['avgTr']=float(resTime)/8.0
    resultDic['Total Time'] = timeUnit
    return resultDic #keys = [cpuUtil, PnTtr, avgTtr, avgTw]

def FCFS(traceDic):
        #store the start time of each task
        StartTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
        #store the end time of each task
        EndTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
        #store the wait time of each task
        WaitTimeDic = {'P1':0,'P2':0,'P3':0,'P4':0,'P5':0,'P6':0,'P7':0,'P8':0}
        timeUnit = CPUruntime = downTime = processIndex = tempStartTime = waitTime = 0
        processStackList= makeProcessStack(traceDic)
        readyList = []
        waitingList = []
        finishList = []
        resultDic = {}
        running = True
        #add first task of every process to readyList and set current task to none
        for PS in processStackList:
            PS[0].StartTime = tempStartTime
            tempStartTime += PS[0].ProcessTime
            readyList.append(PS[0])
            PS.pop(0)
        current = None
        while running:
            #Move process to readyList
            if len(waitingList)>0 and waitingList[0].StartTime <= timeUnit:
                for w in waitingList:
                    if w.StartTime <= timeUnit:
                        readyList.append(w)
                        waitingList.remove(w)

            if not current:#When CPU is not occupied
                if processStackList or len(readyList) > 0 or len(waitingList)>0:
                    if len(readyList) > 0:
                        current = readyList[0] #Move the first process in readyList to running state
                        display(CPUruntime, timeUnit, current, waitingList, readyList)
                        current.StartTime = timeUnit
                        readyList.pop(0)
                        StartTimeDic.get(current.ProcessName).append(timeUnit)
                    else:#If the readyList is empty, increament down time
                        downTime += 1
                else:
                    running = False #stop the loop
                    resultDic = calcResult(timeUnit, downTime, CPUruntime, StartTimeDic, EndTimeDic, WaitTimeDic) #calculate results
                    for key in resultDic:
                        print(key+': '+str(resultDic[key])) #display results
            else:#When CPU is occupied
                CPUruntime += 1
                if timeUnit == (current.StartTime + current.ProcessTime):#if the running process is finished
                    EndTimeDic[current.ProcessName].append(timeUnit)#record the end time
                    index = int(current.ProcessName[-1])-1
                    try:#handle error thrown when the current process is the last task
                        nextTaskInProcess = processStackList[index][0]
                        nextTaskInProcess.StartTime = timeUnit + current.IOtime
                        waitingList = addtoListSorted(waitingList, nextTaskInProcess)
                        processStackList[index].pop(0)
                    except:
                        count = 0
                        for stack in processStackList:#if all the tasks are finished, wipe out the processStackList
                            if len(stack) == 0:
                                count += 1
                                if count == len(processStackList):
                                    processStackList.clear()
                    current = None
                    continue
            timeUnit += 1
            #acumulating waiting time for each process in WaitTimeDic
            if len(readyList)>0:
                for r in readyList:
                    WaitTimeDic[r.ProcessName] += 1

def SJF(traceDic):
    StartTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
    EndTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
    WaitTimeDic = {'P1':0,'P2':0,'P3':0,'P4':0,'P5':0,'P6':0,'P7':0,'P8':0}
    timeUnit = CPUruntime = downTime = processIndex = tempStartTime = waitTime = 0
    processStackList= makeProcessStack(traceDic)
    readyList = []
    waitingList = []
    finishList = []
    resultDic = {}
    running = True
    #add first task of every process to readyList and set current task to none
    for PS in processStackList:
        PS[0].StartTime = tempStartTime
        tempStartTime += PS[0].ProcessTime
        readyList = addtoReadySorted(readyList, PS[0])
        PS.pop(0)
    current = None
    while running:
        if len(waitingList)>0 and waitingList[0].StartTime <= timeUnit:
            readyList = addtoReadySorted(readyList,waitingList[0]) #Move the process to readyList and sort the list by CPU burst time
            waitingList.pop(0)
        if not current:#CPU not occupied
            if processStackList or len(readyList) > 0 or len(waitingList)>0:
                if len(readyList) > 0:
                    current = readyList[0]#Move the first process on readyList to running state
                    display(CPUruntime, timeUnit, current, waitingList, readyList)#display context switch info
                    current.StartTime = timeUnit
                    readyList.pop(0)
                    StartTimeDic.get(current.ProcessName).append(timeUnit)#store the start time
                else:
                    downTime += 1
            else:
                running = False
                resultDic = calcResult(timeUnit, downTime, CPUruntime, StartTimeDic, EndTimeDic, WaitTimeDic)
                for key in resultDic:
                    print(key+': '+str(resultDic[key]))
        else:#CPU is occupied
            CPUruntime += 1
            if timeUnit == (current.StartTime + current.ProcessTime):#the process on running state is finished
                EndTimeDic[current.ProcessName].append(timeUnit)
                index = int(current.ProcessName[-1])-1
                try:#handle the error thrown at the end of process
                    nextTaskInProcess = processStackList[index][0]
                    nextTaskInProcess.StartTime = timeUnit + current.IOtime
                    waitingList = addtoListSorted(waitingList, nextTaskInProcess)
                    processStackList[index].pop(0)
                except:
                    count = 0
                    for stack in processStackList:#when all the process are finished, wipe out the list
                        if len(stack) == 0:
                            count += 1
                            if count == len(traceDic):
                                processStackList.clear()
                current = None
                continue
        timeUnit += 1
        #acumulating waiting time for each process in WaitTimeDic
        if len(readyList)>0:
            for r in readyList:
                WaitTimeDic[r.ProcessName] += 1

def MLFQ(traceDic):
    StartTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
    EndTimeDic = {'P1':[0],'P2':[0],'P3':[0],'P4':[0],'P5':[0],'P6':[0],'P7':[0],'P8':[0]}
    WaitTimeDic = {'P1':0,'P2':0,'P3':0,'P4':0,'P5':0,'P6':0,'P7':0,'P8':0}
    timeUnit = CPUruntime = downTime = processIndex = tempStartTime = waitTime = 0
    processStackList= makeProcessStack(traceDic)
    Q1readyList = []
    Q2readyList = []
    Q3readyList = []
    readyListDisplay = []
    waitingList = []
    resultDic = {}
    #put all the first task to Q1readyList
    for PS in processStackList:
        PS[0].StartTime = tempStartTime
        tempStartTime += PS[0].ProcessTime
        Q1readyList.append(PS[0])
        PS.pop(0)
    current = None
    running = True

    while running:
        if len(waitingList) > 0:
            for w in waitingList:
                if w.StartTime > timeUnit:#Move process to its ready queue
                    break
                if w.StartTime <= timeUnit:
                    if w.QueLevel == 1:
                        Q1readyList.append(w)
                    elif w.QueLevel == 2:
                        Q2readyList.append(w)
                    else:
                        Q3readyList.append(w)
                waitingList.remove(w)
        if current:#cpu is occupied
            CPUruntime +=1
            current.TimeOnCPU += 1
            if current.QueLevel == 1:
                if current.TimeOnCPU == 5 and current.ProcessTime >5:#downgrade the process when 5 quantam are used and the process is not finished
                    print('*** DownGrading '+current.ProcessName + ' to Q2')
                    current.ProcessTime -= 5
                    current.QueLevel = 2
                    current.DownGraded = True
                    Q2readyList.append(current)
                    current = None
                    continue
            elif current.QueLevel == 2:
                #downgrade the process when 10 quantam are used and the process is not finished
                if (current.DownGraded and current.TimeOnCPU == 15) or (not current.DownGraded and current.TimeOnCPU ==10) and current.ProcessTime > 10:
                    current.ProcessTime -= 10
                    current.QueLevel = 3
                    current.DownGraded = True
                    Q3readyList.append(current)
                    current = None
                    continue

            if current.CPUburst == current.TimeOnCPU:#when the CPU burst is finished
                current.DownGraded = False
                index = int(current.ProcessName[-1]) -1
                try:#handle the error thrown at the end of the process
                    nextTask = processStackList[index][0]
                    nextTask.StartTime = timeUnit + current.IOtime
                    nextTask.QueLevel = current.QueLevel
                    waitingList = addtoListSorted(waitingList, nextTask)
                    processStackList[index].pop(0)
                except:
                    count = 0
                    for stack in processStackList:#wipe out the list when all the processes are finished
                        if len(stack) == 0:
                            count += 1
                            if count == len(traceDic):
                                processStackList.clear()
                EndTimeDic[current.ProcessName].append(timeUnit)#record the end time of the current process
                current = None
                continue

        else:#CPU is not occupied
            readyListDisplay = Q1readyList + Q2readyList + Q3readyList #join all the readyLists for display
            display(CPUruntime, timeUnit, current, waitingList, readyListDisplay)

            #Move process from readyLists to running state according to its priority
            if len(Q1readyList)>0:
                current = Q1readyList[0]
                current.StartTime = timeUnit
                StartTimeDic[current.ProcessName].append(timeUnit)
                Q1readyList.pop(0)
            elif len(Q2readyList)>0:
                current = Q2readyList[0]
                current.StartTime = timeUnit
                StartTimeDic[current.ProcessName].append(timeUnit)
                Q2readyList.pop(0)
            elif len(Q3readyList)>0:
                current = Q3readyList[0]
                current.StartTime = timeUnit
                StartTimeDic[current.ProcessName].append(timeUnit)
                Q3readyList.pop(0)
            else:
                if processStackList:
                    downTime += 1
                else:
                    running = False
                    resultDic = calcResult(timeUnit, downTime, CPUruntime, StartTimeDic, EndTimeDic, WaitTimeDic)
                    for key in resultDic:
                        print(key+': '+str(resultDic[key]))
                    continue
        #increament waiting time for all the processes in the readyLists
        if len(Q1readyList) > 0:
            for r in Q1readyList:
                WaitTimeDic[r.ProcessName] += 1
        if len(Q2readyList) > 0:
            for r in Q2readyList:
                WaitTimeDic[r.ProcessName] += 1

        if len(Q3readyList) > 0:
            for r in Q2readyList:
                WaitTimeDic[r.ProcessName] += 1

        timeUnit += 1


def main():
    traceDic = {'P1':[5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
                'P2':[4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
                'P3':[8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
                'P4':[3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
                'P5':[16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
                'P6':[11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
                'P7':[14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
                'P8':[4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]}

    #FCFS(traceDic)
    #SJF(traceDic)
    MLFQ(traceDic)
main()#run the simulation

#SJF
        #when waiting list is not empty and the first element in waiting list is up
            #move to readyList
            #pop the first element on the waitingList

        #when current is none
            #if there are more tasks on the stack
                #if the ready list is not empty
                    #current = first task on the readyList
                    #pop first element on the readyList
                    #change the startTime to timeUnit
                    #record time to StartTimeDic
                #else
                    #downTime ++
            #else(no more tasks on stack)
                #calc result and display

        #else(current is not none)
            #cpuruntime++
            #when timeUnit == task start time + task cpu
                #asssign start time to the next task on the stack
                #put next task of the current process on the waiting list
                #current is finished
                #record time to EndTimeDic

#MLFQ
    #while running
        #if waiting list is not empty
            #for each element in waiting list
                #if the start time of the element on waiting list <= timeUnit
                    #put them in to their readyList

        #if current
            #CPU runtime +=1
            #current.TimeOnCPU += 1

            #if current.QueLevel == 1
                #run over 5 time units (TimeOnCPU == 5 and ProcessTIme > 5)
                    #ProcessTime - = 5
                    #put to Q2readyList

            #else if current.QueLevel == 2
                #if run over 10 time units
                    #ProcessTime - = 10
                    #put to Q3readyList

            #if current.ProcessTime + current.StartTime == timeUnit
                #if next process on the stack exists
                    #set start time for the next process on the stack
                    #put next process on the stack to waiting list
                #else
                    #check if all processStasks in the list are empty
                    #if all empty
                        #clear processStackList

        #else
            #if Q1List is not empty
                #current = fist task on the Q1List
                #current.StartTime = timeUnit
                #pop first task on the Q1List
            #else if Q2List is not empty
                #current = fist task on the Q2List
                #current.StartTime = timeUnit
                #pop first task on the Q1List
            #else if Q3List is not empty
                #current = fist task on the Q3List
                #current.StartTime = timeUnit
                #pop first task on the Q1List
            #else
                #increament downTime
                #running = False
                #calculate result
                #display result
