[app]

title = Calculator

package.name = calculator

package.domain = org.example

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

version = 1.0

requirements = python3,kivy,arabic_reshaper,python-bidi,setuptools

orientation = portrait

fullscreen = 0


# ---------------------------------------------------------
# Android
# ---------------------------------------------------------

android.api = 34

android.minapi = 21

android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

android.enable_androidx = True


# ---------------------------------------------------------
# واجهة التطبيق
# ---------------------------------------------------------

android.presplash_color = #F7F7F7


# ---------------------------------------------------------
# إعدادات Buildozer
# ---------------------------------------------------------

[buildozer]

log_level = 2

warn_on_root = 1
