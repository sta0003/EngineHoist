# created by: Ashton Stack
# description: This is a simple program that will create a Tkinter GUI that will allow the user to select engines from a list and then change the engine in the main.mr file.

# copyright: (c) 2022 Ashton Stack
# 

# Error codes:
# E001 Failed to find directory
# E002 Failed to load engines
# E003 Failed to open file
# E004 Failed to load main.mr
# E005 Failed to set engine
# E006 Failed to start simulator


//https://docs.python.org/3/library/tkinter.html
from tkinter import *
import glob
import os
from tkinter import messagebox
import webbrowser
import requests
import platform

try:
    import pyi_splash
except:
    pyi = False



# main variables

version = "1.2.0"

mainDir = os.getcwd()
osName = None
enginesLocation = "./assets/engines/**/*.mr"
mainLocation    = "./assets/main.mr"
configLocation  = "./selector.cfg"
appLocation     = None
configLoaded    = False
config          = None
darkMode        = False
unLoadedEngines = []
loadedEngines   = {}
windowHeight = 700
windowWidth = 700

# tk window setup
root = Tk()
root.title("Engine Selector")
root.geometry(str(700) + "x" + str(700))
root.resizable(False, False)
i = 0
while i < 4:
    root.columnconfigure(i,weight=1)
    i += 1
i=0
while i < 2:
    root.rowconfigure(i,weight=1)
    i += 1




def start():
    global appLocation
    try:
        pyi_splash.close()
    except:
        A=1    
    # search for gamefile.
    # osName = platform.system()
    # if osName == "Windows":
    mainWindow.createWindow()
    # for core in glob.glob("./**/engine-sim-app.exe", recursive=True): 
    #     appLocation = core
    appLocation = "engine-sim-app.exe"
    # else:
    #     mainWindow.createWindow()
    #     for core in glob.glob("./**/engine-sim-app", recursive=True):
    #         appLocation = core



    response = requests.get("https://api.github.com/repos/sta0003/EngineSimulatorSelector/releases")
    try:
        
        latestRelease = response.json()[0]["tag_name"]
        if latestRelease == "V" + version:
            root.title("Engine Selector V" + version)
        else:
            root.title("Engine Selector | V" + version + " | Update Available " + response.json()[0]["tag_name"])

    except:
        root.title("Engine Selector" + " | Update Check Failed")



class config():
    
    def export():
        config = open(configLocation,"w")
        config.write("darkMode : " + str(darkMode))
        config.close()
    
    def loadConfig():
        global darkMode
        if os.path.exists(configLocation):
        
            config = open(configLocation,"r").read()
            config = config.split("\n")
            for setting in config:
                setting = setting.split(" : ")
                if setting[0] == "darkMode":
                    global darkMode
                    if setting[1] == "True":
                        darkMode = True
                        mainWindow.darkMode(False)
                    else:
                        mainWindow.darkMode(True)
                        darkMode = False
        else:
            config = open(configLocation,"w")
            config.write("")
            config.close()



class tools():
    def resetMain():
        main = open(mainLocation, 'w')
        main.write("import \"engine_sim.mr\"\nimport \"themes/default.mr\"\nimport \"engines/audi/i5.mr\"\n\nuse_default_theme()\nset_engine(\n    audi_i5_2_2L()\n)")
        main.close()



