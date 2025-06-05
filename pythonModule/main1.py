# main.py

# Import the entire module
import my_utils

result = my_utils.add(5, 3)
print("Addition:", result)

# Access the constant
print("PI:", my_utils.PI)


# Import specific functions
from my_utils import add, subtract

print(add(10, 5))

# Import with an alias

import my_utils as utils

print(utils.subtract(9, 2))



# Use __name__ == "__main__" in modules to write code that only runs when the module is run directly.