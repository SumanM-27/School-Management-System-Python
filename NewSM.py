""""
School Management System

"""

#Helper functions for validation and normalization
def is_alphanumeric(s: str) -> bool:
    return s.isalnum()

def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email and len(email.strip()) > 5

def is_valid_phone(phone: str) -> bool:
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 7 <= len(digits) <= 15

def normalize_class_name(c: str) -> str | None:
    digits = "".join(ch for ch in c if ch.isdigit())
    if digits.isdigit():
        n = int(digits)
        if 1 <= n <= 12:
            return f"Class {n}"
    return None

#Main School Management 
class SchoolManagementSystem:
    DEFAULT_SUBJECTS = ["Tamil", "English", "Maths", "Science",
        "Social Science", "Computer Science"]
    
    def __init__(self):
        self.__students = []
        self.__teachers = []
        self.__teacher_counter = 1

    #Student Methods
    def add_student(self, name, reg_no, grade, age, gender, email, phone):
        if not is_alphanumeric(reg_no):
            print(" Register number must be alphanumeric.")
            return

        if any(s["register_number"].lower() == reg_no.lower() for s in self.__students):
            print(" Student with this register number already exists!")
            return

        grade_name = normalize_class_name(grade)
        if not grade_name:
            print(" Grade must be between Class 1 and Class 12.")
            return

        if not is_valid_email(email):
            print(" Invalid email format.")
            return
        if not is_valid_phone(phone):
            print(" Invalid phone number.")
            return

        student = {
            "name": name.strip(),
            "register_number": reg_no.strip(),
            "grade": grade_name,
            "age": age.strip(),
            "gender": gender.strip(),
            "email": email.strip(),
            "phone": phone.strip()
        }

        self.__students.append(student)
        print(f" Student '{student['name']}' added successfully!")

    def view_students(self, sort_by="name"):
        if not self.__students:
            print("\n No students added yet!")
            return

        students = self.__students[:]
        if sort_by == "name":
            students.sort(key=lambda x: x["name"].lower())
        elif sort_by == "roll":
            students.sort(key=lambda x: x["register_number"].lower())
        elif sort_by == "class":
            students.sort(key=lambda x: x["grade"])

        print("\n👩‍🎓 Students List:")
        for idx, s in enumerate(students, start=1):
            print(f"{idx}. {s['name']} (Reg No: {s['register_number']}, {s['grade']}, "
                  f"Age: {s['age']}, Gender: {s['gender']}, Email: {s['email']}, Phone: {s['phone']})")

    def search_student(self, keyword):
        keyword = keyword.lower()
        results = [s for s in self.__students if keyword in s["name"].lower() or keyword in s["register_number"].lower()]
        if results:
            print("\n Search Results:")
            for s in results:
                print(f"- {s['name']} (Reg No: {s['register_number']}, {s['grade']})")
        else:
            print(" No students found.")

    def remove_student(self, reg_no):
        for s in self.__students:
            if s["register_number"].lower() == reg_no.lower():
                self.__students.remove(s)
                print(f"🗑 Student '{s['name']}' removed successfully.")
                return
        print(" Student not found.")

    def update_student(self, reg_no, field, new_value):
        for s in self.__students:
            if s["register_number"].lower() == reg_no.lower():
                if field in s:
                    s[field] = new_value.strip()
                    print(f" Updated {field} for student '{s['name']}'.")
                    return
                else:
                    print(" Invalid field.")
                    return
        print(" Student not found.")

    def count_students_per_class(self):
        if not self.__students:
            print("\n No students available.")
            return
        class_map = {}
        for s in self.__students:
            class_map[s["grade"]] = class_map.get(s["grade"], 0) + 1
        print("\n Students per Class:")
        for grade, count in class_map.items():
            print(f"{grade}: {count} student(s)")

    def list_students_by_class(self, grade):
        grade_name = normalize_class_name(grade)
        if not grade_name:
            print(" Invalid class.")
            return
        students = [s for s in self.__students if s["grade"] == grade_name]
        if students:
            print(f"\n Students in {grade_name}:")
            for s in students:
                print(f"- {s['name']} (Reg No: {s['register_number']})")
        else:
            print(f" No students found in {grade_name}.")

    #Teacher Methods
    def add_teacher(self, name, experience, qualification):
        if any(t["name"].lower() == name.strip().lower() for t in self.__teachers):
            print(" Teacher with this name already exists!")
            return

        teacher = {
            "teacher_id": f"T{self.__teacher_counter:03d}",
            "name": name.strip(),
            "experience": experience.strip(),
            "qualification": qualification.strip(),
            "subjects": []
        }

        self.__teachers.append(teacher)
        self.__teacher_counter += 1
        print(f" Teacher '{teacher['name']}' added with ID {teacher['teacher_id']}!")

    def view_teachers(self):
        if not self.__teachers:
            print("\n⚠ No teachers added yet!")
            return
        print("\n Teachers List:")
        for t in self.__teachers:
            subjects = ", ".join(t["subjects"]) if t["subjects"] else "None"
            print(f"{t['teacher_id']} - {t['name']} (Experience: {t['experience']} years, "
                  f"Qualification: {t['qualification']}, Subjects: {subjects})")

    def remove_teacher(self, teacher_id):
        for t in self.__teachers:
            if t["teacher_id"].lower() == teacher_id.lower():
                self.__teachers.remove(t)
                print(f"🗑 Teacher '{t['name']}' removed successfully.")
                return
        print(" Teacher not found.")

    def update_teacher(self, teacher_id, field, new_value):
        for t in self.__teachers:
            if t["teacher_id"].lower() == teacher_id.lower():
                if field in t:
                    t[field] = new_value.strip()
                    print(f"✅ Updated {field} for teacher '{t['name']}'.")
                    return
                else:
                    print(" Invalid field.")
                    return
        print(" Teacher not found.")

    def assign_subject_to_teacher(self, teacher_id, subject):
        if subject not in self.DEFAULT_SUBJECTS:
            print(f" Subject must be one of: {', '.join(self.DEFAULT_SUBJECTS)}")
            return
        for t in self.__teachers:
            if t["teacher_id"].lower() == teacher_id.lower():
                if subject in t["subjects"]:
                    print(f"⚠ {t['name']} already teaches '{subject}'")
                else:
                    t["subjects"].append(subject)
                    print(f"✅ Subject '{subject}' assigned to {t['name']}")
                return
        print(" Teacher not found.")

    def view_subjects_and_teachers(self):
        print("\n Subjects and Teachers:")
        for subject in self.DEFAULT_SUBJECTS:
            assigned_teachers = [t["name"] for t in self.__teachers if subject in t["subjects"]]
            if assigned_teachers:
                print(f"{subject}: {', '.join(assigned_teachers)}")
            else:
                print(f"{subject}: No teacher assigned")
                
    # Simulated save data
    def save_data(self):
        print(" Data saved successfully (simulated).")

    #  Main menu
    def main_menu(self):
        while True:
            print("\n===== Main Menu =====")
            print("1. Add Student")
            print("2. Add Teacher")
            print("3. View Students")
            print("4. View Teachers")
            print("5. View Classes")
            print("6. Search Student")
            print("7. Remove Student")
            print("8. Remove Teacher")
            print("9. Update Student")
            print("10. Update Teacher")
            print("11. Count Students per Class")
            print("12. List Students by Class")
            print("13. Save Data")
            print("14. Assign Subject to Teacher")
            print("15. View Subjects and Teachers")
            print("16. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                name = input("Enter student name: ")
                reg_no = input("Enter register number: ")
                grade = input("Enter grade/class: ")
                age = input("Enter age: ")
                gender = input("Enter gender: ")
                email = input("Enter email: ")
                phone = input("Enter phone: ")
                self.add_student(name, reg_no, grade, age, gender, email, phone)

            elif choice == "2":
                name = input("Enter teacher name: ")
                experience = input("Enter years of experience: ")
                qualification = input("Enter qualification: ")
                self.add_teacher(name, experience, qualification)

            elif choice == "3":
                sort_choice = input("Sort by (name/roll/class): ").strip().lower()
                self.view_students(sort_choice)

            elif choice == "4":
                self.view_teachers()

            elif choice == "5":
                self.count_students_per_class()

            elif choice == "6":
                keyword = input("Enter name or register number to search: ")
                self.search_student(keyword)

            elif choice == "7":
                reg_no = input("Enter register number to remove: ")
                self.remove_student(reg_no)

            elif choice == "8":
                teacher_id = input("Enter Teacher ID to remove: ")
                self.remove_teacher(teacher_id)

            elif choice == "9":
                reg_no = input("Enter student register number: ")
                field = input("Enter field to update (name, grade, age, gender, email, phone): ")
                new_value = input("Enter new value: ")
                self.update_student(reg_no, field, new_value)

            elif choice == "10":
                teacher_id = input("Enter Teacher ID: ")
                field = input("Enter field to update (name, experience, qualification): ")
                new_value = input("Enter new value: ")
                self.update_teacher(teacher_id, field, new_value)

            elif choice == "11":
                self.count_students_per_class()

            elif choice == "12":
                grade = input("Enter grade/class: ")
                self.list_students_by_class(grade)

            elif choice == "13":
                self.save_data()

            elif choice == "14":
                teacher_id = input("Enter Teacher ID: ")
                subject = input("Enter subject to assign: ")
                self.assign_subject_to_teacher(teacher_id, subject)

            elif choice == "15":
                self.view_subjects_and_teachers()

            elif choice == "16":
                print(" Exiting... Thank you!")
                break

            else:
                print(" Invalid choice. Try again!")

print("====> Welcome to SSN School <====")
school=SchoolManagementSystem()
school.main_menu()