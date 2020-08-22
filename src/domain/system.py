class System_Status():
    def __init__(self, plant_state=None):
        if plant_state is None:
            plant_state = [1, 1, 1]
        self.plant_state = plant_state

    def __str__(self):
        return f"El estado de la planta es {self.plant_state}"