from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import  Window
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
import pyautogui
import datetime
import random


Window.size = (480, 350)

KV = """
MDScreen:
    canvas:
        Color:
            rgba: 1, 1, 1, 15
        Rectangle:
            source: "kosmos.jpg"
            size: self.size
            pos: self.pos
    
    MDLabel:
        text: " Введите необходимое время работы программы"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        pos_hint: {"center_x": .5, "center_y": .93}
        font_style: "H6"
    
    MDLabel:
        id: t
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        halign: "center"
        markup: True
        
    MDTextFieldRect: 
        id: chas
        size_hint: .2, None
        height: "30dp"
        pos_hint: {"center_x": .3, "center_y": .8}   
  
    MDTextFieldRect: 
        id: minut
        size_hint: .2, None
        height: "30dp"
        pos_hint: {"center_x": .7, "center_y": .8}  
        
    MDLabel:
        text: "Часы"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "H6"
        bold: True
        pos_hint: {"center_x": .74, "center_y": .72} 
        
    MDLabel:
        text: "Минуты"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_style: "H6"
        bold: True
        pos_hint: {"center_x": 1.11, "center_y": .72} 
         
    MDLabel:
        id: realtime
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        bold: True
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .3} 
        
           
    MDRaisedButton:
        id: start_stop
        text: "START"
        pos_hint:{"center_x": .2, "center_y": .1}
        on_release:
            app.show_time()
        
    MDRaisedButton:
        id: reset
        text: "RESET"
        pos_hint:{"center_x": .8, "center_y": .1}
        on_release:
            app.reset()
        
    
        

"""


class TestApp(MDApp):
    started = False
    seconds = 0
    vremja = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_start(self):
        ch = "0"
        m = "0"
        s = "0"
        part_s = "0"
        self.root.ids.t.text = f"[size=45]{int(ch):02}[/size][size=30]:[size=45]{int(m):02}[/size][size=30]:[/size][size=60]{int(s):02}[/size][size=30].[/size][size=30]{int(part_s):02}[/size]"
        Clock.schedule_interval(self.get_table_time, 1)

    def build(self):
        return Builder.load_string(KV)

    def get_table_time(self, *args):
        t_now = datetime.datetime.now()
        str_t = t_now.strftime("%H:%M:%S")
        self.root.ids.realtime.text = str_t



    def update_time(self, obj):
        if self.started:
            self.seconds += obj
        minutes, seconds = divmod(self.seconds, 60)
        chas = seconds // 3600
        part_seconds = seconds * 100 % 100
        self.root.ids.t.text = f"[size=45]{int(chas):02}[/size][size=30]:[size=45]{int(minutes):02}[/size][size=30]:[/size][size=60]{int(seconds):02}[/size][size=30].[/size][size=30]{int(part_seconds):02}[/size]"
        if int(self.seconds) == self.vremja:
            TestApp.stop(self)

    def start_stop(self):
        self.root.ids.start_stop.text = "START" if self.started else "STOP"
        self.started = not self.started
        self.root.ids.reset.disabled = True if self.started else False
        Clock.schedule_interval(self.update_time, 0)

    def reset(self):
        if self.started:
            self.started = False
        self.seconds = 0

    def show_time(self):
        self.vremja = 0
        try:
            if self.root.ids.minut.text.isdigit() or self.root.ids.chas.text.isdigit():
                try:
                    if self.root.ids.minut.text.isdigit():
                        a = int(self.root.ids.minut.text) * 60
                        self.vremja += a
                    else:
                        if len(self.root.ids.minut.text):
                            self.snacbar = Snackbar(text="Проверьте правильно ли вы ввели значение минут!")
                            self.snacbar.open()
                except:
                    pass
                try:
                    if self.root.ids.chas.text.isdigit():
                        b = int(self.root.ids.chas.text) * 3600
                        self.vremja += b
                    else:
                        if len(self.root.ids.chas.text) > 0:
                            self.snacbar = Snackbar(text="Проверьте правильно ли вы ввели значение часов!")
                            self.snacbar.open()

                except:
                    pass

                if self.vremja != 0:
                    self.start_stop()
                    Clock.schedule_interval(self.move_mouse, 5)
                    return self.vremja

            else:
                self.snacbar = Snackbar(text="Введёное значение должно быть числом.")
                self.snacbar.open()
        except ValueError:
            print("Введёное значение должно быть числом.")

    def move_mouse(self, *args):
        pyautogui.moveTo(random.randint(200, 1000), random.randint(200, 1000))



if __name__ == "__main__":
    TestApp().run()