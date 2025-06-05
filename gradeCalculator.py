# Helper function to calculate the grade

def calculate_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

students = []
num_students = 0

while True:
    try:
        num_students = int(input("Enter number of students: "))
        if num_students <= 0:
            raise ValueError("Number must be positive.")
        break
    except ValueError as e:
        print("Invalid input:", e)

for i in range(num_students):
    print(f"\nEnter details for student {i+1}:")
    
    name = input("Name: ")
    
    while True:
        try:
            marks = float(input("Marks (0-100): "))
            if marks < 0 or marks > 100:
                raise ValueError("Marks must be between 0 and 100.")
            break
        except ValueError as e:
            print("Invalid input:", e)

    grade = calculate_grade(marks)
    student_data = {
        "name": name,
        "marks": marks,
        "grade": grade
    }
    students.append(student_data)


print("\nStudent Results:\n")
for student in students:
    print(f"Name: {student['name']}, Marks: {student['marks']}, Grade: {student['grade']}")
