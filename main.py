from random import randint as rand
from tkinter import messagebox
from tkinter import *
import webbrowser
import platform
try: import pyi_splash 
except: pass
import requests
import glob
import re
import os


from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem
from kivy.core.window import Window


enginesFileLocation = os.getcwd() + "/assets/engines/**/*.mr"
mainLocation        = os.getcwd() +"/assets/main.mr"
configLocation      = "./hoist.cfg"
themesLocation      = "./assets/themes/*.mr"
appLocation         = "engine-sim-app.exe"
mainDir             = os.getcwd()
version             = "2.0.0-development"
engineLocations     = []
failedEngines       = []

lastClicked = None


# config
darkMode            = False
shareAnalytics      = None
promptToUpdate      = True
units               = "metric"
simTheme            = "default"





mainScreen = """
MDScreen:
    MDGridLayout:
        cols: 2
    
    MDScrollView:
        pos_hint: {"x": 0.05, "top": 1}
        bar_width: 0
        size_hint_y: 0.8
        size_hint_x: 0.4
        MDList:
            spacing: dp(10)
            padding: dp(10)
            id: leftContainer        
        
    MDScrollView:
        pos_hint: {"right": .95, "top": 1}
        bar_width: 0
        size_hint_y: 0.8
        size_hint_x: 0.4
        MDList:
            spacing: dp(10)
            padding: dp(10)
            id: rightContainer
            
    MDRectangleFlatButton:
        text: "Start Simulation"
        size_hint: 1, .2
        font_size: 30
        background_color: 0, 0, 1, 1
        on_release: app.startSimulation()        

"""

# Main App
class EngineHoistApp(MDApp):
    
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        
        self.root = Builder.load_string(mainScreen)  
        
    def on_start(self):
        print("Application Ready!")
        
        
        
        print("Looking for engines...")
        engineBrands = []
        for engine in engineLocations:
            print("Found engine: " + engine)
            if vehicleInfo.getEngineBrand(engine) not in engineBrands:
                print(engineBrands)
                engineBrands.append(vehicleInfo.getEngineBrand(engine))
                self.root.ids.leftContainer.add_widget(
                    TwoLineListItem(text=f"{vehicleInfo.getEngineBrand(engine).upper()}", secondary_text=engine, secondary_font_style="Caption",
                                    bg_color=("purple"), radius=30, on_release=lambda x: self.openEngine(x)))

        return super().on_start()
    
    
    def openEngine(self, instance):
        self.root.ids.rightContainer.clear_widgets()
        for engine in engineLocations:
            if vehicleInfo.getEngineBrand(engine).upper() == instance.text.upper():
                try: 
                    self.root.ids.rightContainer.add_widget(TwoLineListItem(text=f"{vehicleInfo.getEngineName(engine)}",
                                                            secondary_text=f"{vehicleInfo.getEngineFunctionName(engine)}", bg_color="purple", radius=30
                                                            , on_release=lambda x: self.selectEngine(x)))
                except: 
                    pass
                    self.root.ids.rightContainer.add_widget(TwoLineListItem(text=f"UNKNOWN ENGINE FORMAT",
                                                            secondary_text=f"{engine}", bg_color="grey", radius=30
                                                            , on_release=lambda x: self.selectEngine(x)))
                    # engineList.insert(END, ("(UNKNOWN FORMAT) ("+ vehicleInfo.getEngineFileName(engine) +")"))

    def selectEngine(self, instance):
        global lastClicked
        lastClicked = instance
        print(lastClicked.text)

    def startSimulation(self):
        simulator.start()

    def checkUpdates(self):
        response = requests.get("https://api.github.com/repos/sta0003/EngineHoist/releases")
        try:
            
            latestRelease = response.json()[0]["tag_name"]
            if latestRelease == "V" + version:
                self.title = "Engine Hoist Simulator"
                # root.title("Engine hoist V" + version)
                pass
            else:
                global promptToUpdate
                if "development" in version:
                    pass
                    # root.title("Engine hoist V" + version)
                # else:
                    # root.title("Engine hoist | V" + version + " | Update Available " + response.json()[0]["tag_name"])
                    # if promptToUpdate or rand(0,10) == 3:
                    #     # confirm = messagebox.askyesno("Update Available", "An update is available for Engine Hoist. Would you like to download it now?", icon="question")
                    #     if confirm:
                    #         webbrowser.open("https://github.com/sta0003/EngineHoist/releases/latest")
                    #     else:
                    #         # confirm = messagebox.askyesno("Would you like to be prompted to update in the future?", "Would you like to be prompted to update in the future?", icon="question")
                    #         if not confirm:
                    #             promptToUpdate = False
                    #             config.export()

        except:
            pass
            # root.title("Engine hoist" + " | Update Check Failed")


    def on_stop(self):
        print("Hulktastic!")
        return super().on_stop()



