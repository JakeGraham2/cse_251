"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: Jacob Graham

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, pipe_start, marbles, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.pipe_start = pipe_start
        self.marbles = marbles
        self.delay = delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        # Had some help in doing these from a friend
        for i in range(self.marbles):
            marble_color = random.choice(self.colors)
            self.pipe_start.send(marble_color)
            time.sleep(self.delay)
            self.pipe_start.close()
            


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, from_created, marble_bag, to_assembler, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.from_created = from_created
        self.marble_bag = marble_bag
        self.to_assembler = to_assembler
        self.delay = delay
        

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            bag = Bag()
            for i in range(self.marble_bag):
                marble = self.from_created.recv()
                bag.add(marble)
                self.from_created.close()
                self.to_assembler.send(bag)
                self.to_assembler.close()
                time.sleep(self.delay)



class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, marble_set, wrapper, number_gifts, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marble_set = marble_set
        self.wrapper = wrapper
        self.number_gifts = number_gifts
        self.delay = delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag = self.marble_set.recv()
            gift = Gift(random.choice(self.marble_names),bag.items)
            time.sleep(self.delay)
            self.number_gifts.value +=1
            self.wrapper.send(gift)
            self.marble_set.close()
            self.wrapper.close()


class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """
    def __init__(self, from_assembler, filename, delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.from_assembler = from_assembler
        self.filename = filename
        self.delay = delay
        

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, "w") as o:
            while True:
                gift = self.from_assembler.recv()
                o.write(str(gift))
                o.write("\n")
                time.sleep(self.delay)
                o.close()
                self.from_assembler.close()


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    start_creator, end_creator = mp.Pipe()
    start_bagger, end_bagger = mp.Pipe()
    start_assember, end_assembler = mp.Pipe()


    # TODO create variable to be used to count the number of gifts
    number_gifts = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    marble = Marble_Creator(start_creator, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    bagger = Bagger(end_creator, start_bagger, settings[NUMBER_OF_MARBLES_IN_A_BAG], settings[BAGGER_DELAY])
    assembler = Assembler(end_bagger,start_assember,settings[ASSEMBLER_DELAY], number_gifts)
    wrapper = Wrapper(end_assembler,BOXES_FILENAME,settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    # TODO add code here
    marble.start()
    bagger.start()
    assembler.start()
    wrapper.start()


    log.write('Waiting for processes to finish')
    # TODO add code here
    marble.join()
    bagger.join()
    assembler.join()
    wrapper.join()


    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f"Number of Gifts - {number_gifts.value}")

    log.stop_timer(f'Total time')




if __name__ == '__main__':
    main()
