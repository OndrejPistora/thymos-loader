import yaml
from pathlib import Path

class Config:
    def __init__(self, path="config.yaml"):
        self.path = Path(path)
        self.data = {}
        self.load()

    def load(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                self.data = yaml.safe_load(f) or {}
        else:
            # Create a new file if it doesn't exist
            print("Config file not found, creating a new one.")
            self.data = {}
            self.save()

    def save(self):
        with open(self.path, "w") as f:
            yaml.dump(self.data, f, default_flow_style=False)

    def get(self, dotted_key, default=None):
        keys = dotted_key.split(".")
        current = self.data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def set(self, dotted_key, value):
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
            self.save()
            self.value_changed.emit(dotted_key, value)

    # ========== Binding Widgets ==========
    # QSpinBox
    # QDoubleSpinBox
    # QCheckBox
    # QLineEdit
    # QTextEdit

    def bind_checkbox(self, checkbox, key, default=False):
        checkbox.setChecked(self.get(key, default))
        checkbox.stateChanged.connect(lambda state: self.set(key, bool(state)))

    def bind_lineedit(self, lineedit, key, default=""):
        """Bind a QLineEdit or QTextEdit to a config key."""
        lineedit.setText(self.get(key, default))
        lineedit.textChanged.connect(lambda text: self.set(key, text))

    def bind_spinbox(self, spinbox, key, default=0):
        """Bind a QSpinBox or QDoubleSpinBox to a config key."""
        spinbox.setValue(self.get(key, default))
        spinbox.valueChanged.connect(lambda val: self.set(key, val))

    # def bind_combobox(self, combobox, key, default_index=0):
    #     index = self.get(key, default_index)
    #     if 0 <= index < combobox.count():
    #         combobox.setCurrentIndex(index)
    #     combobox.currentIndexChanged.connect(lambda i: self.set(key, i))

    # ========== Binding variables ==========
    def bind_variable(self, key, default=None):
        return self.get(key, default)

    def set_variable(self, key, value):
        self.set(key, value)