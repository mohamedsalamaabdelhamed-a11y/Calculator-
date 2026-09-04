from kivy.app import App
from kivy.uix.label import Label


class CalculatorApp(App):

    def build(self):
        return Label(
            text="Calculator\nTest OK",
            font_size="30sp"
        )


if __name__ == "__main__":
    CalculatorApp().run()
