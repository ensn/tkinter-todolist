import tkinter, os, copy
global data, boxes, history, histindex

def readdata():
    data=[]
    for i in range(0, 6):
        try:
            listfile=open(str(i)+".txt")
            data.append([line.rstrip() for line in listfile.readlines()])
        except:
            pass
    return data

def buildgui():
    global data, boxes
    for list in data:
        boxes.append(tkinter.Listbox(win))
    for i in range(len(boxes)):
        for j in range(len(data[i])):
            boxes[i].insert(j, str(j+1)+": "+data[i][j])
        boxes[i].grid(row = 0, column = i, sticky = "nwse", rowspan = 1, columnspan = 1, padx = 0, pady = 0, ipadx = 0, ipady = 0)
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(1, minsize=50)
    for i in range(len(boxes)):
        win.grid_columnconfigure(i, weight=1)
    entry.grid(row = 1, column = 0, sticky = "snwe", rowspan = 1, columnspan = len(boxes), padx = 0, pady = 0, ipadx = 0, ipady = 0)
    entry.focus()
    

def updatebox(index):
    global data, boxes
    boxes[index].delete(0, last=len(data[index]))
    for i in range(len(data[index])):
        boxes[index].insert(i, str(i+1)+": "+data[index][i])


def saveandexit(event):
    for i in range(len(data)):
        filew=open(str(i)+".txt", "w")
        for line in data[i]:
            filew.write(line+"\n")
        filew.close()
    win.destroy()

def undo(event):
    global data, history, histindex, boxes
    if histindex>0:
        for i in range(len(boxes)):
            win.grid_columnconfigure(i, weight=0)
        histindex-=1
        data=copy.deepcopy(history[histindex])
        deleteboxes()
        buildgui()

def redo(event):
    global data, history, histindex, boxes
    if histindex<len(history)-1:
        for i in range(len(boxes)):
            win.grid_columnconfigure(i, weight=0)
        histindex+=1
        data=copy.deepcopy(history[histindex])
        deleteboxes()
        buildgui()
    
    
def deleteboxes():
    global boxes
    for box in boxes:
        box.destroy()
    boxes=[]

def processinput(event):
    #dont try to understand this code, it just works but idk how
    global data, boxes, history, histindex
    if len(data)==1:
        command=entry.get().split(" ", 1)
    else:
        command=entry.get().split(" ", 2)
    entry.delete(0, "end")
    try:
        if command!=[]:
            if command[0]=="n":
                try:
                    i=int(command[1])
                except:
                    i=len(data)
                addlist(i)
            elif command[0]=="r":
                if len(data)==1:
                    0/0
                else:
                    i=int(command[1])
                    deletelist(i)
            else:
                if len(data)==1:
                    listindex=0
                else:
                    listindex=int(command[0])
                    command.pop(0)
                try:
                        editindex=int(command[0])
                        if len(command)==1:
                            data[listindex].pop(editindex-1)
                        elif command[1][0]=="+":
                            data[listindex][editindex-1]+=str(command[1][1:])
                        else:
                            data[listindex][editindex-1]=command[1]
                except:
                    if len(command)==1:
                        data[listindex].append(command[0])
                    else:
                        data[listindex].append(command[0]+" "+command[1])
                updatebox(listindex) 
        histindex+=1
        history.insert(histindex, copy.deepcopy(data))   
    except:
        pass
            
def addlist(i):
    global data
    for j in range(len(data)-1, i-1, -1):
        os.rename(str(j)+".txt", str(j+1)+".txt")
    file=open(str(i)+".txt", "w")
    file.close()
    data.insert(i, [])
    deleteboxes()
    buildgui()

def deletelist(i):
    global data, boxes
    data.pop(i)
    os.remove(str(i)+".txt")
    for j in range(i+1, len(data)+1):
        os.rename(str(j)+".txt", str(j-1)+".txt")
    win.grid_columnconfigure(len(data), weight=0)
    deleteboxes()
    buildgui()



data=readdata()

win=tkinter.Tk()
win.state("zoomed")
win.title("List")
win.bind("<Control-w>", saveandexit)
win.bind("<Control-z>", undo)
win.bind("<Control-y>", redo)
win.bind("<Return>", processinput)
win.protocol("WM_DELETE_WINDOW", lambda: saveandexit(1))

entry=tkinter.Entry(win)

boxes=[]
buildgui()

history=[copy.deepcopy(data)]
histindex=0

win.mainloop()
