import unittest

from cgolai.ai import RL
from .util import Hanoi


class TestRL(unittest.TestCase):
    def setUp(self):
        self.mu = .001
        self.inner = [10, 10]
        self.rows = 50
        self.verbose = True  # for debugging
        self.iterations = 2
        self.epsilon_decay_factor = 0.9
        self.epsilon_init = 1.0
        self.problem = Hanoi()

    @staticmethod
    def norm(A):
        total = 0
        for a in A:
            for b in a:
                total += b*b
        return total/len(A)

    def tet_rl_basic(self):
        rl = RL(problem=self.problem, epsilon_decay_factor=self.epsilon_decay_factor, epsilon_init=self.epsilon_init,
                verbose=self.verbose, shape=[None, *self.inner, None])

        rl.train(25, max_steps=1000, iterations=1000)
        steps = 0
        self.problem.reset()
        steps_record = []
        while not self.problem.is_terminal():
            action, _ = rl.choose_best_action(explore=False)
            self.problem.do(action)
            steps += 1
            if steps > 100:
                break
        if self.verbose and steps != 7:
            print(steps)
        self.assertEqual(steps, 7)

