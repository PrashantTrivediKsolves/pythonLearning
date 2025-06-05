# Error handling in python

# Example 1: Catching an error

# try:
#     x = 10 / 0
# except ZeroDivisionError:
#     print("You can't divide by zero!")



# Example 2: Catching multiple error types


# try:
#     num = int("abc")  # This will cause a ValueError
# except ZeroDivisionError:
#     print("Zero division error.")
# except ValueError:
#     print("Invalid number!")



# ✅ Example 3: Catching all errors (generic)


# try:
#   print("Hello david !!!!")
# try:
#     print(10 / 0)
# except Exception as e:
#     print(f"Error occurred: {e}")


# Optional: else and finally
# else: runs if no error happens

# finally: always runs (good for cleanup)


# try:
#     print("No error here.")
# except:
#     print("Error!")
# else:
#     print("This runs if no error.")
# finally:
#     print("This runs no matter what.")
