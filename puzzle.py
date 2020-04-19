import random
import heapq

#program to solve the slider puzzle with A*-Algorithm
#Heuristic: Manhatten-distance or Hamming-distance between two puzzle-configurations

class puz_node:
    def __init__(self, puz, pred):
        self.puzzle = puz
        self.pred = pred

        if pred is not None:
            self.moves = pred.moves + 1
        else:
            self.moves = 0
        self.prio = self.moves + self.manhatten_dist()

    def __le__(self, other):
        return self.prio <= other.prio

    def __lt__(self, other):
        return self.prio < other.prio

    def print_preds(self):
        self.print_puz()
        print()
        if self.pred is not None:
            self.pred.print_preds()

    def print_puz(self):
        puzzle = self.puzzle
        for i in range(3):
            for j in range(3):
                print(puzzle[i * 3 + j], end=" ")
            print()

    def is_solution(self):
        if self.puzzle[len(self.puzzle) - 1] != 0:
            return False
        puz_zero = self.puzzle[:]
        puz_zero.pop(puz_zero.index(0))

        for i in range(len(puz_zero) - 1):
            if puz_zero[i] > puz_zero[i + 1]:
                return False
        return True

    def is_solvable(self):
        inversions = 0
        for i in range(len(self.puzzle) - 1):
            if self.puzzle[i] == 0:
                continue
            for j in range(i + 1, len(self.puzzle)):
                if self.puzzle[j] == 0:
                    continue
                if self.puzzle[j] < self.puzzle[i]:
                    inversions += 1
        return inversions % 2 == 0

    def is_equal(self, other):
        return self.puzzle == other.puzzle

    def manhatten_dist(self):
        dist = 0
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == 0:
                continue
            dist += mdist(self.puzzle[i] - 1, i)
        return dist

    def hamming_dist(self):
        dist = 0
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == 0:
                continue
            dist += i + 1 != self.puzzle[i]
        return dist

    def test():
        puz1 = puz_node([0, 1, 3, 4, 2, 5, 7, 8, 6], None)
        puz1.print_puz()
        print("hamming dist: ", puz1.hamming_dist())
        print("manhatten dist: ", puz1.manhatten_dist())

        puz2 = puz_node([1, 2, 5, 3, 4, 8, 6, 0, 7], None)
        puz2.print_puz()
        print("hamming dist: ", puz2.hamming_dist())
        print("manhatten dist: ", puz2.manhatten_dist())

    def next_puzzles(self):
        puzzle = self.puzzle
        steps = [-1, 1, -3, 3]
        res = []

        for i in range(len(puzzle)):
            if puzzle[i] == 0:
                break
        for j in steps:
            if j == 1:
                if i + j == 3 or i + j == 6:
                    continue
            elif j == -1:
                if i + j == 2 or i + j == 5:
                    continue

            if i + j >= 0 and i + j <= 8:
                newpuzzle = puzzle[:]  # erzeuge neues Puzzle
                newpuzzle[i + j], newpuzzle[i] = newpuzzle[i], newpuzzle[i + j]  # mit der Verschiebung
                newpuzzle = puz_node(newpuzzle, self)
                if not newpuzzle.is_equal(self):
                    res.append(newpuzzle)

        return res


def mdist(goal, current):
    dist = abs(goal % 3 - current % 3) + abs(goal // 3 - current // 3)
    return dist


def gen_puzzle():
    puzzle = [x for x in range(9)]
    while True:
        random.shuffle(puzzle)
        node = puz_node(puzzle, None)
        if node.is_solvable():
            return node


def simulate():
    start = gen_puzzle()  # [5,7,0,3,4,8,2,6,1],None) # [1,2,5,3,4,8,6,0,7], None)
    queue = []
    queue.append((start))

    while queue:
        current = heapq.heappop(queue)
        if current.is_solution():
            current.print_preds()
            return current

        for puz in current.next_puzzles():
            heapq.heappush(queue, puz)

        # queue[0][2].print_preds()
        # print()


# print(puz_node([5,7,0,3,4,8,2,6,1], None).is_solvable())
simulate()

# puz_node.test()
