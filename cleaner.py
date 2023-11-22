import os
import shutil
from time import sleep

DIRECTORY_PATH = 'temp'

TIME = 60 * 30  # 30 minutes

def clear_directory():
    while True:
        try:
            # Check if the directory exists
            if os.path.exists(DIRECTORY_PATH):
                # Iterate over all items in the directory
                for item in os.listdir(DIRECTORY_PATH):
                    item_path = os.path.join(DIRECTORY_PATH, item)

                    # Check if it is a file or a directory
                    if os.path.isfile(item_path):
                        # Remove the file
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        # Remove the directory and its contents recursively
                        shutil.rmtree(item_path)
        except Exception as e:
            # Handle error
            print(f"An error occurred: {str(e)}") #TODO: LOG
        
        # Wait
        sleep(TIME)