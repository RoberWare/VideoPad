#!/usr/bin/env python
# -*- coding: utf-8 -*-

#KIVY IMPORTS
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.video import Video

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from  kivy.uix.widget import Widget

from kivy.properties import ListProperty, OptionProperty, BooleanProperty, DictProperty, ObjectProperty, StringProperty, NumericProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.utils import platform

from kivy.clock import Clock
from functools import partial

#NXT IMPORTS
import nxt.locator
from nxt.motor import *
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4

#SYSTEM IMPORTS
import os,sys,json,shutil

if platform == 'android':
    from plyer import email

ID = '00:16:53:00:F5:A9'


class VideoPadUI(Screen):
    pass

class ControlPadsUI(Screen):
    pass
        
class PadSettingsUI(Popup):
    pass

class PortSettingsUI(Popup):
    pass

class MappingUI(Popup):
    mappingkey=StringProperty()

class KeyMappingUI(Popup):
    powerra=NumericProperty()
    powerta=NumericProperty()
    tachoa=NumericProperty()
    powerrb=NumericProperty()
    powertb=NumericProperty()
    tachob=NumericProperty()
    powerrc=NumericProperty()
    powertc=NumericProperty()
    tachoc=NumericProperty()

class VideoIPUI(Popup):
    pass

class SidePanel(BoxLayout):
    pass

class MainPanel(BoxLayout):
    pass

class MetaPanel(BoxLayout):
    pass

class DualClassicControl(Widget):
    power_x=NumericProperty()
    power_y=NumericProperty()
    pass

class ClassicControl(Widget):
    power_x=NumericProperty()
    power_y=NumericProperty()
    pass

class TankControl(Widget):
    s1=NumericProperty()
    s2=NumericProperty()
    pass

class MyButton(Button):
    myimg=StringProperty()
    mylbl=StringProperty()
    pass

