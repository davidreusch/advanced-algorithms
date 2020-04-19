# Höhere Algorithmik, Zettel U10
# Abgabe Reuschenberg, Strobl, Alex
# Implementierung des Viterbi-Algorithmus, test mit mobydick.txt, muss im gleichen Verzeichnis wie Code liegen


from math import log
import random



class viterbi_trainer:
    transitions = {}
    states = {}

    def mogramm_train(self, filepath, amount):
        """read a text and record characters and transition probabilities from character to character"""
        with open(filepath) as f:
            text = f.read(amount)
            count = 0
            for i in range(amount - 1):
                # record all states
                if text[i] not in self.states:
                    self.states[text[i]] = count
                    count += 1

                # record all transitions from one state to another
                if (text[i], text[i + 1]) not in self.transitions:
                    self.transitions[(text[i], text[i + 1])] = 1
                else:
                    self.transitions[(text[i], text[i + 1])] += 1

        # get the probability of a transition, log of it to avoid small numbers
        lgamount = log(amount)
        for (a, b) in self.transitions:
            self.transitions[(a, b)] = log(self.transitions[(a, b)]) - lgamount

        # sort for testing
        self.probabilities = {k: v for k, v in sorted(self.transitions.items(), key=lambda item: item[1], reverse=True)}

        # get the reverse mapping for corrupting the text later
        self.revstates = {v: k for k,v in self.states.items()}

        self.statenum = len(self.states)


    def mogramm_reconstruct(self, filepath, correctness_rate, fromw, to):
        """reconstruct a corrupted text with a corruption_rate"""
        with open(filepath) as f:
            text = f.read()
            text = "".join(self.corrupt(list(text[fromw:to]), correctness_rate))
            print("corrupted text: ")
            print(text)

            # initialize matrix
            # just initialize with very  low probability -> there must be a better way
            self.matrix = [[(-10000000, None) for j in range(len(text))] for i in range(self.statenum)]

            prbegin = -log(len(self.states))
            osamestate = log(correctness_rate)
            ootherstate = -log((len(self.states) - 1)) + log(1 - correctness_rate)

            # base case:
            # fill first column of table
            for q in self.states:
                self.matrix[self.states[q]][0] = (prbegin + osamestate, None) if text[0] == q else (prbegin + ootherstate, None)

            # fill rest of table from left to right
            for j in range(1, len(text)):
                # for each state get max probability that this state occurs under condition of a previous state
                for q in self.states:
                    o = osamestate if q == text[j] else ootherstate
                    self.matrix[self.states[q]][j] = self.getmaxandpos(j, q, o)

            #self.printmatrix()

    def getmaxandpos(self, j, q, o):
        maxim = -1000000, q
        # look at all states from the previous column
        for r in self.states:
            if (r,q) in self.probabilities:
                # this is the recursive case of the formula from class
                # get max prob that a previous state leads to this state now given the symbol that we read
                curval = self.matrix[self.states[r]][j - 1][0] + self.probabilities[(r, q)] + o
                if curval > maxim[0]:
                    maxim = curval, r
        return maxim

    def traceback(self):
        # most likely explanation
        self.MLE = []

        # get max probability of last row
        lastrow = len(self.matrix[0]) - 1
        maxim = self.matrix[0][lastrow]
        for i in range(len(self.matrix)):
            if self.matrix[i][lastrow][0] > maxim[0]:
                maxim = self.matrix[i][lastrow]

        next_sign = maxim[1]
        self.MLE.append(next_sign)

        # just follow the pointers to the prior states in the columns
        for j in range(lastrow - 1, 0, -1):
            next_sign = self.matrix[self.states[next_sign]][j][1]
            self.MLE.append(next_sign)

        self.MLE = self.MLE[::-1]

        print()
        print("#################################################")
        print("############# corrected text: ###################")
        print("#################################################")
        print()
        print("".join(self.MLE))

    def check_correctness(self, fromw, to):
        """compare MLE to actual text"""
        with open("mobydick.txt") as f:
            text = f.read()
            count = 0
            for i in range(fromw, to - 2):
                if text[i] == self.MLE[i - fromw]:
                    count += 1
            count /= to - fromw

            print()
            print("#### correctness rate #####")
            print(count)

    def corrupt(self, textlist, rate):
        """function to change every character of a text by a given probability"""
        for i in range(len(textlist)):
            # change into random state read during training
            if random.random() >= rate:
                textlist[i] = self.revstates[random.randint(0, self.statenum - 1)]
        return textlist

    def printmatrix(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                print(self.matrix[i][j], end=" ")
            print()

trainer = viterbi_trainer()

def test(textfile, trainto, predictfrom, predictto, rate):
    trainer.mogramm_train(textfile, trainto)
    print(trainer.probabilities)
    print(trainer.states)
    trainer.mogramm_reconstruct(textfile, rate, predictfrom, predictto)
    trainer.traceback()
    trainer.check_correctness(predictfrom, predictto)

test("mobydick.txt", 900000, 900000, 905000, 9/10)
