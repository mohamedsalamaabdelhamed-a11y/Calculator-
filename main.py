
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class Calculator(App):

    def build(self):

        # لون خلفية التطبيق
        Window.clearcolor = (0.08, 0.08, 0.10, 1)

        self.first_number = None
        self.operator = None
        self.new_number = True

        main_layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # شاشة الحاسبة
        self.display = TextInput(
            text="0",
            readonly=True,
            halign="right",
            font_size=36,
            multiline=False,
            size_hint_y=0.20,
            background_color=(0.15, 0.15, 0.18, 1),
            foreground_color=(1, 1, 1, 1)
        )

        main_layout.add_widget(self.display)

        # لوحة الأزرار
        layout = GridLayout(
            cols=4,
            spacing=5,
            padding=5
        )

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
                font_size=24,
                background_normal="",
                background_color=(0.18, 0.18, 0.22, 1),
                color=(1, 1, 1, 1)
            )

            button.bind(
                on_press=self.button_pressed
            )

            layout.add_widget(button)

        main_layout.add_widget(layout)

        return main_layout

    # -------------------------
    # التعامل مع الأزرار
    # -------------------------

    def button_pressed(self, button):

        value = button.text

        # الأرقام والنقطة
        if value in "0123456789.":

            if self.new_number:

                self.display.text = ""

                self.new_number = False

            # منع إدخال أكثر من نقطة
            if value == "." and "." in self.display.text:

                return

            self.display.text += value

        # العمليات الحسابية
        elif value in ["+", "-", "×", "÷"]:

            try:

                # إذا كانت هناك عملية سابقة
                if self.first_number is not None and self.operator:

                    self.calculate()

                self.first_number = float(
                    self.display.text
                )

                self.operator = value

                self.display.text = (
                    self.format_number(self.first_number)
                    + " "
                    + value
                    + " "
                )

                self.new_number = True

            except:

                self.clear()

        # يساوي
        elif value == "=":

            self.calculate()

        # مسح الكل
        elif value == "C":

            self.clear()

        # حذف آخر رقم
        elif value == "⌫":

            if not self.new_number:

                self.display.text = (
                    self.display.text[:-1]
                )

                if self.display.text == "":

                    self.display.text = "0"

        # النسبة المئوية
        elif value == "%":

            try:

                # إذا كانت الشاشة تحتوي على عملية
                parts = self.display.text.split()

                if len(parts) == 3:

                    number = float(parts[2])

                    self.display.text = (
                        parts[0]
                        + " "
                        + parts[1]
                        + " "
                        + self.format_number(number / 100)
                    )

                else:

                    number = float(
                        self.display.text
                    )

                    self.display.text = self.format_number(
                        number / 100
                    )

            except:

                self.display.text = "خطأ"

    # -------------------------
    # تنفيذ العملية
    # -------------------------

    def calculate(self):

        try:

            parts = self.display.text.split()

            if len(parts) != 3:

                return

            second_number = float(parts[2])

            if self.first_number is None:

                return

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

                    self.first_number = None
                    self.operator = None

                    return

                result = (
                    self.first_number /
                    second_number
                )

            else:

                return

            # عرض النتيجة بشكل صحيح
            self.display.text = self.format_number(
                result
            )

            self.first_number = None
            self.operator = None
            self.new_number = True

        except:

            self.display.text = "خطأ"

            self.first_number = None
            self.operator = None

    # -------------------------
    # تنظيف الشاشة
    # -------------------------

    def clear(self):

        self.display.text = "0"

        self.first_number = None
        self.operator = None
        self.new_number = True

    # -------------------------
    # تنسيق الأرقام
    # -------------------------

    def format_number(self, number):

        # إذا كان الرقم صحيحًا
        if number == int(number):

            return str(int(number))

        # إزالة الأصفار الزائدة
        return f"{number:.10f}".rstrip("0").rstrip(".")


Calculator().run()
