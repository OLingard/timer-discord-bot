class TimeError(Exception):
    def __init__(self):
        super().__init__("The time argument has to be a whole number.")


class TimeTypeError(Exception):
    def __init__(self):
        super().__init__(f"The time unit is incorrect.")