# class for the engine selector
class engineClass():
    def findEngines():
        manufacturerList.delete(0,END)
        engineList.delete(0,END)
        
        for f in glob.glob(enginesLocation, recursive=True):
            unLoadedEngines.append(f.replace("\\","/"))
        x = 0
        for engine in unLoadedEngines:
            with open(engine) as f:
                i = 0
                engineName = ""
                engineFunction = ""
                engineBrand = unLoadedEngines[x].split("/")[3]
                lines = f.readlines()
                for line in lines:
                    if line != "\n":
                        if line.startswith("public node"):
                            if  "alias output __out: engine;" in lines[i+1]:
                                engineFunction = (line.split()[2])
                        if " name:" in line:
                            engineName = line.split("\"")[1]
                    i += 1
                f.close()
                if engineBrand.upper() not in manufacturerList.get(0,END):
                    manufacturerList.insert(END,(engineBrand.upper()))
                    
                engineName = engineName + " (" + str(engineFunction) + ")"  
                      
                loadedEngines[engineName] = engineFunction , engineBrand , unLoadedEngines[x]
            x += 1
            
            
    def setEngine(engine):
        try:
            with open(mainLocation, 'r') as f:
                i = 0
                lines = f.readlines()
                for line in lines:
                    if line != "\n":
                        if "engines" in line:
                            lines[i] = ("import \"" + loadedEngines[engine][2][9:] + "\"\n")
                        if line.startswith("set_engine"):
                            lines[i+2] = "    " + loadedEngines[engine][0] + "()\n"
                            open(mainLocation, 'w').writelines(lines)
                        i += 1
        except:
            messagebox.showerror("ERROR","Failed to set engine (E005)")

    
    def startSimulator():
        try:
            for engine in loadedEngines.keys():
                if len(engineList.curselection()) <1: break
                if engineList.get(engineList.curselection()) == engine:
                    engineClass.setEngine(engine)
                    break
        except:
            messagebox.showerror("ERROR","Failed to start simulator (E006)")
        
        root.withdraw()
        os.chdir(os.getcwd() + "/bin")
        os.system(appLocation)
        root.deiconify()
        os.chdir(mainDir)

# class for the GUI
class mainWindow():
    def createWindow():
        startBtn.grid(row=1, column=0, columnspan=3, sticky="nsew")
        closeBtn.grid(row=1, column=3, columnspan=1, sticky="nsew")
        manufacturerList.grid(row=0, column=0, columnspan=2 , sticky="nsew")
        engineList.grid(row=0, column=2, columnspan=2, sticky="nsew")
        startBtn.config(font=("Montserrat", 30))
        closeBtn.config(font=("Montserrat", 30))
        manufacturerList.config(font=("Montserrat", 15))
        engineList.config(font=("Montserrat", 15))
    def darkMode(mode):
        global darkMode
        if not mode:
            manufacturerList.config(bg="#2d2d2d", fg="#ffffff")
            engineList.config(bg="#2d2d2d", fg="#ffffff")
            startBtn.config(bg="#2d2d2d", fg="#ffffff")
            closeBtn.config(bg="#2d2d2d", fg="#ffffff")
            root.config(bg="#2d2d2d")
            darkMode = True
        else:
            manufacturerList.config(bg="#ffffff", fg="#000000")
            engineList.config(bg="#ffffff", fg="#000000")
            startBtn.config(bg="#ffffff", fg="#000000")
            closeBtn.config(bg="#ffffff", fg="#000000")
            root.config(bg="#ffffff")
            darkMode = False
        config.export()
    def toggelDarkmode():
        if darkMode:
            mainWindow.darkMode(True)
        else:
            mainWindow.darkMode(False)
        config.export()
        
        

def manufacturerSelected(event):
    engineList.delete(0,END)
    for engine in loadedEngines.keys():
        if loadedEngines[engine][1].upper() == manufacturerList.get(manufacturerList.curselection()):
            engineList.insert(END,engine)


# gui variables
startBtn = Button(root, text="START \nSIMULATOR", command=engineClass.startSimulator)
closeBtn = Button(root, text="CLOSE", command=root.destroy)

manufacturerList = Listbox(root, height=15, width=50, selectmode="SINGLE", exportselection=False)
engineList = Listbox(root, height=15, width=50, selectmode="SINGLE", exportselection=False)

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


toolmenu = Menu(mainmenu, tearoff = 0)
toolmenu.add_command(label = "Refresh Engines", command = engineClass.findEngines)
toolmenu.add_command(label = "Dark Mode", command = mainWindow.toggelDarkmode)
toolmenu.add_command(label = "Reset main.mr", command = tools.resetMain)
mainmenu.add_cascade(label = "Tools", menu = toolmenu)

# Help
helpmenu = Menu(mainmenu, tearoff = 0)
helpmenu.add_command(label = "Github", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector"))
helpmenu.add_command(label = "Update", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector/releases/latest"))
helpmenu.add_separator()
helpmenu.add_command(label = "Help", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector/blob/main/help.md"))
helpmenu.add_command(label = "README", command = lambda: webbrowser.open("https://github.com/sta0003/EngineSimulatorSelector/blob/main/README.md"))
mainmenu.add_cascade(label = "Documentation", menu = helpmenu)

root.config(menu = mainmenu)



    

# main loop
config.loadConfig()
engineClass.findEngines()
start()
root.mainloop()
