import random
import time


class DsuNode:
    def __init__(self, data, parent=None):
        self.data = data
        self.children = []
        self.parent = parent
        self.rank = 0

    def print(self):
        print("Node Nr. ", self.data)
        if len(self.children) > 0:
            for c in self.children:
                c.print()


class DsuForest:
    # just for testing we keep a list of the roots as well
    forest = []

    # dictionary for fast access to items
    dic = {}

    def __init__(self, items):
        for e in items:
            newnode = DsuNode(e)
            self.dic[e] = newnode
            # uncomment for print
            # self.forest.append(newnode)

    def find(self, elem):
        node = self.dic[elem]
        # save nodes on the way to root for path compression
        path = []
        while node.parent is not None:
            path.append(node)
            node = node.parent
        # compress nodes, i. e. change parent to root
        for n in path:
            n.parent = node
        return node

    def union(self, e1, e2):
        # We allow Union to be called on arbitrary items.
        # Search for the roots and combine trees
        p1 = self.find(e1)
        p2 = self.find(e2)

        if p1 == p2:
            return

        # decide which tree to put under which by comparing ranks
        if p1.rank > p2.rank:
            p1.children.append(p2)
            p2.parent = p1
            # uncomment for print
            # self.delete(p2)

        elif p1.rank < p2.rank:
            p2.children.append(p1)
            p1.parent = p2
            # self.delete(p2)
        else:  # same rank
            p1.children.append(p2)
            p2.parent = p1
            p1.rank += 1
            # self.delete(p2)

    def print(self):
        for node in self.forest:
            node.print()
            print("Tree finished")

    def delete(self, elem):
        i = 0
        length = len(self.forest)
        while i < length:
            if self.forest[i] == elem:
                del (self.forest[i])
                length -= 1
            else:
                i += 1


def test_correctness():
    A = [1, 2, 3, 4, 5, 6, 7]
    forest = DsuForest(A)
    forest.union(5, 7)
    forest.print()
    forest.union(7, 3)
    forest.print()
    forest.union(3, 1)
    forest.print()
    forest.union(6, 4)
    forest.print()
    forest.union(4, 2)
    forest.print()
    forest.union(2, 3)
    forest.print()


def test_speed():
    A = [x for x in range(1000000)]
    random.shuffle(A)

    dsu = DsuForest(A)
    m = 900000

    start = time.time()
    for i in range(m // 2): # 2 finds pro union, also nur die hälfte der aufrufe
        a, b = random.sample(A, 2)
        dsu.union(a, b)

    res = time.time() - start
    print("Unions mixed with finds: ", res)

    start = time.time()
    for i in range(m):
        dsu.find(random.randint(0, 100000 - 1))
    res = time.time() - start

    print("Finds after Unions: ", res)


test_speed()
