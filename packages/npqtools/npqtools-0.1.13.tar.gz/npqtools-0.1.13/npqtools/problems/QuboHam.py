from npqtools.qubo import QUBO
from npqtools.problems.PrintGraph import PaintNonOrientatedGraphWithCycle
import numpy as np


class QUBOHam(QUBO):
    def __init__(self, adjastency_matrix):
        super().__init__()
        self.adjastency_matrix = adjastency_matrix
        self.adjastency_matrix_size = adjastency_matrix.shape[0]
        self.compute_qubo()

    #Возвращает гамильтонов путь
    def set_solution(self):
        solution = np.array([key % self.adjastency_matrix_size for key, value in self.raw_solution.items() if value == np.int8(1)])
        self.solution = solution if solution.shape[0] == self.adjastency_matrix_size else None

    def compute_qubo(self):
        self.shape = self.adjastency_matrix_size ** 2

        indices = np.arange(self.shape).reshape(-1, 1)

        mask1 = ((indices // self.adjastency_matrix_size) == (indices.T // self.adjastency_matrix_size)).astype(int) - 2 * np.eye(
            self.shape)
        mask2 = ((indices % self.adjastency_matrix_size) == (indices.T % self.adjastency_matrix_size)).astype(int) - 2 * np.eye(
            self.shape)
        mask3 = ((self.adjastency_matrix[indices // self.adjastency_matrix_size, indices.T // self.adjastency_matrix_size] == 0) & ((
            indices % self.adjastency_matrix_size - indices.T % self.adjastency_matrix_size + 1) % self.adjastency_matrix_size == 0)).astype(
            int)

        self.matrix = mask1 + mask2 + mask3
        self.delta = 2 * self.adjastency_matrix_size

    def display_solution(self):
        PaintNonOrientatedGraphWithCycle(self.adjastency_matrix, self.solution) if self.solution is not None else print("Nothing to show!")
