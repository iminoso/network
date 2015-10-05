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

TICK_DURATION = 1000000


class Simulator:
    def __init__(self, packet_per_second, packet_length, transmission_rate, buffer_size):
        self._packet_per_second = packet_per_second
        self._packet_length = packet_length
        self._transmission_rate = transmission_rate
        self._buffer_size = buffer_size

        # the buffer queue (infinite in size by default)
        self._queue = []

        # calculate next arrival time of packet
        self._next_arrival_time = 0

        # determine whether to begin service time
        self._service_start_time = -1

        self._idle_time = 0
        self._packets_dropped = 0
        self._total_packets_in_queue = 0
        self._sojurn_time = 0
        self._packets_serviced = 0

        self._service_time = int(packet_length / float(transmission_rate) * TICK_DURATION)
        print(self._service_time)

    def _uniform_rand(self):
        return random.uniform(0, 1)

    def _exponential_rand(self, l):
        return -math.log((1 - self._uniform_rand() / l))

    def _arrival(self, tick):
        if self._packet_generator(tick):
            if not self._buffer_size or len(self._queue) < self._buffer_size:
                self._queue.append(tick)
            else:
                self._packets_dropped += 1

    def _departure(self, tick):
        if len(self._queue) == 0:
            self._idle_time += 1
            return True
        self._total_packets_in_queue += len(self._queue)

        if self._service_start_time < 0:
            self._service_start_time = tick
        else:
            packet_entry_time = self._queue.pop(0)
            self._sojurn_time += tick - packet_entry_time
            self._packets_serviced += 1

    def _metrics(self, tick):
        E_n = self._total_packets_in_queue / float(tick)
        E_t = self._sojurn_time / float(self._packets_serviced)
        P_idle = self._idle_time / float(tick) * 100
        P_loss = self._packets_dropped / (float(self._packets_dropped + self._packets_serviced))
        print('E_n = ' + str(E_n))
        print('E_t = ' + str(E_t))
        print('P_idle = ' + str(P_idle))
        print('P_loss = ' + str(P_loss))

    def _packet_generator(self, tick):
        if tick > self._next_arrival_time:
            distribution = self._exponential_rand(self._packet_per_second)
            tick_duration = TICK_DURATION
            self._next_arrival_time += int(distribution * tick_duration)
            return True
        else:
            return False

    def simulate(self, tick):
        # Run Simulation
        percentage_fraction = tick * TICK_DURATION / 10
        percentage_done = 0

        for i in xrange(0, tick * TICK_DURATION):

            if i % percentage_fraction == 0:
                print(str(percentage_done) + '% Complete')
                percentage_done += 10

            # TODO: Remove this print statement, was used just for testing purposes
            # print(i)

            self._arrival(i)
            self._departure(i)

        print('100% Complete')

        # Compute metrics after running simulation
        self._metrics(tick * TICK_DURATION)


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

    # TODO: Make this take command line arguments later
    test = Simulator(50, 5, 10, 50)
    test.simulate(50)


if __name__ == "__main__":
    main(sys.argv)
