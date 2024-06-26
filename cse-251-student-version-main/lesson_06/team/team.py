"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: Jacob Graham

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(filename, pipe_conn): # Parent
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(filename, 'r') as file:
        for line in file:
            for word in line.split():
                pipe_conn.send(word)
    pipe_conn.close()


def receiver(filename, pipe_conn): # Child
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
with open(filename, 'w') as file:
        while True:
            word = pipe_conn.recv()
            if word:
                file.write(word + ' ')
            else:
                break


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):

     parent_conn, child_conn = mp.Pipe()

    # Create processes for sender and receiver
    sender_process = mp.Process(target=sender, args=(filename1, parent_conn))
    receiver_process = mp.Process(target=receiver, args=(filename2, child_conn))

    log.start_timer()
    start_time = log.get_time()


    # TODO start processes 
    sender_process.start()
    receiver_process.start()
    
    # TODO wait for processes to finish
    sender_process.join()
    receiver_process.join()


    stop_time = log.get_time()

    #log.stop_timer(f'Total time to transfer content = {PUT YOUR VARIABLE HERE}: ')
    #log.write(f'items / second = {PUT YOUR VARIABLE HERE / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')