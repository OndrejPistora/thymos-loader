# Test of loader app with Qt and Python

## Python install

requirements: python, git

- install virtual environment

```sh
python -m venv .venv
MAC source .venv/bin/activate
WIN .venv\Scripts\activate.bat
```

- install requrements

```sh
pip install -r requirements.txt
```

- run

```sh
python src/main/python/main.py
```

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

## “ThymosLoader.app” is damaged and can’t be opened. You should move it to the Bin

move it from Applications/ ie to Downloads/

```sh
xattr -rd com.apple.quarantine Downloads/ThymosLoader.app
```

## Pack - dont use now

Convert .ui to .py:

```sh
pyuic6 -o src/ui/design.py src/ui/design.ui
```

Pack to exe

```sh
pyinstaller --noconsole --onefile src/main/python/main.py
```

```sh
pyinstaller --noconsole --onefile --windowed --name="ThymosControl" src/main/python/main.py
```

## pyQT6 designer

cant install PyQt6-tools so doesnt work for me

```sh
pyqt6-tools designer
```