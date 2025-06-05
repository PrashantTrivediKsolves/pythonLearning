import os
import logging

# Configure logging
logging.basicConfig(filename='file_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def walk_directory(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            full_path = os.path.join(root, file)
            logging.info(f"File: {full_path}")
            print(full_path)

if __name__ == '__main__':
    target_directory = './data'  # or any folder
    walk_directory(target_directory)
