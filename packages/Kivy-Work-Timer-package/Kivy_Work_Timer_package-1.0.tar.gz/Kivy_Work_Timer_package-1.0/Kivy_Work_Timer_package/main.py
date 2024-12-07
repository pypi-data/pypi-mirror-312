from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

sound = SoundLoader.load('notification.mp3')

class Config_popup(Popup):
    
    def save_config(self, w, r, l,f, caller):
        if w == ''or int(w) <=0: w = 1
        if r == ''or int(r) <=0: r = 1
        if l == ''or int(l) <=0: l = 1
        if f == ''or int(f) <=0: f = 1
        caller.apply_config(w, r, l,f)
        self.dismiss()

    def get_info(self, caller):
        self.work_time = caller.work_time
        self.rest_time = caller.rest_time
        self.long_rest_time = caller.long_rest_time
        self.number_of_work_faizes = caller.number_of_work_faizes
        self.caller = caller

class MainGrid(GridLayout):

    def start_stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.clock_event.cancel()
            self.ids.start_stop.text = "Resume"
            self.ids.start_stop.color = (0, 1, 0, 1)
            self.ids.status.text = "Paused during " + self.ids.status.text
            self.ids.status.color = (1, 1, 0, 1)
        else:
            self.is_running = True
            self.clock_event = Clock.schedule_interval(self.update_timer, 1)
            self.ids.start_stop.text = "Stop"
            self.ids.start_stop.color = (1, 0, 0, 1)
            self.ids.status.text = "Working..."
            self.ids.status.color = (0, 1, 0, 1)

    def reset_timer(self):
        self.work_time = self.original_times[0]
        self.rest_time = self.original_times[1]
        self.long_rest_time = self.original_times[2]
        self.faze_counter = 1
        self.ids.status.text = "Work Timer"
        self.ids.status.color = (0, 0, 1, 1)
        if self.is_running:
            self.clock_event.cancel()
            self.is_running = False
        self.ids.timer.text = '%02d:%02d' % (int(self.work_time/60), self.work_time % 60)
        self.ids.start_stop.text = "Start"
        self.ids.start_stop.color = (0, 1, 0, 1)
        self.is_working = True

    def open_config(self):
        self.config_popup = Config_popup()
        self.config_popup.get_info(self)
        self.config_popup.open()

    def apply_config(self, work, rest, long_rest, faizes):
        self.work_time = int(work)*60
        self.rest_time = int(rest)*60
        self.long_rest_time = int(long_rest)*60
        self.original_times = [self.work_time, self.rest_time, self.long_rest_time]
        self.faze_counter = 1
        self.number_of_work_faizes = int(faizes)
        if self.is_running:
            self.clock_event.cancel()
        self.ids.timer.text = '%02d:%02d' % (int(self.work_time/60), self.work_time % 60)
        self.ids.status.text = "Work Timer"
        self.ids.status.color = (0, 0, 1, 1)
        self.is_working = True
        self.is_running = False
        self.ids.start_stop.text = "Start"

    def update_timer(self, t):
        if self.is_working:
            self.work_time -= 1
            time = self.work_time
        elif self.faze_counter % (self.number_of_work_faizes*2) == 0:
            self.long_rest_time -= 1
            time = self.long_rest_time
        else:
            self.rest_time -= 1
            time = self.rest_time
        minutes, remainder = divmod(time, 60)
        self.ids.timer.text = ("%02d:%02d" % (minutes, remainder))
        self.check_time()

    def check_time(self):
        if self.faze_counter % self.number_of_work_faizes*2 == 0 and self.work_time == 0 and self.long_rest_time > 0:
            self.is_working = False
            self.work_time = self.original_times[0]
            self.ids.timer.text = "%02d:00" % (self.long_rest_time/60)
            self.ids.status.text = "End Break Time"
            self.ids.status.color = (1, 0, 0, 1)
            self.faze_counter += 1
            sound.play()
        elif self.faze_counter % self.number_of_work_faizes*2 == 0 and self.long_rest_time <= 0:
            if self.is_running:
                self.clock_event.cancel()
            self.is_running = False
            self.ids.timer.text = "00:00"
            self.ids.status.text = "You are done, press reset if you want to start again"
            self.ids.status.color = (1, 1, 0, 1)
        elif self.work_time == 0:
            self.is_working = False
            self.work_time = self.original_times[0]
            self.ids.timer.text = "%02d:00" % (self.rest_time/60)
            self.ids.status.text = "Break Time"
            self.ids.status.color = (1, 0, 0, 1)
            self.faze_counter += 1
            sound.play()
        elif self.rest_time == 0:
            self.is_working = True
            self.rest_time = self.original_times[1]
            self.ids.timer.text = "%02d:00" % (self.work_time/60)
            self.ids.status.text = "Working..."
            self.ids.status.color = (0, 1, 0, 1)
            self.faze_counter += 1
            sound.play()

class Work_timerApp(App):
    def build(self):
        return MainGrid()

Work_timerApp().run()