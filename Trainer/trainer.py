import random
import socket
import time
import subprocess
from strategy import *

mutation_rate = 0.005
crossover_rate = 0.7
pool_size = 100
matchups_per_fitness_calc = 10


def mate(vec1, vec2):
    i = random.randrange(1, len(vec1) - 1)
    return vec1[:i] + vec2[i:]


def mutate(vec):
    indices = sorted([i for i in range(len(vec)) if random.random() < mutation_rate])
    # print("mutation indices" + str(indices))
    if not indices:
        return vec
    out = vec[:indices[0]]
    for i in indices[1:]:
        out += '1' if random.getrandbits(1) else '0'
        out += vec[len(out): i]
    out += vec[len(out):]
    # print(len(vec))
    # print(len(out))
    return out


def rand_vec(size):
    return bin(random.getrandbits(size))[2:].rjust(size, '0')


def xml_for_vecs(vecs):
    s = '<?xml version="1.0" encoding="UTF-8"?><playerCollection>'
    for player in (Strategy(vec) for vec in vecs):
        s += player.xml()
    s += '</playerCollection>'
    return s


class GenAlgTrainer:
    def __init__(self):
        vecs = [rand_vec(N_VECTOR_BITS) for _ in range(pool_size)]
        self.vecs_fitnesses = [(v, 0) for v in vecs]

        address = (socket.gethostname(), 22222)
        success = False
        while not success:
            try:
                self.socketClient = socket.create_connection(address)
                success = True
            except ConnectionRefusedError:
                pass

    def calc_fitnesses(self):
        for _ in range(matchups_per_fitness_calc):
            random.shuffle(self.vecs_fitnesses)
            tested = []
            while len(self.vecs_fitnesses) > 0:
                inprocess = [self.vecs_fitnesses.pop() for _ in range(4)]
                scores = self.run_test([vec for vec, f in inprocess])
                # print("inprocess has %d members" % len(inprocess))
                tested += [(inprocess[i][0], inprocess[i][1] + scores[i]) for i in range(4)]
            self.vecs_fitnesses = tested
        # print([f for v, f in self.vecs_fitnesses])

    def next_generation(self):
        vecs = [vf[0] for vf in self.vecs_fitnesses]
        fitnesses = [vf[1] for vf in self.vecs_fitnesses]
        new_vecs = []
        for i in range(pool_size):
            p1vec = random.choices(vecs, fitnesses)[0]
            if random.random() < crossover_rate:
                p2vec = random.choices(vecs, fitnesses)[0]
                vec = mutate(mate(p1vec, p2vec))
            else:
                vec = mutate(p1vec)
            new_vecs.append(vec)

        self.vecs_fitnesses = [(v, 0) for v in new_vecs]

    def train(self, n_generations):
        for i in range(n_generations):
            self.calc_fitnesses()
            self.next_generation()
            if (i+1) % 10 == 0:
                print("finished generation " + str(i+1))

    def xml(self):
        return xml_for_vecs((v for v, f in self.vecs_fitnesses))

    def run_test(self, vecs):
        if len(vecs) != 4:
            print("Expected 4 vectors for testing")
            return

        # print("running solution tests")
        self.socketClient.send(bytes(xml_for_vecs(vecs) + '\n', "utf-8"))

        r = self.socketClient.recv(64)
        # print(r)
        wins = r.split(b' ')
        if len(wins) != len(vecs):
            print("Error: send/receive lengths %d != %d" % (len(vecs), len(wins)))
            return

        return [int(s) for s in wins]


if __name__ == '__main__':
    # start server
    subprocess.Popen(['C:\\Program Files\\gradle-3.0\\bin\\gradle.bat',
                      '-b', 'C:\\Users\\Evan\\git\\Dominion\\Simulator\\cmdservice.gradle', 'run'],
                     stdout=subprocess.DEVNULL)

    # train strategies
    trainer = GenAlgTrainer()
    trainer.train(1000)

    # display results
    trainer.calc_fitnesses()
    best_vec = max(trainer.vecs_fitnesses, key=lambda vf: vf[1])
    time.sleep(0.1)
    print("most wins of last round: %d out of %d" % (best_vec[1], matchups_per_fitness_calc * 10))
    print(Strategy(best_vec[0]).xml())