class vehicleInfo:
    def getMainFunction(file):
        with open(file, "r") as f:
            for line in f:
                if "public node main {" in line:
                    return True
        
    def getEngineName(file):
        with open(file, "r") as f:
            for line in f:
                if " name:" in line:
                    return line.split("\"")[1]

    def getEngineFunctionName(file):
        with open(file, "r") as f:
            for line in f:
                if re.match(r"^public node", line):
                    next_line = f.readline()
                    if re.match(r'^\s*alias output __out: engine;', next_line):
                        return line.split()[2]

    def getEngineBrand(file):
        return file.split("/")[-2]

    def getEngineFileName(file):
        return file.split("/")[-1]

    def getVehicleName(file):
        with open(file, "r") as f:
            for line in f:
                if re.match(r"^public node", line):
                    next_line = f.readline()
                    if re.match(r'^\s*alias output __out: vehicle;', next_line):
                        return line.split()[2]

    def getTransmissionName(file):
        with open(file, "r") as f:
            for line in f:
                if re.match(r"^public node", line):
                    next_line = f.readline()
                    if re.match(r'^\s*alias output __out: transmission;', next_line):
                        return line.split()[2]

class themeInfo:
    def getThemeName(file):
        file = "./assets/themes/{}.mr".format(file)
        with open(file, "r") as f:
            for line in f:
                if re.match(r"^\s*unit_names units()", line):
                    next_line = f.readline()
                    if re.match(r'^public node', next_line):
                        return next_line.split()[2]

# edit main file with selected engine
def createMainFile(engine, theme):
    themeFunctionName   = themeInfo.getThemeName(theme)
    engineFunctionName  = vehicleInfo.getEngineFunctionName(engine)
    vehicleName         = vehicleInfo.getVehicleName(engine)
    transmissionName    = vehicleInfo.getTransmissionName(engine)
    newEngineName       = vehicleInfo.getMainFunction(engine)
    def writeFile(f):
        f.write("// This file was generated by Engine Hoist V" + version + "\n")
        f.write("// remove these comments to prevent this file from being overwritten\n")
        f.write('import "engine_sim.mr"\n')
        f.write('import "themes/{}.mr"\n'.format(theme))
        f.write('import "{}"\n\n'.format(engine.replace("./assets/","",1)))
        f.write('unit_names units()\n')
        if units == "metric":
            f.write('{}(speed_units: units.kph,pressure_units: units.bar,torque_units: units.Nm,power_units: units.kW)\n'.format(themeFunctionName))
        else:
            f.write('{}(speed_units: units.mph, pressure_units: units.inHg, torque_units: units.lb_ft, power_units: units.hp)\n'.format(themeFunctionName))
        if newEngineName:
            f.write('main()\n')
        else:
            f.write('set_engine({}())\n'.format(engineFunctionName))
            if vehicleName:
                f.write('set_vehicle({}())\n'.format(vehicleName))
            if transmissionName:
                f.write('set_transmission({}())\n'.format(transmissionName))
    
    with open((mainLocation), 'r') as f:
        if f.readline().startswith("// This file was generated by Engine Hoist"):
            f.close()
            with open((mainLocation), 'w') as f:
                writeFile(f)
        else:
            with open((mainDir +"/assets/main.mr.OLD"), 'w') as f2:
                backup = f.read()
                f2.write(backup)
            with open((mainLocation), 'w') as f:
                writeFile(f)


