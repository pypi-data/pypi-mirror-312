import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

# the main grid layout of the calculator
class MyGrid(GridLayout):
    def result(instance, text):
        #print(text)
        try:
            return str(eval(text))
        except:
            return 'Error'

# the app class/root of the calculator
class CalculatorApp(App):
    def build(self):
        return MyGrid()

# create an instance of the app
if __name__ == '__main__':
    CalculatorApp().run()