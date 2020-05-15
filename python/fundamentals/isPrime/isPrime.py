# Spec Output a message of whether a number given is prime
# Input: Number will be inputted into the command line
# The message will say 
#   - The number {number} is prime
#   - The number {number} is not prime
import sys


def get_input_number():
    return int(sys.argv[1])

def is_prime(input_num):
    # prime means only divisible by 1 and itself
    # if any number from 2 to itself - 1 is divisible,
    # ... then then number is not prime
    for i in range(2, input_num):
        is_divisible = input_num % i == 0

        if is_divisible:
            return False

    return True

def print_prime_message(input_num):
    print("The number {0} is prime".format(input_num))

def print_not_prime_message(input_num):
    print("The number {0} is not prime".format(input_num))


def main():
    input_num = get_input_number()

    if is_prime(input_num):
        print_prime_message(input_num)
    else:
        print_not_prime_message(input_num)

main()