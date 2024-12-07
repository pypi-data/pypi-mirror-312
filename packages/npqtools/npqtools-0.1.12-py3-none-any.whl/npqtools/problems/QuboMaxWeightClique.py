import numpy as np
from npqtools.QUBO.qubo import QUBO
from npqtools.problems.PrintGraph import PaintVertexSetInWeightedGraph

class QUBOMaxWeightClique(QUBO) :
    def __init__(self, adjastency_matrix : np.array):
        super().__init__()
        self.adjastency_matrix = adjastency_matrix
        self.adjastency_matrix_size = adjastency_matrix.shape[0]
        self.compute_qubo()

    def change_adjastency_matrix(self) :
        for i in range(self.adjastency_matrix_size) :
            self.adjastency_matrix[i][i] = 0

    def generate_mask(self) -> np.array :
        return np.array([[1 if self.adjastency_matrix[i][j] else 0 for j in range(self.adjastency_matrix_size)] for i in range(self.adjastency_matrix_size)])

    def compute_qubo(self):
        self.shape = self.adjastency_matrix_size
        self.change_adjastency_matrix()
        self.matrix = - self.adjastency_matrix
        mask = self.generate_mask()
        self.matrix += self.adjastency_matrix.sum() * (np.ones(self.matrix.shape) - mask - np.eye(self.matrix.shape[0])).astype(int)
    

    def set_solution(self) -> None:
        self.solution = np.array([key for key, value in self.raw_solution.items() if value])

    
    def display_solution(self) -> None :
        PaintVertexSetInWeightedGraph(self.adjastency_matrix, self.solution)
