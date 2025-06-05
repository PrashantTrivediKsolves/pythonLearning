# Example 1: Using lambda with map()


nums = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)  # Output: [2, 4, 6, 8]



#  Example 2: Using lambda with filter()

nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # Output: [2, 4, 6]


# filter() keeps only the items where the lambda returns True.




#  Example 3: Using lambda with sorted()

names = ["Charlie", "Alice", "Bob"]
sorted_names = sorted(names, key=lambda x: len(x))

print(sorted_names) 
print(sorted_names)  # Output: ['Bob', 'Alice', 'Charlie']

# Sorts by length of names.



# Same Logic Using a Named Function Instead of Lambda

def double(x):
    return x * 2

print(list(map(double, [1, 2, 3])))  # [2, 4, 6]

# But lambda is more concise when the function is simple and used only once.



#  sorted() – sort items using custom logic

words = ["apple", "banana", "fig", "grape"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)  # ['fig', 'apple', 'grape', 'banana']

# 🧠 Sorts the list by the length of each word.
    



from functools import reduce

nums = [1, 2, 3, 20]
product = reduce(lambda x , y=4: x *2 , nums)

print("Protocols : ---- \n ----\n ------ \n")
print(product)  # 24






# More Examples:
# 🔢 Sum of all numbers

nums = [10, 20, 30]
total = reduce(lambda x, y: x + y, nums)
print(total)  # Output: 60


# 🧵 Join strings

words = ["Python", "is", "awesome"]
result = reduce(lambda x, y: x + " " + y, words)
print(result)  # Output: "Python is awesome"




# Best example of the Initializer ----------------------------------------------------------------------------------------------


from functools import reduce

result = reduce(lambda x, y: x + y, [1, 2, 3], 10)
print(result)  # Output: 16




# 🧠 reduce(function, iterable, initializer)
# function: a lambda function → lambda x, y: x + y

# iterable: the list → [1, 2, 3]

# initializer: 10



names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 95]
grades = ['B', 'A', 'A+']


# print(tuple(zip(names , scores , grades)))

zipped = list(zip(names, scores, grades))
print(zipped)



# If the lists are not the same length, zip() will stop at the shortest list.


names = ['Alice', 'Bob']
scores = [85, 90, 95]
grades = ['B', 'A', 'A+']

zipped = list(zip(names, scores, grades))
print(zipped)
# Output: [('Alice', 85, 'B'), ('Bob', 90, 'A')]



# Awesome! When your lists are of different lengths and you still want to combine all elements (instead of stopping at the shortest one like zip() does), you can use **itertools.zip_longest**



from itertools import zip_longest

names = ['Alice', 'Bob']
scores = [85, 90, 95]
grades = ['B', 'A', 'A+']

zipped = list(zip_longest(names, scores, grades, fillvalue='N/A'))
print(zipped)
