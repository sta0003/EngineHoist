# created by: Ashton Stack
# description: This is a simple program that will create a Tkinter GUI that will allow the user to select engines from a list and then change the engine in the main.mr file.

# copyright: (c) 2022 Ashton Stack
# 


from tkinter import *
import glob
import os
import webbrowser
import requests




# main variables

version = "1.0.1"

mainDir = os.getcwd()
enginesLocation = "./assets/engines/**/*.mr"
mainLocation    = "./assets/main.mr"
unLoadedEngines = []
loadedEngines = {}


# tk window setup
root = Tk()
root.title("Engine Selector")
root.geometry('500x600')

root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)





# class for the engine selector
class engineClass():
    def findEngines():
        for f in glob.glob(enginesLocation, recursive=True):
            unLoadedEngines.append(f)

# loading engines
        x = 0
        for engine in unLoadedEngines:
            with open(engine) as f:
                i = 0
                engineName = ""
                engineFunction = ""
                engineBrand = unLoadedEngines[x].split("\\")[1]
                lines = f.readlines()
                for line in lines:
                    if line is not "\n":
                        if line.startswith("public node"):
                            if  "alias output __out: engine;" in lines[i+1]:
                                engineFunction = (line.split()[2])
                        if "name:" in line:
                            engineName = line.split("\"")[1]
                    i += 1
                f.close()
                if engineBrand.upper() not in manufacturerList.get(0,END):
                    manufacturerList.insert(END,(engineBrand.upper()))
                loadedEngines[engineName] = engineFunction , engineBrand , unLoadedEngines[x]
            x += 1
            
            
    def setEngine(engine):
        with open(mainLocation, 'r') as f:
            i = 0
            lines = f.readlines()
            for line in lines:
                if line is not "\n":
                    if "engines" in line:
                        lines[i] = ("import \"" + loadedEngines[engine][2][9:] + "\"\n")
                    if line.startswith("set_engine"):
                        lines[i+2] = "    " + loadedEngines[engine][0] + "()\n"
                        open(mainLocation, 'w').writelines(lines)
                    i += 1

    
    def startSimulator():
        for engine in loadedEngines.keys():
            if engineList.get(engineList.curselection()) == engine:
                engineClass.setEngine(engine)
                break
        
        root.withdraw()
        os.chdir(os.getcwd() + "\\bin")
        os.system(os.getcwd() + "\\engine-sim-app.exe")
        root.deiconify()
        os.chdir(mainDir)

# class for the GUI
class mainWindow():
    def createWindow():
        btn.grid(row=2, column=0, columnspan=2, sticky="nsew")
        manufacturerList.grid(row=1, column=0, sticky="nsew")
        engineList.grid(row=1, column=1, sticky="nsew")

def manufacturerSelected(event):
    engineList.delete(0,END)
    for engine in loadedEngines.keys():
        if loadedEngines[engine][1].upper() == manufacturerList.get(manufacturerList.curselection()):
            engineList.insert(END,engine)


# gui variables
btn = Button(root, text="Start Simulator", command=engineClass.startSimulator)

manufacturerList = Listbox(root, height=20, width=50, selectmode="SINGLE", exportselection=False)
engineList = Listbox(root, height=20, width=50, selectmode="SINGLE", exportselection=False)

manufacturerList.bind('<<ListboxSelect>>', manufacturerSelected)



# menu bar

mainmenu = Menu(root)
# File
filemenu = Menu(mainmenu, tearoff = 0)
# filemenu.add_command(label = "Open")
# filemenu.add_command(label = "Save")
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = root.destroy)
mainmenu.add_cascade(label="File", menu=filemenu)
 
# Help
helpmenu = Menu(mainmenu, tearoff = 0)
helpmenu.add_command(label = "Github", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector"))
helpmenu.add_command(label = "Update", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector/releases/latest"))
mainmenu.add_cascade(label = "Documentation", menu = helpmenu)
 
root.config(menu = mainmenu)




response = requests.get("https://api.github.com/repos/sta0003/EngineSimulatorSelector/releases")
latestRelease = response.json()[0]["tag_name"]
if latestRelease == "V" + version:
    root.title("Engine Selector V" + version)
else:
    root.title("Engine Selector | V" + version + " | Update Available " + response.json()[0]["tag_name"])
    

# main loop
engineClass.findEngines()
mainWindow.createWindow()
root.mainloop()