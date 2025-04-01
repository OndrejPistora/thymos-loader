import yaml
from pathlib import Path

class Config:
    def __init__(self, path="config.yaml"):
        self.path = Path(path)
        self.data = {}
        self.load_config()

    def load_config(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                self.data = yaml.safe_load(f) or {}
                # print(self.data)
        else:
            # Create a new file if it doesn't exist
            print("Config file not found, creating a new one.")
            self.data = {}
            self.save_config()

    def save_config(self):
        with open(self.path, "w") as f:
            yaml.dump(self.data, f, default_flow_style=False, sort_keys=False)

    def load(self, dotted_key, default=None):
        keys = dotted_key.split(".")
        current = self.data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def save(self, dotted_key, value):
        keys = dotted_key.split(".")
        current = self.data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        last_key = keys[-1]
        old_value = current.get(last_key)

        if old_value != value:
            current[last_key] = value
            self.save_config()

    # ========== Binding Widgets ==========
    # QSpinBox
    # QDoubleSpinBox
    # QCheckBox
    # QLineEdit
    # QTextEdit

    def bind_checkbox(self, checkbox, key, default=False):
        checkbox.setChecked(self.load(key, default))
        checkbox.stateChanged.connect(lambda state: self.save(key, bool(state)))

    def bind_lineedit(self, lineedit, key, default=""):
        lineedit.setText(self.load(key, default))
        lineedit.editingFinished.connect(lambda: self.save(key, lineedit.text()))

    # text edits need to be promoted to ConfigTextEdit so we have editingFinished event
    def bind_configtextedit(self, textedit, key, default=""):
        textedit.setPlainText(self.load(key, default))
        textedit.editingFinished.connect(lambda: self.save(key, textedit.toPlainText()))
        
    def bind_spinbox(self, spinbox, key, default=0):
        """Bind a QSpinBox or QDoubleSpinBox to a config key."""
        # disable emiting valueChanged signal when setting the value
        spinbox.blockSignals(True)
        spinbox.setValue(self.load(key, default))
        spinbox.blockSignals(False)
        spinbox.valueChanged.connect(lambda val: self.save(key, val))

    # def bind_combobox(self, combobox, key, default_index=0):
    #     index = self.get(key, default_index)
    #     if 0 <= index < combobox.count():
    #         combobox.setCurrentIndex(index)
    #     combobox.currentIndexChanged.connect(lambda i: self.set(key, i))

    # ========== Binding variables ==========
    def bind_variable(self, key, default=None):
        return self.load(key, default)

    def set_variable(self, key, value):
        self.save(key, value)