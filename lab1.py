"""
Lab 1

Inputs
Lambda - Average number of packets generated/arrived
L - Length of packet in bits
C - Service time by packet (transmission rate of the output link in bits per second)
K (optional) - Size of buffer, infinite if None
"""

import math
import sys
import random


class Simulator:
    def __init__(self, packet_per_second, packet_length, transmission_rate, buffer_size):
        self._packet_per_second = packet_per_second
        self._packet_length = packet_length
        self._transmission_rate = transmission_rate
        self._buffer_size = buffer_size

        self._queue = []
        self._next_arrival_time = 0
        self._service_start_time = -1
        self._tick_duration = 1000000

        self._packets_dropped = 0

        self._service_time = int(packet_length / float(transmission_rate) * self._tick_duration)
        print(self._service_time)

    def _uniform_rand(self):
        return random.uniform(0, 1)

    def _exponential_rand(self, l):
        return -math.log((1 - self._uniform_rand() / l))

    def _arrival(self, tick):
        """
        TODO: Handle arrival of tick
        """
        return True

    def _departure(self, tick):
        """
        TODO: Handle departure of tick
        """
        return True

    def _metrics(self):
        """
        TODO: Compute metrics after simulation
        """
        print('Finished Running Metrics')
        return True

    def _packet_generator(self, tick):
        if tick > self._next_arrival_time:
            distribution = self._exponential_rand(self._packet_per_second)
            tick_duration = self._tick_duration
            self._next_arrival_time += int(distribution * tick_duration)
            return True
        else:
            return False

    def simulate(self, tick):
        # Run Simulation
        for i in xrange(0, tick * self._tick_duration):
            print(i)
            if self._packet_generator(i):
                print('Packet Generated ' + str(self._next_arrival_time))
            self._arrival(i)
            self._departure(i)

        # Compute metrics after running simulation
        self._metrics()


def main(argv):
    """
    TODO: Pass python arguments to simulator, hard coded at the moment

    if len(argv) == 5:
        ticks = argv[1]
        Lambda = argv[2]
        L = argv[3]
        C = argv[4]

    if len(argv) > 5:
        K = argv[5]
    else:
        K = None
    """

    test = Simulator(5000, 5, 10, 50)
    test.simulate(5000)


if __name__ == "__main__":
    main(sys.argv)
