"""
Course: CSE 251 
Lesson: L04 Prove
File:   prove.py
Author: Jacob Graham

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Complete the assignments TODO sections and DO NOT edit parts you were told to leave alone.
- Review the full instructions in Canvas; there are a lot of DO NOTS in this lesson.
"""

import time
import threading
import random


# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, semaphore, lock):
        threading.Thread.__init__(self)
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.lock = lock


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            with self.lock:
                car = Car()
                self.car_queue.put(car)
                self.semaphore.release()

        # signal the dealer that there there are not more cars
        self.semaphore.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, semaphore, lock):
        threading.Thread.__init__(self)
        self.car_queue = car_queue
        self.semaphore = semaphore
        self.lock = lock

    def run(self):
        while True:
            # TODO Add your code here
            self.semaphore.acquire()
            with self.lock:
                car = self.car_queue.get()

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    factory_dealer_semaphore = threading.Semaphore(0)
    # TODO Create queue251 
    car_queue = Queue251()
    # TODO Create lock(s) ?
    car_queue_lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory(car_queue, factory_dealer_semaphore, car_queue_lock)
    # TODO create your one dealership
    dealer = Dealer(car_queue, factory_dealer_semaphore, car_queue_lock)

    log.start_timer()

    # TODO Start factory and dealership
    factory.start()
    dealer.start()

    # TODO Wait for factory and dealership to complete
    factory.join()
    dealer.join()
    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]# I'm such a dunce
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production count vs queue size.png')



if __name__ == '__main__':
    main()