class CGPACalculator:
    def __init__(self):
        self.courses = []

    def add_course(self, course_name, gpa, credit):
        if not (0.0 <= gpa <= 4.0):
            print("Error: GPA should be between 0.0 and 4.0.")
            return
        if credit <= 0:
            print("Error: Credit hours should be positive.")
            return
        self.courses.append({"name": course_name, "gpa": gpa, "credit": credit})
        print(f"Course {course_name} added successfully!")

    def calculate_cgpa(self):
        if not self.courses:
            print("No courses added yet. Please add some courses first.")
            return
        total_weighted_gpa = sum(course["gpa"] * course["credit"] for course in self.courses)
        total_credits = sum(course["credit"] for course in self.courses)
        cgpa = total_weighted_gpa / total_credits
        print(f"Your CGPA is: {cgpa:.2f}")

    def show_results(self):
        if not self.courses:
            print("No courses to display.")
            return
        print("Course Results:")
        for course in self.courses:
            print(f"Course: {course['name']} || Credit: {course['credit']} || GPA: {course['gpa']}")


# # Example Usage
# calculator = CGPACalculator()
# calculator.add_course("CSE110", 4.0, 3)
# calculator.add_course("CSE111", 4.0, 3)
# calculator.add_course("CSE370", 3.7, 3)
# calculator.add_course("CSE421", 3.7, 3)
# calculator.add_course("CSE420", 4.0, 4)

# calculator.calculate_cgpa()
# calculator.show_results()
