class Component:
    def __init__(self, fail_ratio, repair_ratio, state):
        self.fail_ratio = fail_ratio
        self.repair_ratio = repair_ratio
        self.state = state