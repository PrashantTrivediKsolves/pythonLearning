class Person:
    species = "Human"  # Class variable

    def __init__(self, name):
        self.name = name

    def greet(self):  # Instance method
        print(f"Hello, I'm {self.name}")

    @classmethod
    def show_species(cls):  # Class method
        print("Species:", cls.species)

    @staticmethod
    def is_adult(age):  # Static method
        return age >= 18

class Student(Person):  # Inheritance
    def study(self):
        print(f"{self.name} is studying")

# Using all methods
s = Student("John")
s.greet()               # Instance method
s.study()               # Own instance method
Student.show_species()  # Class method
print(Student.is_adult(20))  # Static method



