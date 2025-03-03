# Test of loader app with Qt and Python

## Qt designer

<https://build-system.fman.io/qt-designer-download>

pip install pyside6-tools  # For PySide
pyside6-uic your_ui_file.ui -o your_ui_file.py

## realtime graphs

pip install pyqtgraph

## pyserial

pip install pyserial

## FBS

<https://github.com/mherrmann/fbs-tutorial>
fbs startproject

I bought the PRO version
email from <michael@herrmann.io> on 26. 2. 2025 15:52

```sh
pip install fbs_pro-1.2.7.tar.gz
```

## inculde graph in qt desinger

<https://www.pythonguis.com/tutorials/pyside6-embed-pyqtgraph-custom-widgets/>

## Python GUIs

<https://www.pythonguis.com/>

## How to release new version

```sh
bump2version patch
bump2version minor
bump2version major
```

then push to github
