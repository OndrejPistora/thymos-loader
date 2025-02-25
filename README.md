# Thymos Control

## Intro

Software to use Thymos laoding machines.

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

## GUI screenshot

![Thymos Control UI](./GUI.png)

## Pack

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

## ToDo list

- configs saved to YAML file
- view csv
- upload exports to cloud?
- cloud viewers