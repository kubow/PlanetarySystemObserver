"""This file is for testing purposes
Usage: just run for now
"""
from context import Master, generate_result_files

if __name__ == '__main__':
    observer = Master()
    
    submit_args = False
    if submit_args:
        generate_result_files()
    else:
        observer.move_head_direction("moon", "pluto")
        print("Sitting in", str(observer.head["location"]), 
              "\nLooking at", observer.head["direction"],
              "\nComputing", observer.head["compute"])
        observer.frame_the_time()
        print(observer.time["frame"])
        
    