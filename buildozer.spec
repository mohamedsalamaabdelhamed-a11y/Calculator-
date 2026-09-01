[app]

title = Calculator
package.name = calculator
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 34
android.minapi = 21
android.ndk = 27c
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
