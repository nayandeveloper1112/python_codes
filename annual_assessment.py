def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 75:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    else:
        return 'Fail'

def assess_student():
    name = input("Enter child's name: ")
    roll_no = input("Enter roll number: ")

    subjects = ["English", "Math", "Science", "Social Science", "Computer"]
    marks = {}
    total = 0

    print("\nEnter marks out of 100:")
    for subject in subjects:
        while True:
            try:
                score = float(input(f"{subject}: "))
                if 0 <= score <= 100:
                    marks[subject] = score
                    total += score
                    break
                else:
                    print("Enter a valid score between 0 and 100.")
            except ValueError:
                print("Please enter a number.")

    percentage = total / len(subjects)
    grade = calculate_grade(percentage)

    print("\n----- Annual Assessment Report -----")
    print(f"Name       : {name}")
    print(f"Roll No    : {roll_no}")
    print(f"Total Marks: {total}/500")
    print(f"Percentage : {percentage:.2f}%")
    print(f"Grade      : {grade}")
    print("------------------------------------\n")

def main():
    print("===== ANNUAL ASSESSMENT SYSTEM =====\n")
    while True:
        assess_student()
        cont = input("Do you want to assess another student? (y/n): ").lower()
        if cont != 'y':
            print("\nThank you for using the assessment system!")
            break

if __name__ == "__main__":
    main()
