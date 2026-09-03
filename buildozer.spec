[app]

# (str) Title of your application
title = Calculator

# (str) Package name
package.name = calculator

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (exts found in the project)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

# (list) List of inclusions using pattern matching
source.include_patterns = fonts/*

# (str) Application versioning
version = 1.0

# (list) Application requirements
# تمت إضافة pypdf/typing-extensions أو المكتبات المساندة لضمان استقرار arabic_reshaper و python-bidi
requirements = python3,kivy==2.3.0,arabic_reshaper,python-bidi,setuptools

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0


# ---------------------------------------------------------
# Android Specific Settings
# ---------------------------------------------------------

# (int) Target Android API
android.api = 34

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (bool) Enable AndroidX support
android.enable_androidx = True

# (list) Permissions
# android.permissions = INTERNET


# ---------------------------------------------------------
# UI & Splash Screen
# ---------------------------------------------------------

android.presplash_color = #F7F7F7


# ---------------------------------------------------------
# Buildozer Configuration
# ---------------------------------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
