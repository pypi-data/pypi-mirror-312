class UIComponent:
    def __init__(self, element):
        self.element = element

    def change_style(self, style_dict):
        for key, value in style_dict.items():
            self.element.style[key] = value

    def add_event_listener(self, event_type, callback):
        self.element.addEventListener(event_type, callback)

