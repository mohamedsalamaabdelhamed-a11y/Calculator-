from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Calculator(App):

    def build(self):

        self.first_number = None
        self.operator = None

        layout = GridLayout(
            cols=4,
            rows=6,
            spacing=5,
            padding=10
        )

        self.display = TextInput(
            text="",
            readonly=True,
            halign="right",
            font_size=30,
            multiline=False
        )

        layout.add_widget(self.display)

        buttons = [
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "-",
            "0", ".", "=", "+",
            "C", "⌫", "%"
        ]

        for text in buttons:

            button = Button(
                text=text,
                font_size=22
            )

            button.bind(
                on_press=self.button_pressed
            )

            layout.add_widget(button)

        return layout


    def button_pressed(self, button):

        value = button.text

        if value in "0123456789.":

            self.display.text += value

        elif value in ["+", "-", "×", "÷"]:

            self.first_number = float(
                self.display.text
            )

            self.operator = value

            self.display.text += " " + value + " "

        elif value == "=":

            self.calculate()

        elif value == "C":

            self.clear()

        elif value == "⌫":

            self.display.text = self.display.text[:-1]

        elif value == "%":

            try:

                number = float(
                    self.display.text
                )

                self.display.text = str(
                    number / 100
                )

            except:

                self.clear()


    def calculate(self):

        try:

            parts = self.display.text.split()

            second_number = float(parts[2])

            if self.operator == "+":

                result = (
                    self.first_number +
                    second_number
                )

            elif self.operator == "-":

                result = (
                    self.first_number -
                    second_number
                )

            elif self.operator == "×":

                result = (
                    self.first_number *
                    second_number
                )

            elif self.operator == "÷":

                if second_number == 0:

                    self.display.text = "خطأ"
                    return

                result = (
                    self.first_number /
                    second_number
                )

            if result == int(result):

                self.display.text = str(
                    int(result)
                )

            else:

                self.display.text = str(
                    result
                )

        except:

            self.display.text = "خطأ"


    def clear(self):

        self.display.text = ""

        self.first_number = None
        self.operator = None


Calculator().run()
