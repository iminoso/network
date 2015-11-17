"""
Lab 2

Inputs
N - Number of computers connected to the LAN (variable)
A - Data packets arrive at the MAC layer following a poisson process with an avg arrival rate of A packets/second
W - speed of LAN (fixed)
L - packet length (fixed)
P (optional) - Persistence parameter for P-persistent

"""

import math
import sys
import random

# Tick Duration definition
TICK_DURATION = 1000000


class Generator:
    def __init__(self, packets_per_second):
        self.packets_per_second = packets_per_second

    # Generate a uniform random number
    def _uniform_rand(self):
        return random.uniform(0, 1)

    # Generate an exponential random number
    def _exponential_rand(self, l):
        return -math.log((1 - self._uniform_rand() / l))

    def generate_packet(self, tick, next_arrival_time):
        if tick > next_arrival_time:
            distribution = self._exponential_rand(self.packets_per_second)
            return next_arrival_time + int(distribution * TICK_DURATION)

        return None


class Node:
    def __init__(self, id, rate, length, num_nodes):
        self.id = id
        self.rate = rate
        self.length = length
        self.num_nodes = num_nodes
        self.next_arrival = 0
        self.queue = []

    def packet_dest(self):
        dest = self.id

        # potential opt
        while dest == self.id:
            dest = random.randint(0, self.num_nodes - 1)

        return dest

    def generate(self, tick):
        gen = Generator(self.rate)
        packet_generated = gen.generate_packet(tick, self.next_arrival)
        if packet_generated:
            self.queue.append(tick)
            self.next_arrival = packet_generated


class Simulator:
    def __init__(self, number_computers, packet_rate, speed, packet_length, p):
        self.number_computers = number_computers
        self.packet_rate = packet_rate
        self.speed = speed
        self.packet_length = packet_length
        self.p = p

    def _arrival(self, tick):
        pass

    def _departure(self, tick):
        pass

    def _metrics(self, tick):
        pass

    def simulate(self, tick):

        percentage_fraction = tick * TICK_DURATION / 10
        percentage_done = 0

        network = []

        # init network
        for i in xrange(0, self.number_computers):
            network.append(Node(i, self.packet_rate, self.packet_length, self.number_computers))

        # sim loop
        for i in xrange(0, tick * TICK_DURATION):

            if i % percentage_fraction == 0:
                print(str(percentage_done) + '% Complete')
                percentage_done += 10

            for node in network:
                node.generate(i)

        print('100% Complete')


def main(argv):
    ticks = 1
    n = 100
    a = 5
    w = 1000000
    l = 15000

    test = Simulator(n, a, w, l, None)
    test.simulate(ticks)


if __name__ == "__main__":
    main(sys.argv)
