from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock


class LapWidget(GridLayout):
    def __init__(self, time, lap_number):
        super(LapWidget, self).__init__()
        self.cols = 1
        self.size_hint_y = None
        self.height = 50
        grid = GridLayout(cols=2)
        grid.add_widget(Label(text='Lap'+str(lap_number), size=(50, 50), size_hint_x=0.5, color=(0, 20, 0, 1)))
        grid.add_widget(Label(text=time, size_hint_x=0.5))
        self.add_widget(grid)

# This is the main grid
class MainGrid(GridLayout):

    # method for starting and stopping the stopwatch
    def start_stop(self):
        if not self.is_running:
            self.is_running = True
            self.clock_event = Clock.schedule_interval(self.update, 0.1)
        else:
            self.is_running = False
            self.clock_event.cancel()

    # method for adding a lap widget to the scrollview
    def lap(self):
        # Adding the current time to the list of laps
        self.number_of_laps += 1
        self.ids.scrollview.add_widget(LapWidget(self.ids.time.text, self.number_of_laps))
        # making the scrollview larger to fit the new lap
        self.ids.scrollview.height += 50

    # method for reseting everything
    def reset(self):
        self.is_running = False
        self.time = 0
        self.ids.time.text = '00:00:00'
        if self.clock_event:
            self.clock_event.cancel()
        # Clearing the scrollview
        self.ids.scrollview.clear_widgets()
        self.ids.scrollview.height = 0
        self.number_of_laps = 0
        # Changing the color and text of the start/stop button
        self.ids.start_stop.color = [0, 1, 0, 1]
        self.ids.start_stop.text = 'Start'

    # method that updates the time label
    def update(self, t):
        self.time += 0.1
        hours, remainder = divmod(self.time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.ids.time.text = ('%02d:%02d:%02d' % (hours, minutes, seconds))

    # method to change the color of the start/stop button
    def start_stop_change_color(self,button):
        if button.color == [0, 1, 0, 1]:
            button.color = [1, 0, 0, 1]
            button.text = 'Stop'
        else:
            button.color = [0, 1, 0, 1]
            button.text = 'Start'

class StopwatchApp(App):
    def build(self):
        return MainGrid()


if __name__ == '__main__':
    StopwatchApp().run()