class PopMsg(Popup):
    msg=StringProperty()
    title=StringProperty()
    size_hint=ListProperty()
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down,on_key_up=self._on_keyboard_up)
        
        self.pressedkeys = []
        self.power={}        
        
    def build(self):
        # WINDOW SETTINGS
        self.title = "PadUI"
        self.window_icon = "imgs/logo.png"
        self.icon = "imgs/logo.png"
        
        # SCREENS
        self.myMetaPanel = MetaPanel()
        self.mySidePanel = SidePanel()
        root = self.myMetaPanel
        self.myMainPanel = self.myMetaPanel.ids.MainPanel
        
        self.myVideoPadUI = self.myMainPanel.ids.myVideoPadUI
        self.myControlPadsUI = self.myMainPanel.ids.myControlPadsUI
        self.myPadSettingsUI = PadSettingsUI()
        self.myPortSettingsUI = PortSettingsUI()
        self.myMappingUI = MappingUI()
        self.myKeyMappingUI = KeyMappingUI()
        self.myVideoIPUI =VideoIPUI()
        
        self.myClassicControlWidget = ClassicControl(power_x=0,power_y=0)
        self.myDualClassicControlWidget = DualClassicControl(power_x=0,power_y=0)
        self.myTankControlWidget = TankControl(s1=0,s2=0)

        self.myPopMsg = PopMsg()
        
        return root

    def on_start(self):
        self.play=False
        
        self.myVideoPadUI.ids.video.play=False
        
        self.resetmapping()
        
        self.ports = {}        

        self.newkey = ""   
        self.keyboardlistening=False
        
        self.showpads()
        
        self.findbrick()
    
    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.bind(on_key_down=self._on_keyboard_down,on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not keycode[1] in self.pressedkeys: self.pressedkeys.append(keycode[1])        
        print self.pressedkeys
        #print keycode[1]
        if self.keyboardlistening == True:
            self.newkey == keycode[1]
            print ">>>",self.newkey,self.keyboardlistening
        """
        elif self.controlmode == "tank":
            forwardA = self.myTankControlWidget.s1
            forwardB = self.myTankControlWidget.s2
            if 'w' in self.pressedkeys:
                if forwardB > -100:
                    self.myTankControlWidget.s2 -= 100
            if 's' in self.pressedkeys:            
                if forwardB < +100:
                    self.myTankControlWidget.s2 += 100
            if 'up' in self.pressedkeys:
                if forwardA > -100:
                    self.myTankControlWidgewt.s1 -= 100
            if 'down' in self.pressedkeys:w
                if forwardA < +100:
                    selfsssssssssssssssssssw.myTankControlWidget.s1 += 100
        """
        if self.play == True:
            print self.power
            if self.mapping['w'] in self.pressedkeys:
                if self.cmd["w"]["A"]["Run"]==1:
                    if self.power["A"]+self.cmd["w"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100: self.power["A"]+=self.cmd["w"]["A"]["Power"]
                elif self.cmd["w"]["A"]["Turn"]==1:
                    if self.power["A"]+self.cmd["w"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100:self.power["A"]+=self.cmd["w"]["A"]["Power"]
                if self.cmd["w"]["B"]["Run"]==1:
                    if self.power["B"]+self.cmd["w"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["w"]["B"]["Power"]
                elif self.cmd["w"]["B"]["Turn"]==1:
                    if self.power["B"]+self.cmd["w"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["w"]["B"]["Power"]
                if self.cmd["w"]["C"]["Run"]==1:
                    if self.power["C"]+self.cmd["w"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["w"]["C"]["Power"]
                elif self.cmd["w"]["C"]["Turn"]==1:
                    if self.power["C"]+self.cmd["w"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["w"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["w"]["C"]["Power"]
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.w.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.w.state="down"
                else:self.myTankControlWidget.s1 += 100
                print "OK"
            if self.mapping['s'] in self.pressedkeys:            
                if self.cmd["s"]["A"]["Run"]==1:
                    if self.power["A"]+self.cmd["s"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["A"]+=self.cmd["s"]["A"]["Power"]
                elif self.cmd["s"]["A"]["Turn"]==1:
                    if self.power["A"]+self.cmd["s"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["A"]+=self.cmd["s"]["A"]["Power"]
                if self.cmd["s"]["B"]["Run"]==1:
                    if self.power["B"]+self.cmd["s"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["s"]["C"]["Power"]
                elif self.cmd["s"]["B"]["Turn"]==1:
                    if self.power["B"]+self.cmd["s"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["s"]["C"]["Power"]
                if self.cmd["s"]["C"]["Run"]==1:
                    if self.power["C"]+self.cmd["s"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["s"]["C"]["Power"]
                elif self.cmd["s"]["C"]["Turn"]==1:
                    if self.power["C"]+self.cmd["s"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["s"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["s"]["C"]["Power"]
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.s.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.s.state="down"
                else:self.myTankControlWidget.s1 -= 100
                print "OK"
            if self.mapping['a'] in self.pressedkeys:            
                if self.cmd["a"]["A"]["Run"]==1:
                    Motor(self.b, PORT_A).run(self.cmd["a"]["A"]["Power"])
                elif self.cmd["a"]["A"]["Turn"]==1:
                    Motor(self.b, PORT_A).turn(self.cmd["a"]["A"]["Power"],self.cmd["a"]["A"]["Tacho"])                   
                if self.cmd["a"]["B"]["Run"]==1:
                    Motor(self.b, PORT_B).run(self.cmd["a"]["B"]["Power"])
                elif self.cmd["a"]["B"]["Turn"]==1:
                    Motor(self.b, PORT_B).turn(self.cmd["a"]["B"]["Power"],self.cmd["a"]["B"]["Tacho"])
                if self.cmd["a"]["C"]["Run"]==1:
                    Motor(self.b, PORT_C).run(self.cmd["a"]["C"]["Power"])
                elif self.cmd["a"]["C"]["Turn"]==1:
                    Motor(self.b, PORT_C).turn(self.cmd["a"]["C"]["Power"],self.cmd["a"]["C"]["Tacho"])   
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.a.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.a.state="down"                
                print "OK"
            if self.mapping['d'] in self.pressedkeys:            
                if self.cmd["d"]["A"]["Run"]==1:
                    Motor(self.b, PORT_A).run(self.cmd["d"]["A"]["Power"])
                elif self.cmd["d"]["A"]["Turn"]==1:
                    Motor(self.b, PORT_A).turn(self.cmd["d"]["A"]["Power"],self.cmd["d"]["A"]["Tacho"])                   
                if self.cmd["d"]["B"]["Run"]==1:
                    Motor(self.b, PORT_B).run(self.cmd["d"]["B"]["Power"])
                elif self.cmd["d"]["B"]["Turn"]==1:
                    Motor(self.b, PORT_B).turn(self.cmd["d"]["B"]["Power"],self.cmd["d"]["B"]["Tacho"])
                if self.cmd["d"]["C"]["Run"]==1:
                    Motor(self.b, PORT_C).run(self.cmd["d"]["C"]["Power"])
                elif self.cmd["d"]["C"]["Turn"]==1:
                    Motor(self.b, PORT_C).turn(self.cmd["d"]["C"]["Power"],self.cmd["d"]["C"]["Tacho"])   
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.d.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.d.state="down"
                print "OK"

            if self.mapping['up'] in self.pressedkeys:
                if self.cmd["up"]["A"]["Run"]==1:
                    if self.power["A"]+self.cmd["up"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100: self.power["A"]+=self.cmd["up"]["A"]["Power"]
                elif self.cmd["up"]["A"]["Turn"]==1:
                    if self.power["A"]+self.cmd["up"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100:self.power["A"]+=self.cmd["up"]["A"]["Power"]
                if self.cmd["up"]["B"]["Run"]==1:
                    if self.power["B"]+self.cmd["up"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["up"]["B"]["Power"]
                elif self.cmd["up"]["B"]["Turn"]==1:
                    if self.power["B"]+self.cmd["up"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["up"]["B"]["Power"]
                if self.cmd["up"]["C"]["Run"]==1:
                    if self.power["C"]+self.cmd["up"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["up"]["C"]["Power"]
                elif self.cmd["up"]["C"]["Turn"]==1:
                    if self.power["C"]+self.cmd["up"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["up"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["up"]["C"]["Power"]
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.w.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.w.state="down"
                else:self.myTankControlWidget.s2 += 100
                print "OK"
            if self.mapping['down'] in self.pressedkeys:
                if self.cmd["down"]["A"]["Run"]==1:
                    if self.power["A"]+self.cmd["down"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100: self.power["A"]+=self.cmd["down"]["A"]["Power"]
                elif self.cmd["down"]["A"]["Turn"]==1:
                    if self.power["A"]+self.cmd["down"]["A"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100:self.power["A"]+=self.cmd["down"]["A"]["Power"]
                if self.cmd["down"]["B"]["Run"]==1:
                    if self.power["B"]+self.cmd["down"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["down"]["B"]["Power"]
                elif self.cmd["down"]["B"]["Turn"]==1:
                    if self.power["B"]+self.cmd["down"]["B"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100:self.power["B"]+=self.cmd["down"]["B"]["Power"]
                if self.cmd["down"]["C"]["Run"]==1:
                    if self.power["C"]+self.cmd["down"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["down"]["C"]["Power"]
                elif self.cmd["down"]["C"]["Turn"]==1:
                    if self.power["C"]+self.cmd["down"]["C"]["Power"] <= 100 and self.power["A"]+self.cmd["down"]["A"]["Power"] >=-100:self.power["C"]+=self.cmd["down"]["C"]["Power"]
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.w.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.w.state="down"
                else:self.myTankControlWidget.s2 -= 100
                print "OK"
            if self.mapping['left'] in self.pressedkeys:            
                if self.cmd["left"]["A"]["Run"]==1:
                    Motor(self.b, PORT_A).run(self.cmd["left"]["A"]["Power"])
                elif self.cmd["left"]["A"]["Turn"]==1:
                    Motor(self.b, PORT_A).turn(self.cmd["left"]["A"]["Power"],self.cmd["left"]["A"]["Tacho"])                   
                if self.cmd["left"]["B"]["Run"]==1:
                    Motor(self.b, PORT_B).run(self.cmd["left"]["B"]["Power"])
                elif self.cmd["left"]["B"]["Turn"]==1:
                    Motor(self.b, PORT_B).turn(self.cmd["left"]["B"]["Power"],self.cmd["left"]["B"]["Tacho"])
                if self.cmd["left"]["C"]["Run"]==1:
                    Motor(self.b, PORT_C).run(self.cmd["left"]["C"]["Power"])
                elif self.cmd["left"]["C"]["Turn"]==1:
                    Motor(self.b, PORT_C).turn(self.cmd["a"]["C"]["Power"],self.cmd["left"]["C"]["Tacho"])   
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.left.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.left.state="down"                
                print "OK"
            if self.mapping['right'] in self.pressedkeys:            
                if self.cmd["right"]["A"]["Run"]==1:
                    Motor(self.b, PORT_A).run(self.cmd["right"]["A"]["Power"])
                elif self.cmd["right"]["A"]["Turn"]==1:
                    Motor(self.b, PORT_A).turn(self.cmd["right"]["A"]["Power"],self.cmd["right"]["A"]["Tacho"])                   
                if self.cmd["right"]["B"]["Run"]==1:
                    Motor(self.b, PORT_B).run(self.cmd["right"]["B"]["Power"])
                elif self.cmd["right"]["B"]["Turn"]==1:
                    Motor(self.b, PORT_B).turn(self.cmd["right"]["B"]["Power"],self.cmd["right"]["B"]["Tacho"])
                if self.cmd["right"]["C"]["Run"]==1:
                    Motor(self.b, PORT_C).run(self.cmd["right"]["C"]["Power"])
                elif self.cmd["right"]["C"]["Turn"]==1:
                    Motor(self.b, PORT_C).turn(self.cmd["right"]["C"]["Power"],self.cmd["right"]["C"]["Tacho"])   
                if self.pad["controlmode"] == "dualclassic":self.myDualClassicControlWidget.ids.right.state="down"
                elif self.pad["controlmode"] == "classic":self.myClassicControlWidget.ids.right.state="down"                    
                print "OK"
            print self.power
        else:print ">>>>>>mistake"
        if keycode[1] == "escape":
            self.myVideoPadUI.ids.forwardA.value = 0
            self.myVideoPadUI.ids.forwardB.value = 0
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        released_key = keycode[1]
        print released_key
        if self.keyboardlistening == True:
            self.keyboardlistening=False
            self.myKeyMappingUI.ids.key.text = released_key
            self.newkey = ""
            self.listeningthread.cancel()

        else:
            print "Released",released_key
            print self.power
            if released_key == self.mapping['w']:
                if self.pad["controlmode"] == "tank":self.myTankControlWidget.s1=0
                if self.cmd["w"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["w"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["w"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.w.state="normal"
            if released_key == self.mapping['s']:
                if self.pad["controlmode"] == "tank":self.myTankControlWidget.s1=0
                if self.cmd["s"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["s"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["s"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.s.state="normal"
            if released_key == self.mapping['a']:
                if self.cmd["a"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["a"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["a"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.a.state="normal"
            if released_key == self.mapping['d']:
                if self.cmd["d"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["d"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["d"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.d.state="normal"
            if released_key == self.mapping['up']:
                if self.pad["controlmode"] == "tank":self.myTankControlWidget.s2=0
                if self.cmd["up"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["up"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["up"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.w.state="normal"
            if released_key == self.mapping['down']:
                if self.pad["controlmode"] == "tank":self.myTankControlWidget.s2=0
                if self.cmd["down"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["down"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["down"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.w.state="normal"
            if released_key == self.mapping['left']:
                if self.cmd["left"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["left"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["left"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.a.state="normal"
            if released_key == self.mapping['right']:
                if self.cmd["right"]["A"]["Power"] != 0: self.power["A"]=0
                if self.cmd["right"]["B"]["Power"] != 0: self.power["B"]=0
                if self.cmd["right"]["C"]["Power"] != 0: self.power["C"]=0
                self.myClassicControlWidget.ids.d.state="normal"  
        print self.power
        self.pressedkeys.remove(released_key)
        return True


    def show_side_panel(self):
        self.myMetaPanel.ids.NavDraw.toggle_state()

    def vpui(self):
        self.myMainPanel.ids.ScrMan.current = self.myVideoPadUI.name        

    def controlpads(self):
        self.myMainPanel.ids.ScrMan.current = self.myControlPadsUI.name
        try:self.listeningthread.cancel()
        except: print "NO"
        self.play=False
    
    def cartype(self):
        pass

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def addnewkey(self):
        oldkey=self.newkey
        self.keyboardlistening=True
        self.listeningthread=Clock.schedule_interval(partial(self.listenkey,oldkey), 1 / 30.)
        return
        
    def listenkey(self,oldkey,dt):
        print "listening"
        if oldkey != self.newkey:
            #print oldkey,self.newkey
            self.keyboardlistening=False
            self.listeningthread.cancel()
            return False

    def preparemappingUI(self):
        pass

    def resetmapping(self):
        self.mapping={}        
        
        self.mapkeys={"w","s","a","d","up","down","left","right"}
        self.mapping={}
        for x in self.mapkeys:
            self.mapping[x]=x
        self.cmdkey = "" 
        
        self.cmd = {}
        
        for x in self.cmd:
            del self.cmd[x]
        
        for x in self.mapkeys:
            self.cmd[x]={}
            self.cmd[x]["A"]={}
            self.cmd[x]["A"]["Run"]=0
            self.cmd[x]["A"]["Turn"]=0
            self.cmd[x]["A"]["Power"]=0
            self.cmd[x]["A"]["Tacho"]=0
            self.cmd[x]["B"]={}
            self.cmd[x]["B"]["Run"]=0
            self.cmd[x]["B"]["Turn"]=0
            self.cmd[x]["B"]["Power"]=0
            self.cmd[x]["B"]["Tacho"]=0
            self.cmd[x]["C"]={}
            self.cmd[x]["C"]["Run"]=0
            self.cmd[x]["C"]["Turn"]=0
            self.cmd[x]["C"]["Power"]=0
            self.cmd[x]["C"]["Tacho"]=0
            
            print self.cmd
            
    def resetsettings(self):
        self.resetmapping()
    
        self.myPadSettingsUI.ids.padname.text=""

        self.myPortSettingsUI.ids.porta.text="None"
        self.myPortSettingsUI.ids.portb.text="None"
        self.myPortSettingsUI.ids.portc.text="None"
        self.myPortSettingsUI.ids.port1.text="None"
        self.myPortSettingsUI.ids.port2.text="None"
        self.myPortSettingsUI.ids.port3.text="None"
        self.myPortSettingsUI.ids.port4.text="None"

        self.myKeyMappingUI.ids.ta.active = False
        self.myKeyMappingUI.ids.powerta.value = 0
        self.myKeyMappingUI.ids.tachoa.value = 0                   

        self.myKeyMappingUI.ids.ra.active = False
        self.myKeyMappingUI.ids.powerra.value = 0           
        

        self.myKeyMappingUI.ids.tb.active = False
        self.myKeyMappingUI.ids.powertb.value = 0
        self.myKeyMappingUI.ids.tachob.value = 0            
        
        
        self.myKeyMappingUI.ids.rb.active = False
        self.myKeyMappingUI.ids.powerrb.value = 0          

        self.myKeyMappingUI.ids.tc.active = False
        self.myKeyMappingUI.ids.powertc.value = 0
        self.myKeyMappingUI.ids.tachoc.value = 0
        

        self.myKeyMappingUI.ids.rc.active = False
        self.myKeyMappingUI.ids.powerrc.value = 0

        for x in self.mapkeys:
            code="self.myMappingUI.ids.%s.text = '%s'"%(x, x)
            print code
            exec(code)
            
        self.pad = {}
        self.pad["controlmode"] = ""


    def setmappingkey(self,key):
        self.myKeyMappingUI.ids.key.text=self.mapping[key]
        self.cmdkey = key
        
        if self.cmd[self.cmdkey]["A"]["Run"] == 1:
            self.myKeyMappingUI.ids.ra.active = True
            self.myKeyMappingUI.ids.powerra.value = self.cmd[self.cmdkey]["A"]["Power"]
            
            self.myKeyMappingUI.ids.ta.active = False
            self.myKeyMappingUI.ids.powerta.value = 0
            self.myKeyMappingUI.ids.tachoa.value = 0                   
        elif self.cmd[self.cmdkey]["A"]["Turn"] == 1:
            self.myKeyMappingUI.ids.ta.active = True
            self.myKeyMappingUI.ids.powerta.value = self.cmd[self.cmdkey]["A"]["Power"]
            self.myKeyMappingUI.ids.tachoa.value = self.cmd[self.cmdkey]["A"]["Tacho"]
            
            self.myKeyMappingUI.ids.ra.active = False
            self.myKeyMappingUI.ids.powerra.value = 0           
            
        else:
            self.myKeyMappingUI.ids.ta.active = False
            self.myKeyMappingUI.ids.powerta.value = 0
            self.myKeyMappingUI.ids.tachoa.value = 0                   

            self.myKeyMappingUI.ids.ra.active = False
            self.myKeyMappingUI.ids.powerra.value = 0     
            
        if self.cmd[self.cmdkey]["B"]["Run"] == 1:
            self.myKeyMappingUI.ids.rb.active = True
            self.myKeyMappingUI.ids.powerrb.value = self.cmd[self.cmdkey]["B"]["Power"]

            self.myKeyMappingUI.ids.tb.active = False
            self.myKeyMappingUI.ids.powertb.value = 0
            self.myKeyMappingUI.ids.tachob.value = 0            
            
        elif self.cmd[self.cmdkey]["B"]["Turn"] == 1:
            self.myKeyMappingUI.ids.tb.active = True
            self.myKeyMappingUI.ids.powertb.value = self.cmd[self.cmdkey]["B"]["Power"]
            self.myKeyMappingUI.ids.tachob.value = self.cmd[self.cmdkey]["B"]["Tacho"]
            
            self.myKeyMappingUI.ids.rb.active = False
            self.myKeyMappingUI.ids.powerrb.value = 0          
            
        else:
            self.myKeyMappingUI.ids.tb.active = False
            self.myKeyMappingUI.ids.powertb.value = 0
            self.myKeyMappingUI.ids.tachob.value = 0            
            
            
            self.myKeyMappingUI.ids.rb.active = False
            self.myKeyMappingUI.ids.powerrb.value = 0                
            
        if self.cmd[self.cmdkey]["C"]["Run"] == 1:
            self.myKeyMappingUI.ids.rc.active = True
            self.myKeyMappingUI.ids.powerrc.value = self.cmd[self.cmdkey]["C"]["Power"]

            self.myKeyMappingUI.ids.tc.active = False
            self.myKeyMappingUI.ids.powertc.value = 0
            self.myKeyMappingUI.ids.tachoc.value = 0
            
        elif self.cmd[self.cmdkey]["C"]["Turn"] == 1:
            self.myKeyMappingUI.ids.tc.active = True
            self.myKeyMappingUI.ids.powertc.value = self.cmd[self.cmdkey]["C"]["Power"]
            self.myKeyMappingUI.ids.tachoc.value = self.cmd[self.cmdkey]["C"]["Tacho"]

            self.myKeyMappingUI.ids.rc.active = False
            self.myKeyMappingUI.ids.powerrc.value = 0
            
        else:
            self.myKeyMappingUI.ids.tc.active = False
            self.myKeyMappingUI.ids.powertc.value = 0
            self.myKeyMappingUI.ids.tachoc.value = 0
            

            self.myKeyMappingUI.ids.rc.active = False
            self.myKeyMappingUI.ids.powerrc.value = 0

    def tmpkeymapping(self):
        self.mapping[self.cmdkey] = self.myKeyMappingUI.ids.key.text
        exec("self.myMappingUI.ids.%s.text = self.myKeyMappingUI.ids.key.text"%(self.cmdkey))
    
        self.mapping[self.cmdkey]=self.myKeyMappingUI.ids.key.text
        if self.myKeyMappingUI.ids.ra.state == "down":
            self.cmd[self.cmdkey]["A"]["Run"]=1
            self.cmd[self.cmdkey]["A"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powerra.value))[:-2])
        elif self.myKeyMappingUI.ids.ta.state == "down":
            self.cmd[self.cmdkey]["A"]["Turn"]=1
            self.cmd[self.cmdkey]["A"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powerta.value))[:-2])
            self.cmd[self.cmdkey]["A"]["Tacho"]=int(str(round(self.myKeyMappingUI.ids.tachoa.value))[:-2])

        if self.myKeyMappingUI.ids.rb.state == "down":
            self.cmd[self.cmdkey]["B"]["Run"]=1
            self.cmd[self.cmdkey]["B"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powerrb.value))[:-2])

        elif self.myKeyMappingUI.ids.tb.state == "down":
            self.cmd[self.cmdkey]["B"]["Turn"]=1
            self.cmd[self.cmdkey]["B"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powertb.value))[:-2])
            self.cmd[self.cmdkey]["B"]["Tacho"]=int(str(round(self.myKeyMappingUI.ids.tachob.value))[:-2])
            
        if self.myKeyMappingUI.ids.rc.state == "down":
            self.cmd[self.cmdkey]["C"]["Run"]=1
            self.cmd[self.cmdkey]["C"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powerrc.value))[:-2])

        elif self.myKeyMappingUI.ids.tc.state == "down":
            self.cmd[self.cmdkey]["C"]["Turn"]=1
            self.cmd[self.cmdkey]["C"]["Power"]=int(str(round(self.myKeyMappingUI.ids.powertc.value))[:-2])
            self.cmd[self.cmdkey]["C"]["Tacho"]=int(str(round(self.myKeyMappingUI.ids.tachoc.value))[:-2])
   
        #self.cmd[self.cmdkey][self.myKeyMappingUI.ids.key.text]=str(cmd)

    def savesettings(self):
        padname=self.myPadSettingsUI.ids.padname.text
        if padname != "":
            directory="./data/pads/"+padname
            try:
                os.stat(directory)
            except:
                os.mkdir(directory) 
            self.ports = {}
            self.ports["1"]=self.myPortSettingsUI.ids.port1.text
            self.ports["2"]=self.myPortSettingsUI.ids.port2.text
            self.ports["3"]=self.myPortSettingsUI.ids.port3.text
            self.ports["4"]=self.myPortSettingsUI.ids.port4.text
            self.ports["A"]=self.myPortSettingsUI.ids.porta.text
            self.ports["B"]=self.myPortSettingsUI.ids.portb.text
            self.ports["C"]=self.myPortSettingsUI.ids.portc.text
            with open("data/pads/%s/ports.json"%(padname), 'w') as json_file:
                json.dump(self.ports, json_file)
            with open("data/pads/%s/cmd.json"%(padname), 'w') as json_file:
                json.dump(self.cmd, json_file)
            self.pad={}
            self.pad["video"]=self.myVideoIPUI.ids.ip.text
            if self.myMappingUI.ids.pad1.state == "down": self.pad["pad1"]="down"
            else: self.pad["pad1"]="normal"
            if self.myMappingUI.ids.pad2.state == "down": self.pad["pad2"]="down"
            else: self.pad["pad2"]="normal"
            self.pad["controlmode"]=self.myMappingUI.ids.controlmode.text
            with open("data/pads/%s/pad.json"%(padname), 'w') as json_file:
                json.dump(self.pad, json_file)
            with open("data/pads/%s/mapping.json"%(padname), 'w') as json_file:
                json.dump(self.mapping, json_file)
            self.showpads()
    def showpads(self):
        self.myControlPadsUI.ids.pads.clear_widgets()
        self.myControlPadsUI.ids.pads.bind(minimum_height=self.myControlPadsUI.ids.pads.setter('height'))
        folders = list(os.listdir("./data/pads"))
        for x in sorted(folders):
            layout=BoxLayout(orientation="horizontal",size_hint= (1,None),height= "50dp")
            layout.add_widget(Button(id=x,text=x,on_release=partial(self.open_settings,x)))
            layout.add_widget(Button(id=x,text="conf",size_hint= (None,None),height= "50dp",width="50dp",on_release=partial(self.open_settings,x)))
            layout.add_widget(Button(id=x,text="del",size_hint= (None,None),height= "50dp",width="50dp",on_release=partial(self.delete_pad,x)))
            layout.add_widget(Button(id=x,text="play",size_hint= (None,None),height= "50dp",width="50dp",on_release=partial(self.play_pad,x)))
            self.myControlPadsUI.ids.pads.add_widget(layout)
  
    def delete_pad(self,pad,dt=None):
        directory="./data/pads/%s/"%(pad)
        shutil.rmtree(directory)
        self.showpads()

    def open_settings(self,pad,dt=None):
        self.open_pad(pad)
        self.myPadSettingsUI.open()

        self.myVideoIPUI.ids.ip.text=self.pad["video"]

        self.myPadSettingsUI.ids.padname.text=pad
        self.myPortSettingsUI.ids.porta.text=self.ports["A"]
        self.myPortSettingsUI.ids.portb.text=self.ports["B"]
        self.myPortSettingsUI.ids.portc.text=self.ports["C"]
        self.myPortSettingsUI.ids.port1.text=self.ports["1"]
        self.myPortSettingsUI.ids.port2.text=self.ports["2"]
        self.myPortSettingsUI.ids.port3.text=self.ports["3"]
        self.myPortSettingsUI.ids.port4.text=self.ports["4"]

        if self.pad["pad1"]=="down": self.myMappingUI.ids.pad1.state = "down"
        else:self.myMappingUI.ids.pad1.state = "normal"
        if self.pad["pad2"]=="down": self.myMappingUI.ids.pad2.state = "down"
        else:self.myMappingUI.ids.pad2.state = "normal"
        
        for x in self.mapping:
            code="self.myMappingUI.ids.%s.text = '%s'"%(x, self.mapping[x])
            print code
            exec(code)

    def open_pad(self,pad=None,dt=None):
        directory="./data/pads/%s/"%(pad)
        print directory
        try:
            os.stat(directory)
            print "?????????"
        except:
            os.mkdir(directory) 
        with open("%sports.json"%(directory)) as json_file:
            self.ports = json.load(json_file)
        with open("%scmd.json"%(directory)) as json_file:
            self.cmd = json.load(json_file)
        with open("%spad.json"%(directory)) as json_file:
            self.pad = json.load(json_file)            
        with open("%smapping.json"%(directory)) as json_file:
            self.mapping = json.load(json_file)    
        
        self.myVideoPadUI.ids.video.source = self.pad["video"]

       
    def play_pad(self,pad,dt=None):
        self.open_pad(pad)
        #self.findbrick()
        #self.mainloop = Clock.schedule_interval(self.main, 1 / 30.)
        self.power={}
        ports=["A","B","C"]
        for y in ports:
            self.power[y]=0
        print self.power

        self.play=True
        self.myVideoPadUI.ids.video.play=True
        self.myMainPanel.ids.ScrMan.current = self.myVideoPadUI.name   
        self.myVideoPadUI.clear_widgets()
        self.myVideoPadUI.add_widget(Video(id="video",source=self.pad["video"],play=True))
        if self.pad["controlmode"] == "Tank":
            self.myVideoPadUI.add_widget(self.myTankControlWidget)
        elif self.pad["pad2"] == "down":
            self.myVideoPadUI.add_widget(self.myDualClassicControlWidget)
            for x in self.mapping:
                code="self.myDualClassicControlWidget.ids.%s.text = '%s'"%(x, self.mapping[x])
                print code
                exec(code)
        else:
            self.myVideoPadUI.add_widget(self.myClassicControlWidget)
            for x in self.mapping:
                code="self.myClassicControlWidget.ids.%s.text = '%s'"%(x, self.mapping[x])
                print code
                exec(code)
        self.mainloop = Clock.schedule_interval(self.main, 1 / 30.)

    ###MAIN FUNCTIONS       
            
    def findbrick(self):
        print "Finding a brick..."
        try:
            # Locate the brick
            self.b = nxt.locator.find_one_brick()
            print "Brick connected"
        except:
            print "Sorry, we couldn't find a nxt brick..."
            sys.exit()
    def main(self,dt):
        if self.b:
            Motor(self.b, PORT_A).run(self.power["A"])
            Motor(self.b, PORT_B).run(self.power["B"])
            Motor(self.b, PORT_C).run(self.power["C"]) 
            """
            if self.controlmode == "tank":
                forwardA = self.myTankControlWidget.s1
                forwardB = self.myTankControlWidget.s2
                print forwardA, forwardB
                Motor(self.b, PORT_A).run(forwardA)
                Motor(self.b, PORT_B).run(forwardB)
            """
            pass
        else:
           print 'No NXT bricks found'

if __name__ == '__main__':
    MainApp().run()
