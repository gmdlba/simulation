class Simulation:
    def __init__(self, mission_time, executions_number):
        self.executions_number = executions_number  # An integer.
        self.executions = []
        self.results = []  # A list that contains the results. Initialized empty.
        self.mission_time = mission_time
    
    def __str__(self):
        return f"El número de simulaciones son {self.executions_number} y el tiempo de misión es de {self.mission_time} unidades de tiempo"