class config:

    def export():
        config = open(configLocation,"w")
        config.write("darkMode : " + str(darkMode))
        config.write("\nshareAnalytics : " + str(shareAnalytics))
        config.write("\npromptToUpdate : " + str(promptToUpdate))
        config.write("\nunits : " + str(units))
        config.write("\ntheme : " + str(simTheme))
        config.close()
    
    def load():
        global darkMode, shareAnalytics, promptToUpdate, units, simTheme
        if os.path.exists(configLocation):
            configFile = open(configLocation,"r").read()
            # confirm user has accepted to share analytics
            if "shareAnalytics" not in configFile:
                confirm = messagebox.askyesno("Share Usage Analytics", "Would you like to share anonymous usage analytics? This will help improve the program and make it more useful for you. You can change this setting at any time in the config file.", icon="question")
                if confirm:
                    shareAnalytics = True
                else:
                    shareAnalytics = False

            # load settings perline
            configFile = configFile.split("\n")
            try:
                if configFile[0].split(" : ")[0] == "darkMode":
                    global darkMode
                    if configFile[0].split(" : ")[1] == "True":
                        # tkinterApp.darkmodeActivate()
                        pass

                if configFile[1].split(" : ")[0] == "shareAnalytics":
                    if configFile[1].split(" : ")[1] == "True":
                        shareAnalytics = True
                        # analyticsCheck.select()
                    elif configFile[1].split(" : ")[1] == "False":
                        shareAnalytics = False
                    else:
                        confirm = messagebox.askquestion("Share Usage Analytics", "Would you like to share anonymous usage analytics? This will help improve the program and make it more useful for you. You can change this setting at any time in the config file.", icon="question")
                        if confirm == "yes":
                            shareAnalytics = True
                            # analyticsCheck.select()
                        else:
                            shareAnalytics = False

                if configFile[2].split(" : ")[0] == "promptToUpdate":
                    if configFile[2].split(" : ")[1] == "True":
                        promptToUpdate = True
                        # updateCheck.select()
                    elif configFile[2].split(" : ")[1] == "False":
                        promptToUpdate = False

                if configFile[3].split(" : ")[0] == "units":
                    if configFile[3].split(" : ")[1] == "metric":
                        units = "metric"
                        # metricCheck.select()
                    elif configFile[3].split(" : ")[1] == "imperial":
                        units = "imperial"
            except:
                pass

            config.export()

        else:
            configFile = open(configLocation,"w")
            configFile.write("")
            configFile.close()

class simulator:
    def start():
        global lastClicked
        
        
        for engine in engineLocations:
            if lastClicked == None: break
            if "UNKNOWN" in lastClicked.text:
                # messagebox.showerror("Error", "This engine is not supported by this version of Engine Hoist. \n Unknow engine format.")
                return
            else:
                if engine in failedEngines:
                    continue
                elif lastClicked.text == vehicleInfo.getEngineName(engine):
                    # try:
                    #     # theme = themeList.get(themeList.curselection())
                    # except:
                    theme = "Default"
                    createMainFile(engine, theme)
                    break
        Window.hide()
        if platform.system() == "Linux":
            os.chdir(os.getcwd() + "/build")
            os.system(os.getcwd() + "/engine-sim-app")
        else:
            os.chdir(os.getcwd() + "/bin")
            os.system(appLocation)
        
        os.chdir(mainDir)
        Window.show()
        # except Exception as e:
        #     print(e)
        #     messagebox.showerror("ERROR","Failed to start simulator\n(Error: {})".format(e))
    # def validate():
    #     if len(engineList.curselection()) <1:
    #         messagebox.showerror("ERROR","No engine selected")
    #     else:
    #         simulator.start()

def main():
    global engineLocations
    config.load()
    for location in glob.glob(enginesFileLocation, recursive=True):
        engineLocations.append(location.replace("\\","/"))
    
    for engine in engineLocations:
        if vehicleInfo.getEngineName(engine):
            continue
        else:
            failedEngines.append(engine)
        

if __name__ == "__main__":

    main()
    EngineHoistApp().run()