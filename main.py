
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# ضبط خلفية التطبيق باللون الأبيض
Window.clearcolor = (0.97, 0.97, 0.97, 1)

class XiaomiButton(Button):
    def __init__(self, bg_color=(1, 1, 1, 1), text_color=(0, 0, 0, 1), radius=25, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = text_color
        self.font_size = '22sp'
        self.bold = True
        self.custom_bg = bg_color
        self.radius = radius

        with self.canvas.before:
            self.canvas_color = Color(*self.custom_bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class CalculatorApp(App):
    def build(self):
        self.title = "Calculator"
        self.expression = ""
        self.history = []
        self.arabic_digits = False

        # الحاوية الرئيسية
        main_layout = BoxLayout(orientation='vertical', padding=16, spacing=10)

        # الشريط العلوي (الإعدادات/السجل)
        top_bar = BoxLayout(size_hint_y=0.08, spacing=10)
        
        btn_history = Button(text="السجل", size_hint_x=0.3, background_color=(0,0,0,0), color=(0.4, 0.4, 0.4, 1))
        btn_history.bind(on_release=self.show_history)
        
        btn_lang = ToggleButton(text="عربي / EN", size_hint_x=0.4, background_color=(0,0,0,0), color=(0.4, 0.4, 0.4, 1))
        btn_lang.bind(on_release=self.toggle_language)

        top_bar.add_widget(btn_history)
        top_bar.add_widget(Label(size_hint_x=0.3)) # مساحة فارغة
        top_bar.add_widget(btn_lang)
        main_layout.add_widget(top_bar)

        # شاشة عرض الحسابات والنتائج
        display_box = BoxLayout(orientation='vertical', size_hint_y=0.27, padding=[10, 10])
        
        self.sub_display = Label(
            text="", 
            font_size='18sp', 
            color=(0.5, 0.5, 0.5, 1), 
            halign='right', 
            valign='bottom',
            text_size=(Window.width - 40, None)
        )
        self.main_display = Label(
            text="0", 
            font_size='48sp', 
            color=(0, 0, 0, 1), 
            bold=True, 
            halign='right', 
            valign='bottom',
            text_size=(Window.width - 40, None)
        )
        
        display_box.add_widget(self.sub_display)
        display_box.add_widget(self.main_display)
        main_layout.add_widget(display_box)

        # شبكة الأزرار
        grid = GridLayout(cols=4, spacing=12, size_hint_y=0.65)

        # الألوان المعتمدة في تصميم شاومي
        c_white = (1, 1, 1, 1)
        c_gray_btn = (0.94, 0.94, 0.94, 1)
        c_orange = (1, 0.4, 0, 1)
        c_orange_text = (1, 0.4, 0, 1)
        c_black_text = (0.1, 0.1, 0.1, 1)

        # أزرار لوحة التحكم
        buttons = [
            ('AC', c_gray_btn, c_orange_text),
            ('⌫', c_gray_btn, c_orange_text),
            ('%', c_gray_btn, c_orange_text),
            ('÷', c_gray_btn, c_orange_text),

            ('7', c_white, c_black_text),
            ('8', c_white, c_black_text),
            ('9', c_white, c_black_text),
            ('×', c_gray_btn, c_orange_text),

            ('4', c_white, c_black_text),
            ('5', c_white, c_black_text),
            ('6', c_white, c_black_text),
            ('-', c_gray_btn, c_orange_text),

            ('1', c_white, c_black_text),
            ('2', c_white, c_black_text),
            ('3', c_white, c_black_text),
            ('+', c_gray_btn, c_orange_text),

            ('⚙', c_white, c_orange_text),
            ('0', c_white, c_black_text),
            ('.', c_white, c_black_text),
            ('=', c_orange, c_white)
        ]

        for text, bg, fg in buttons:
            btn = XiaomiButton(text=text, bg_color=bg, text_color=fg)
            btn.bind(on_release=self.on_button_press)
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        return main_layout

    def convert_digits(self, text):
        if not self.arabic_digits:
            return text
        en_to_ar = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
        return text.translate(en_to_ar)

    def toggle_language(self, instance):
        self.arabic_digits = instance.state == 'down'
        self.update_display()

    def update_display(self):
        disp_text = self.expression if self.expression else "0"
        self.main_display.text = self.convert_digits(disp_text)

    def on_button_press(self, instance):
        text = instance.text

        if text == 'AC':
            self.expression = ""
            self.sub_display.text = ""
        elif text == '⌫':
            self.expression = self.expression[:-1]
        elif text == '=':
            self.calculate()
        elif text == '⚙':
            self.show_history(None)
        else:
            self.expression += text

        self.update_display()

    def calculate(self):
        try:
            formatted_expr = self.expression.replace('×', '*').replace('÷', '/')
            result = str(eval(formatted_expr))
            
            # إضافة الحساب للسجل
            record = f"{self.expression} = {result}"
            self.history.append(record)
            
            self.sub_display.text = self.convert_digits(self.expression)
            self.expression = result
        except Exception:
            self.main_display.text = "خطأ"
            self.expression = ""

    def show_history(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll = ScrollView()
        history_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        history_layout.bind(minimum_height=history_layout.setter('height'))

        if not self.history:
            history_layout.add_widget(Label(text="لا يوجد سجل حظر حالياً", size_hint_y=None, height=40, color=(0,0,0,1)))
        else:
            for item in reversed(self.history):
                lbl = Label(text=self.convert_digits(item), size_hint_y=None, height=40, color=(0.2, 0.2, 0.2, 1), font_size='18sp')
                history_layout.add_widget(lbl)

        scroll.add_widget(history_layout)
        content.add_widget(scroll)

        close_btn = Button(text="إغلاق", size_hint_y=0.15, background_color=(1, 0.4, 0, 1))
        popup = Popup(title='سجل العمليات الحسابية', content=content, size_hint=(0.85, 0.6))
        close_btn.bind(on_release=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()

if __name__ == '__main__':
    CalculatorApp().run()
