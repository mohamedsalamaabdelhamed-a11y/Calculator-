import re
import arabic_reshaper
from bidi.algorithm import get_display

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.core.text import LabelBase


# =========================================================
# معالجة النص العربي
# =========================================================

def fix_text(text):
    """إصلاح عرض النص العربي وتوصيل الأحرف بشكل صحيح"""
    if not text:
        return ""

    if re.search(r'[\u0600-\u06FF]', text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    return text


# =========================================================
# الخط العربي
# =========================================================

FONT_PATH = "fonts/NotoSansArabic-Regular.ttf"

try:
    LabelBase.register(
        name="Arabic",
        fn_regular=FONT_PATH
    )
    ARABIC_FONT = "Arabic"
except Exception:
    ARABIC_FONT = "Roboto"


# =========================================================
# إعدادات الشاشة
# =========================================================

Window.clearcolor = (0.97, 0.97, 0.97, 1)


# =========================================================
# زر بتصميم مستدير
# =========================================================

class XiaomiButton(Button):

    def __init__(
        self,
        bg_color=(1, 1, 1, 1),
        text_color=(0, 0, 0, 1),
        radius=25,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)

        self.color = text_color
        self.font_size = "22sp"
        self.bold = True

        self.custom_bg = bg_color
        self.radius = radius

        with self.canvas.before:
            self.canvas_color = Color(*self.custom_bg)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# =========================================================
# التطبيق
# =========================================================

class CalculatorApp(App):

    def build(self):
        self.title = fix_text("الحاسبة")

        self.expression = ""
        self.history = []

        # =================================================
        # التخطيط الرئيسي
        # =================================================

        main_layout = BoxLayout(
            orientation="vertical",
            padding=[16, 8, 16, 14],
            spacing=8
        )

        # =================================================
        # الشريط العلوي
        # =================================================

        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.09,
            spacing=5
        )

        menu_button = Button(
            text="⋮",
            font_size="30sp",
            color=(0.2, 0.2, 0.2, 1),
            background_color=(0, 0, 0, 0),
            size_hint_x=0.15
        )

        menu_button.bind(
            on_release=self.show_menu
        )

        calculator_title = Label(
            text=fix_text("الحاسبة"),
            font_name=ARABIC_FONT,
            font_size="22sp",
            color=(0.15, 0.15, 0.15, 1),
            size_hint_x=0.42
        )

        converter_button = Button(
            text=fix_text("المحول"),
            font_name=ARABIC_FONT,
            font_size="20sp",
            color=(0.45, 0.45, 0.45, 1),
            background_color=(0, 0, 0, 0),
            size_hint_x=0.43
        )

        converter_button.bind(
            on_release=self.show_converter_message
        )

        top_bar.add_widget(menu_button)
        top_bar.add_widget(calculator_title)
        top_bar.add_widget(converter_button)

        main_layout.add_widget(top_bar)

        # =================================================
        # شاشة العرض
        # =================================================

        display_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.27,
            padding=[10, 10, 5, 15]
        )

        self.sub_display = Label(
            text="",
            font_name=ARABIC_FONT,
            font_size="18sp",
            color=(0.5, 0.5, 0.5, 1),
            halign="right",
            valign="bottom"
        )

        self.sub_display.bind(
            size=lambda instance, val:
            setattr(instance, 'text_size', val)
        )

        self.main_display = Label(
            text="0",
            font_name=ARABIC_FONT,
            font_size="48sp",
            color=(0, 0, 0, 1),
            bold=True,
            halign="right",
            valign="bottom"
        )

        self.main_display.bind(
            size=lambda instance, val:
            setattr(instance, 'text_size', val)
        )

        display_box.add_widget(self.sub_display)
        display_box.add_widget(self.main_display)

        main_layout.add_widget(display_box)

        # =================================================
        # شبكة الأزرار
        # =================================================

        grid = GridLayout(
            cols=4,
            spacing=12,
            size_hint_y=0.64
        )

        c_white = (1, 1, 1, 1)
        c_gray_btn = (0.94, 0.94, 0.94, 1)
        c_orange = (1, 0.4, 0, 1)
        c_black_text = (0.08, 0.08, 0.08, 1)
        c_orange_text = (1, 0.4, 0, 1)

        buttons = [
            ("AC", c_gray_btn, c_orange_text),
            ("⌫", c_gray_btn, c_orange_text),
            ("%", c_gray_btn, c_orange_text),
            ("÷", c_gray_btn, c_orange_text),

            ("7", c_white, c_black_text),
            ("8", c_white, c_black_text),
            ("9", c_white, c_black_text),
            ("×", c_gray_btn, c_orange_text),

            ("4", c_white, c_black_text),
            ("5", c_white, c_black_text),
            ("6", c_white, c_black_text),
            ("−", c_gray_btn, c_orange_text),

            ("1", c_white, c_black_text),
            ("2", c_white, c_black_text),
            ("3", c_white, c_black_text),
            ("+", c_gray_btn, c_orange_text),

            ("⇄", c_white, c_orange_text),
            ("0", c_white, c_black_text),
            (".", c_white, c_black_text),
            ("=", c_orange, c_white)
        ]

        for text, bg, fg in buttons:
            btn = XiaomiButton(
                text=text,
                bg_color=bg,
                text_color=fg
            )

            btn.bind(
                on_release=self.on_button_press
            )

            grid.add_widget(btn)

        main_layout.add_widget(grid)

        return main_layout

    # =====================================================
    # تحديث الشاشة
    # =====================================================

    def update_display(self):

        if self.expression:
            self.main_display.text = self.expression
        else:
            self.main_display.text = "0"

    # =====================================================
    # الضغط على الأزرار
    # =====================================================

    def on_button_press(self, instance):

        text = instance.text

        if text == "AC":

            self.expression = ""
            self.sub_display.text = ""

        elif text == "⌫":

            self.expression = self.expression[:-1]

        elif text == "=":

            self.calculate()

        elif text == "⇄":

            self.show_converter_message(None)

        elif text == "%":

            self.add_percent()

        else:

            self.add_to_expression(text)

        self.update_display()

    # =====================================================
    # إضافة الأرقام والعمليات
    # =====================================================

    def add_to_expression(self, text):

        operators = "+−×÷"

        if text in operators:

            if not self.expression:
                return

            if self.expression[-1] in operators:
                self.expression = self.expression[:-1]

        if text == ".":

            parts = re.split(
                r"[+−×÷]",
                self.expression
            )

            if parts and "." in parts[-1]:
                return

            if (
                not self.expression
                or self.expression[-1] in operators
            ):
                self.expression += "0"

        self.expression += text

    # =====================================================
    # النسبة المئوية
    # =====================================================

    def add_percent(self):

        if not self.expression:
            return

        match = re.search(
            r"(\d+(?:\.\d+)?)$",
            self.expression
        )

        if match:

            number = match.group(1)

            try:

                value = float(number)
                percent = value / 100

                result = (
                    str(int(percent))
                    if percent.is_integer()
                    else str(percent)
                )

                self.expression = (
                    self.expression[:-len(number)]
                    + result
                )

            except Exception:
                pass

    # =====================================================
    # الحساب
    # =====================================================

    def calculate(self):

        if not self.expression:
            return

        try:

            formatted_expr = (
                self.expression
                .replace("×", "*")
                .replace("÷", "/")
                .replace("−", "-")
            )

            if not re.fullmatch(
                r"[0-9+\-*/(). ]+",
                formatted_expr
            ):
                raise ValueError

            result_value = eval(
                formatted_expr,
                {"__builtins__": None},
                {}
            )

            if isinstance(result_value, float):

                result = (
                    str(int(result_value))
                    if result_value.is_integer()
                    else str(round(result_value, 10))
                )

            else:

                result = str(result_value)

            record = (
                f"{self.expression} = {result}"
            )

            self.history.append(record)

            self.sub_display.text = self.expression

            self.expression = result

        except Exception:

            self.main_display.text = fix_text("خطأ")
            self.expression = ""

    # =====================================================
    # القائمة العلوية ⋮
    # =====================================================

    def show_menu(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        history_button = Button(
            text=fix_text("السجل"),
            font_name=ARABIC_FONT,
            font_size="20sp",
            color=(0.1, 0.1, 0.1, 1),
            background_color=(0.94, 0.94, 0.94, 1)
        )

        clear_button = Button(
            text=fix_text("مسح السجل"),
            font_name=ARABIC_FONT,
            font_size="20sp",
            color=(1, 0.4, 0, 1),
            background_color=(0.94, 0.94, 0.94, 1)
        )

        about_button = Button(
            text=fix_text("حول التطبيق"),
            font_name=ARABIC_FONT,
            font_size="20sp",
            color=(0.1, 0.1, 0.1, 1),
            background_color=(0.94, 0.94, 0.94, 1)
        )

        content.add_widget(history_button)
        content.add_widget(clear_button)
        content.add_widget(about_button)

        popup = Popup(
            title=fix_text("الخيارات"),
            title_font=ARABIC_FONT,
            content=content,
            size_hint=(0.75, 0.40),
            separator_height=1
        )

        history_button.bind(
            on_release=lambda x: (
                popup.dismiss(),
                self.show_history(None)
            )
        )

        clear_button.bind(
            on_release=lambda x: (
                popup.dismiss(),
                self.clear_history()
            )
        )

        about_button.bind(
            on_release=lambda x: (
                popup.dismiss(),
                self.show_about()
            )
        )

        popup.open()

    # =====================================================
    # السجل
    # =====================================================

    def show_history(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        scroll = ScrollView()

        history_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=6
        )

        history_layout.bind(
            minimum_height=history_layout.setter("height")
        )

        if not self.history:

            empty_label = Label(
                text=fix_text("لا يوجد سجل حاليًا"),
                font_name=ARABIC_FONT,
                font_size="18sp",
                color=(0.25, 0.25, 0.25, 1),
                size_hint_y=None,
                height=50
            )

            history_layout.add_widget(empty_label)

        else:

            for item in reversed(self.history):

                lbl = Label(
                    text=fix_text(item),
                    font_name=ARABIC_FONT,
                    font_size="18sp",
                    color=(0.1, 0.1, 0.1, 1),
                    halign="right",
                    valign="middle",
                    size_hint_y=None,
                    height=48
                )

                lbl.bind(
                    size=lambda instance, val:
                    setattr(instance, 'text_size', val)
                )

                history_layout.add_widget(lbl)

        scroll.add_widget(history_layout)

        content.add_widget(scroll)

        bottom_bar = BoxLayout(
            size_hint_y=0.18,
            spacing=8
        )

        clear_button = Button(
            text=fix_text("مسح السجل"),
            font_name=ARABIC_FONT,
            font_size="18sp",
            color=(1, 1, 1, 1),
            background_color=(1, 0.4, 0, 1)
        )

        close_button = Button(
            text=fix_text("إغلاق"),
            font_name=ARABIC_FONT,
            font_size="18sp",
            color=(0.2, 0.2, 0.2, 1),
            background_color=(0.92, 0.92, 0.92, 1)
        )

        bottom_bar.add_widget(clear_button)
        bottom_bar.add_widget(close_button)

        content.add_widget(bottom_bar)

        popup = Popup(
            title=fix_text("سجل العمليات الحسابية"),
            title_font=ARABIC_FONT,
            content=content,
            size_hint=(0.90, 0.70)
        )

        clear_button.bind(
            on_release=lambda x: (
                popup.dismiss(),
                self.clear_history()
            )
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =====================================================
    # مسح السجل
    # =====================================================

    def clear_history(self):

        self.history.clear()

    # =====================================================
    # حول التطبيق
    # =====================================================

    def show_about(self):

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        text = Label(
            text=fix_text(
                "الحاسبة\n\nتطبيق حاسبة بسيط وسريع"
            ),
            font_name=ARABIC_FONT,
            font_size="19sp",
            color=(0.15, 0.15, 0.15, 1),
            halign="center",
            valign="middle"
        )

        close_button = Button(
            text=fix_text("إغلاق"),
            font_name=ARABIC_FONT,
            font_size="18sp",
            size_hint_y=0.25,
            color=(1, 1, 1, 1),
            background_color=(1, 0.4, 0, 1)
        )

        content.add_widget(text)
        content.add_widget(close_button)

        popup = Popup(
            title=fix_text("حول التطبيق"),
            title_font=ARABIC_FONT,
            content=content,
            size_hint=(0.80, 0.45)
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =====================================================
    # المحول
    # =====================================================

    def show_converter_message(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        label = Label(
            text=fix_text(
                "المحول\n\nسيتم إضافة أدوات التحويل لاحقًا"
            ),
            font_name=ARABIC_FONT,
            font_size="19sp",
            color=(0.15, 0.15, 0.15, 1),
            halign="center"
        )

        close_button = Button(
            text=fix_text("إغلاق"),
            font_name=ARABIC_FONT,
            font_size="18sp",
            size_hint_y=0.25,
            color=(1, 1, 1, 1),
            background_color=(1, 0.4, 0, 1)
        )

        content.add_widget(label)
        content.add_widget(close_button)

        popup = Popup(
            title=fix_text("المحول"),
            title_font=ARABIC_FONT,
            content=content,
            size_hint=(0.80, 0.45)
        )

        close_button.bind(
            on_release=popup.dismiss
        )

        popup.open()


# =========================================================
# تشغيل التطبيق
# =========================================================

if __name__ == "__main__":
    CalculatorApp().run()
