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

# TODO FIX THIS?
TRANSMISSION_DURATION = 90

TP = 512


class Bus:
    def __init__(self, network):
        self.line = network

    def is_line_open(self, src, dest):
        start = src
        end = dest
        if src > dest:
            start = dest
            end = src

        for i in xrange(start, end + 1):
            if self.line[i].is_busy:
                return False

        return True

    def block_line(self, src, dest, tick):
        start = src
        end = dest
        if src > dest:
            start = dest
            end = src

        for i in xrange(start, end + 1):
            self.line[i].is_busy = True
            self.line[i].block_time = tick

    def try_unblock(self, tick):
        for node in self.line:
            if node.is_busy:
                if tick - node.block_time > TRANSMISSION_DURATION:  # transmission time
                    node.is_busy = False


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
        self.transmission_ctr = 0
        self.is_busy = False
        self.random_wait_time = 0
        self.retry_ctr = 0
        self.has_packet = False
        self.dest = None

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
            self.next_arrival = packet_generated
            dest = self.packet_dest()

            self.dest = dest
            self.has_packet = True

        return None

    def backoff(self):
        self.retry_ctr += 1

        # aborting packet
        if self.retry_ctr > 10:
            self.has_packet = False
            self.retry_ctr = 0
            self.dest = None
            return True

        r = random.randint(0, math.pow(2, self.retry_ctr - 1))
        self.random_wait_time = r * TP

        return None


class Simulator:
    def __init__(self, number_computers, packet_rate, speed, packet_length, p):
        self.number_computers = number_computers
        self.packet_rate = packet_rate
        self.speed = speed
        self.packet_length = packet_length
        self.p = p

        # metrics
        self.abort_ctr = 0
        self.collison_ctr = 0
        self.transmitted_ctr = 0

    def _arrival(self, tick):
        pass

    def _departure(self, tick):
        pass

    def _metrics(self, tick):
        pass

    def simulate(self, tick):

        percentage_fraction = tick * TICK_DURATION / 4
        percentage_done = 0

        network = []

        # init network
        for i in xrange(0, self.number_computers):
            network.append(Node(i, self.packet_rate, self.packet_length, self.number_computers))

        bus = Bus(network)

        # sim loop
        for i in xrange(0, tick * TICK_DURATION):

            if i % percentage_fraction == 0:
                print(str(percentage_done) + '% Complete')
                percentage_done += 25

            for node in network:
                if not node.has_packet:

                    # try to generate a packet for this node
                    # sets has_packet = true
                    node.generate(i)
                else:
                    # checking if the bus is busy from src - dest
                    # if blocked prior, check if random wait time is complete
                    if i > node.random_wait_time and node.dest is not None:
                        if bus.is_line_open(node.id, node.dest):
                            network[node.dest].queue.append(i)
                            bus.block_line(node.id, node.dest, i)
                            node.has_packet = False
                            node.dest = None
                            node.retry_ctr = 0
                            self.transmitted_ctr += 1
                        else:
                            # bus is blocked here, add random waits
                            if node.backoff():
                                self.abort_ctr += 1
                            self.collison_ctr += 1
                    else:
                        pass

            bus.try_unblock(i)

        print('100% Complete')

        total_processing_time = 0
        for node in network:
            total_processing_time += sum(node.queue)
            # print node.queue

        throughput = float(self.transmitted_ctr * self.packet_length * 8) / (tick * TICK_DURATION)
        avg_delay = float(total_processing_time) / self.transmitted_ctr

        print "Throughput: {}".format(throughput)
        print "Average Delay: {}".format(avg_delay)
        print "Packets Transmitted: {}".format(self.transmitted_ctr)
        print "Collisions: {}".format(self.collison_ctr)
        print "Dropped: {}".format(self.abort_ctr)


def main(argv):
    ticks = 1

    test_1(ticks)
    test_2(ticks)

def test_1(ticks):
    w = 1000000
    l = 15000

    N1=[20, 40, 60, 80, 100]
    A1=[5,6,7]

    print "----- Running test 1 -----"
    for n in N1:
        for a in A1:
            test = Simulator(n, a, w, l, None)
            print "n = {}, a = {}".format(n, a)
            test.simulate(ticks)
            print ""
    print "----- Finished test 1 -----"


def test_2(ticks):
    w = 1000000
    l = 15000

    A2=[4, 8, 12, 16, 20]
    N2=[20, 30, 40]
    
    print "----- Running test 2 -----"
    for a in A2:
        for n in N2:
            test = Simulator(n, a, w, l, None)
            print "n = {}, a = {}".format(n, a)
            test.simulate(ticks)
            print ""
    print "----- Finished test 2 -----"

if __name__ == "__main__":
    main(sys.argv)

