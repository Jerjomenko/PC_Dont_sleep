from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import  Window
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar

Window.size = (480, 350)

KV = """
MDScreen:
    md_bg_color: .5, .3, .4, .4
    
    MDLabel:
        text: " Введите необходимое время работы программы"
        pos_hint: {"center_x": .5, "center_y": .93}
        font_style: "H6"
    
    MDLabel:
        id: t
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
        font_style: "H6"
        bold: True
        pos_hint: {"center_x": .74, "center_y": .72} 
        
    MDLabel:
        text: "Минуты"
        font_style: "H6"
        bold: True
        pos_hint: {"center_x": 1.11, "center_y": .72} 
         
  
           
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
        #Clock.schedule_interval(self.update_time, 0)


    def build(self):
        return Builder.load_string(KV)


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
                    return self.vremja

            else:
                self.snacbar = Snackbar(text="Введёное значение должно быть числом.")
                self.snacbar.open()
        except ValueError:
            print("Введёное значение должно быть числом.")



if __name__ == "__main__":
    TestApp().run()