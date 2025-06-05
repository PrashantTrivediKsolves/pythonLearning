# list comprehention Demo 


squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]



#  2. Add if condition (even numbers only)
evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]



#  3. Use if-else inside list comprehension

labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
print(labels)  # ['even', 'odd', 'even', 'odd', 'even']





#  4. List of first characters from a list of strings
words = ["apple", "banana", "cherry"]
first_chars = [word[0] for word in words]
print(first_chars)  # ['a', 'b', 'c']



# 🔹 5. Flatten a 2D list

matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6]



# 6. Convert strings to integers

str_nums = ["1", "2", "3"]
int_nums = [int(x) for x in str_nums]
print(int_nums)  # [1, 2, 3]
