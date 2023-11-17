import os
import shutil
from time import sleep

directory_path = 'temp'

def clear_directory():
    while True:
        try:
            # Check if the directory exists
            if os.path.exists(directory_path):
                # Iterate over all items in the directory
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)

                    # Check if it is a file or a directory
                    if os.path.isfile(item_path):
                        # Remove the file
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        # Remove the directory and its contents recursively
                        shutil.rmtree(item_path)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        sleep(30)