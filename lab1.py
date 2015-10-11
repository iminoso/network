"""
Lab 1

Inputs
Tick - Duration of the experiment in units of tick
Lambda - Average number of packets generated/arrived
L - Length of packet in bits
C - Service time by single packet (transmission rate of the output link in bits per second)
K (optional) - Size of buffer, infinite if None

Usage:
python lab1.py Tick Lambda L C K
"""

import math
import sys
import random

# Tick Duration definition
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

        # Calculate the service time required for a single packet
        self._service_time = int(packet_length / float(transmission_rate) * TICK_DURATION)

    # Generate a uniform random number
    def _uniform_rand(self):
        return random.uniform(0, 1)

    # Generate an exponential random number
    def _exponential_rand(self, l):
        return -math.log((1 - self._uniform_rand() / l))

    def _arrival(self, tick):
        # Determine whether a packet is generated based on exponential distribution
        if self._packet_generator(tick):
            # Check if buffer is filled
            if not self._buffer_size or len(self._queue) < self._buffer_size:
                self._queue.append(tick)
            else:
                self._packets_dropped += 1

    def _departure(self, tick):
        # Calculate idle time when queue is empty
        if len(self._queue) == 0:
            self._idle_time += 1
            return True

        self._total_packets_in_queue += len(self._queue)

        if self._service_start_time < 0:
            # begin servicing the packet in the queue
            self._service_start_time = tick

        elif tick > (self._service_start_time + self._service_time):
            # service time is complete, remove packet from queue
            packet_entry_time = self._queue.pop(0)

            # calculate sojurn time
            self._sojurn_time += tick - packet_entry_time

            # add to total packets services
            self._packets_serviced += 1

            # reset the service time for the next packet
            self._service_start_time = -1

    def _packet_generator(self, tick):
        # Generate the next arrive time of a tick based on exponential distribution
        if tick > self._next_arrival_time:
            distribution = self._exponential_rand(self._packet_per_second)
            self._next_arrival_time += int(distribution * TICK_DURATION)
            return True
        else:
            return False

    def _metrics(self, tick):
        # Average number of packets in queue
        E_n = self._total_packets_in_queue / float(tick)

        # Average sojurn time (total time spent by packets in the system)
        E_t = self._sojurn_time / float(self._packets_serviced)

        # Proportion of time the queue is empty
        P_idle = self._idle_time / float(tick) * 100

        # Ratio of loss packets dude to filled queue
        P_loss = self._packets_dropped / (float(self._packets_dropped + self._packets_serviced))

        print('E_n = ' + str(E_n))
        print('E_t = ' + str(E_t))
        print('P_idle = ' + str(P_idle))
        print('P_loss = ' + str(P_loss))

    def simulate(self, tick):
        # Run Simulation
        percentage_fraction = tick * TICK_DURATION / 10
        percentage_done = 0

        print('Service time per packet: ' + str(self._service_time))

        for i in xrange(0, tick * TICK_DURATION):

            if i % percentage_fraction == 0:
                print(str(percentage_done) + '% Complete')
                percentage_done += 10

            self._arrival(i)
            self._departure(i)

        print('100% Complete')

        # Compute metrics after running simulation
        self._metrics(tick * TICK_DURATION)


def main(argv):
    if len(argv) == 5:
        ticks = int(argv[1])
        Lambda = int(argv[2])
        L = int(argv[3])
        C = int(argv[4])

    if len(argv) > 5:
        K = int(argv[5])
    else:
        K = None

    test = Simulator(Lambda, L, C, K)
    test.simulate(ticks)


if __name__ == "__main__":
    main(sys.argv)
