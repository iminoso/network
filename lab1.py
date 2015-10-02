import random

'''
Inputs
Lambda - Average number of packets generated/arrived
L - Length of packet in bits
C - Service time by packet (transmission rate of the output link in bits per second)
K (optional) - Size of buffer, infinite if None
'''

def main():
    # Define tick duration
    num_of_ticks = 1000000
    for i in range(0, num_of_ticks):
        # TODO: Run simulation in here
        print(i)


if __name__ == "__main__":
    main()
    
