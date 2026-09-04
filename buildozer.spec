[app]

# اسم التطبيق
title = Calculator

# اسم الحزمة
package.name = calculator

# نطاق الحزمة
package.domain = org.example

# مجلد المشروع
source.dir = .

# الملفات التي تدخل داخل APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

# مجلد الخطوط
source.include_patterns = fonts/*

# إصدار التطبيق
version = 1.0

# متطلبات Python
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0,arabic-reshaper,python-bidi

# اتجاه الشاشة
orientation = portrait

# ليس ملء الشاشة
fullscreen = 0


# =========================================================
# Android
# =========================================================

# Android API
android.api = 34

# أقل إصدار Android
android.minapi = 21

# NDK المتوافق مع بيئة p4a القديمة
android.ndk = 25b

# المعماريات
android.archs = arm64-v8a,armeabi-v7a

# قبول ترخيص Android SDK
android.accept_sdk_license = True

# AndroidX
android.enable_androidx = True

# لون شاشة البداية
android.presplash_color = #F7F7F7


# =========================================================
# Python-for-Android
# =========================================================

# مهم جداً:
# لا نستخدم أحدث p4a
# نثبت الإصدار الذي كان يستخدم Python 3.11

p4a.url = https://github.com/kivy/python-for-android.git

p4a.branch = master

p4a.commit = v2024.01.21

p4a.bootstrap = sdl2


# =========================================================
# Buildozer
# =========================================================

[buildozer]

log_level = 2

warn_on_root = 1
