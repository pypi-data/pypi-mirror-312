import numpy as np
from dimod import BinaryQuadraticModel
from dwave.samplers import SteepestDescentSampler

#Родительский класс для всех QUBO матриц
class QUBO:
    def __init__(self, matrix=None):
        self.matrix: np.array = matrix
        self.min_energy = None
        self.shape = None if self.matrix is None else self.matrix.shape[0]
        self.raw_solution = None
        self.solution = None
        self.delta = 0

    def set_solution(self):
        self.solution = self.raw_solution

    #Находит минимальное значение x.T @ matrix @ x + delta
    def find_min_energy(self, num_reads=10):
        Q = self.matrix
        n = self.shape

        assert Q is not None, "QUBO is empty!"

        QUBO = {(i, j): Q[i, j] for i in range(n) for j in range(n) if Q[i, j] != 0}

        bqm = BinaryQuadraticModel.from_qubo(QUBO)
        sampler = SteepestDescentSampler()
        sampleset = sampler.sample(bqm, num_reads=num_reads, postprocess='optimization')

        self.min_energy = sampleset.first.energy + self.delta
        self.raw_solution = sampleset.first.sample

        self.set_solution()

        print(f"Min energy: {self.min_energy}")
        return self.min_energy

    def min_energy(self):
        return self.min_energy

    def shape(self):
        return self.shape

    def binary_solution(self):
        return self.solution

    def compute_qubo(self):
        raise NotImplementedError("compute_cubo")


