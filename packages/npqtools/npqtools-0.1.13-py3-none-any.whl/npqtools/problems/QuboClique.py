import numpy as np
from npqtools.qubo import QUBO
from npqtools.problems.PrintGraph import PaintVertexSetInNonWeightedGraph

class QUBOClique(QUBO) :
    def __init__ (self, adjastency_matrix : np.array) :
        super().__init__()
        self.adjastency_matrix = adjastency_matrix
        self.adjastency_matrix_size = adjastency_matrix.shape[0]
        self.compute_qubo()

    def change_adjstency_matrix(self) -> None :
        for i in range(self.adjastency_matrix_size) :
            for j in range(self.adjastency_matrix_size) :
                if self.adjastency_matrix[i][j] :
                    self.adjastency_matrix[i][j] = 1
                if i == j :
                    self.adjastency_matrix[i][j] = 0

    def compute_qubo(self) -> None :
        self.change_adjstency_matrix()
        self.shape = self.adjastency_matrix_size
        self.matrix = np.zeros(self.adjastency_matrix.shape)
        self.matrix -= np.eye(self.adjastency_matrix.shape[0])
        self.matrix += self.adjastency_matrix.sum() * (np.ones(self.adjastency_matrix.shape) - self.adjastency_matrix - np.eye(self.adjastency_matrix.shape[0]))

    def set_solution(self) -> None:
        self.solution = np.array([key for key, value in self.raw_solution.items() if value])

    def display_solution(self) -> None :
        PaintVertexSetInNonWeightedGraph(self.adjastency_matrix, self.solution)

