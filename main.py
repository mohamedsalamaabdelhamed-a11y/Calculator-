from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class Calculator(App):

    def build(self):
        # لون خلفية التطبيق (رمادي فاتح/أبيض فاتح كالصورة)
        Window.clearcolor = (0.96, 0.96, 0.96, 1)

        self.first_number = None
        self.operator = None
        self.new_number = True
        self.history = []  # حفظ السجل
        self.arabic_mode = False  # وضع الأرقام (الإنجليزية افتراضياً)

        # جدول تحويل الأرقام
        self.digits_en = "0123456789"
        self.digits_ar = "٠١٢٣٤٥٦٧٨٩"

        main_layout = BoxLayout(
            orientation="vertical",
            padding=[15, 10, 15, 15],
            spacing=5
        )

        # --- الشريط العلوي (زر الإعدادات) ---
        top_bar = BoxLayout(
            size_hint_y=0.08,
            orientation="horizontal"
        )
        
        settings_btn = Button(
            text="⚙️",
            font_size=22,
            size_hint_x=0.15,
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(0.2, 0.2, 0.2, 1)
        )
        settings_btn.bind(on_press=self.open_settings)
        
        top_bar.add_widget(settings_btn)
        top_bar.add_widget(Label(size_hint_x=0.85)) # مساحة فارغة
        main_layout.add_widget(top_bar)

        # --- شاشة الحاسبة ---
        self.display = TextInput(
            text=self.to_display_text("0"),
            readonly=True,
            halign="right",
            font_size=48,
            multiline=False,
            size_hint_y=0.22,
            background_color=(0.96, 0.96, 0.96, 1),
            foreground_color=(0, 0, 0, 1)
        )
        main_layout.add_widget(self.display)

        # --- لوحة الأزرار (4 أعمدة) ---
        layout = GridLayout(
            cols=4,
            spacing=10,
            padding=5
        )

        buttons = [
            "AC", "⌫", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "🔄", "0", ".", "="
        ]

        # الألوان
        ORANGE_BG = (1, 0.4, 0, 1)        # لون زر يساوي البرتقالي
        LIGHT_TEXT_BG = (0.92, 0.92, 0.92, 1) # خلفية الأزرار العلمية
        NUM_BG = (0.98, 0.98, 0.98, 1)    # خلفية أزرار الأرقام
        ORANGE_TEXT = (0.9, 0.35, 0, 1)   # نص الأزرار العلمية

        for text in buttons:
            if text == "=":
                bg_color = ORANGE_BG
                text_color = (1, 1, 1, 1)
            elif text in ["AC", "⌫", "%", "÷", "×", "-", "+"]:
                bg_color = LIGHT_TEXT_BG
                text_color = ORANGE_TEXT
            else:
                bg_color = NUM_BG
                text_color = (0, 0, 0, 1)

            # تحويل الأرقام على الأزرار حسب الوضع
            display_btn_text = self.to_display_text(text) if text in "0123456789" else text

            button = Button(
                text=display_btn_text,
                font_size=24,
                bold=True,
                background_normal="",
                background_color=bg_color,
                color=text_color
            )
            button.raw_text = text  # الاحتفاظ بالنص الأصلي لسهولة البرمجة
            button.bind(on_press=self.button_pressed)
            layout.add_widget(button)

        main_layout.add_widget(layout)
        return main_layout

    # --- تحويل الأرقام بين العربية والإنجليزية ---
    def to_display_text(self, text):
        if not self.arabic_mode:
            return text
        trans = str.maketrans(self.digits_en, self.digits_ar)
        return text.translate(trans)

    def to_raw_text(self, text):
        trans = str.maketrans(self.digits_ar, self.digits_en)
        return text.translate(trans)

    # --- نافذة الإعدادات والسجل ---
    def open_settings(self, instance):
        content = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # زر التحويل بين الأرقام العربية والإنجليزية
        lang_text = "تغيير الأرقام إلى: الإنجليزية (123)" if self.arabic_mode else "تغيير الأرقام إلى: العربية (١٢٣)"
        btn_lang = Button(
            text=lang_text,
            size_hint_y=0.2,
            background_color=(0.9, 0.35, 0, 1),
            color=(1, 1, 1, 1)
        )
        
        # عرض السجل
        content.add_widget(Label(text="-- سجل العمليات --", size_hint_y=0.1, color=(0,0,0,1), bold=True))
        
        scroll = ScrollView(size_hint_y=0.7)
        history_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=5)
        history_layout.bind(minimum_height=history_layout.setter('height'))

        if not self.history:
            history_layout.add_widget(Label(text="لا يوجد سجل حتى الآن", color=(0.5,0.5,0.5,1), size_hint_y=None, height=40))
        else:
            for item in reversed(self.history):
                lbl = Label(
                    text=self.to_display_text(item),
                    color=(0.1, 0.1, 0.1, 1),
                    size_hint_y=None,
                    height=35,
                    halign="right"
                )
                history_layout.add_widget(lbl)

        scroll.add_widget(history_layout)
        content.add_widget(scroll)
        content.add_widget(btn_lang)

        popup = Popup(
            title="الإعدادات والسجل",
            content=content,
            size_hint=(0.85, 0.7),
            background=""
        )

        def switch_language(btn_instance):
            self.arabic_mode = not self.arabic_mode
            popup.dismiss()
            # إعادة تشغيل الواجهة بتعديل الأرقام
            self.root.clear_widgets()
            self.root.add_widget(self.build())

        btn_lang.bind(on_press=switch_language)
        popup.open()

    # --- إدارة الأزرار والحساب ---
    def button_pressed(self, button):
        value = button.raw_text
        current_display_raw = self.to_raw_text(self.display.text)

        if value in "0123456789.":
            if self.new_number or current_display_raw == "0" or current_display_raw == "خطأ":
                new_val = "0." if value == "." else value
                self.display.text = self.to_display_text(new_val)
                self.new_number = False
            else:
                if value == "." and "." in current_display_raw.split()[-1]:
                    return
                self.display.text = self.to_display_text(current_display_raw + value)

        elif value in ["+", "-", "×", "÷"]:
            try:
                parts = current_display_raw.split()
                if len(parts) == 3:
                    self.calculate()
                    current_display_raw = self.to_raw_text(self.display.text)
                
                self.first_number = float(current_display_raw)
                self.operator = value
                res = f"{self.format_number(self.first_number)} {value} "
                self.display.text = self.to_display_text(res)
                self.new_number = True
            except:
                self.clear()

        elif value == "=":
            self.calculate()

        elif value in ["C", "AC"]:
            self.clear()

        elif value == "⌫":
            if current_display_raw in ["خطأ", "0"]:
                self.clear()
            else:
                updated = current_display_raw.strip()[:-1]
                if not updated:
                    updated = "0"
                self.display.text = self.to_display_text(updated)

        elif value == "%":
            try:
                parts = current_display_raw.split()
                if len(parts) == 3:
                    num = float(parts[2])
                    res = f"{parts[0]} {parts[1]} {self.format_number(num / 100)}"
                else:
                    num = float(current_display_raw)
                    res = self.format_number(num / 100)
                self.display.text = self.to_display_text(res)
            except:
                self.display.text = "خطأ"

    def calculate(self):
        try:
            raw_text = self.to_raw_text(self.display.text)
            parts = raw_text.split()
            if len(parts) != 3:
                return

            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])

            if op == "+": res = num1 + num2
            elif op == "-": res = num1 - num2
            elif op == "×": res = num1 * num2
            elif op == "÷":
                if num2 == 0:
                    self.display.text = "خطأ"
                    self.reset_state()
                    return
                res = num1 / num2
            else: return

            formatted_res = self.format_number(res)
            # إضافة العملية إلى السجل
            self.history.append(f"{raw_text} = {formatted_res}")

            self.display.text = self.to_display_text(formatted_formatted_res if 'formatted_formatted_res' in locals() else formatted_res)
            self.reset_state()
        except:
            self.display.text = "خطأ"
            self.reset_state()

    def clear(self):
        self.display.text = self.to_display_text("0")
        self.reset_state()

    def reset_state(self):
        self.first_number = None
        self.operator = None
        self.new_number = True

    def format_number(self, number):
        if number == int(number):
            return str(int(number))
        return f"{number:.8f}".rstrip("0").rstrip(".")

if __name__ == "__main__":
    Calculator().run()
