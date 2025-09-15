from colorama import Fore, Back, Style, init
init(autoreset=True)

# ---------------- Validation Functions ---------------- #

def is_valid_name(name: str) -> bool:
    return name.replace(" ", "").isalpha()

def is_alphanumeric(s: str) -> bool:
    return s.isalnum()

def is_valid_age(age: str) -> bool:
    return age.isdigit() and 5 <= int(age) <= 100

def is_valid_gender(gender: str) -> bool:
    return gender.lower() in ["male", "female", "other"]

def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email

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


# ---------------- Student Manager ---------------- #

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self):
        print(Fore.CYAN + "\n=== Add Student ===")
        name = input("Enter name: ").strip()
        if not is_valid_name(name):
            print(Fore.RED + " Invalid name! Only letters and spaces allowed.")
            return

        reg_no = input("Enter register number: ").strip()
        if not is_alphanumeric(reg_no):
            print(Fore.RED + " Register number must be alphanumeric!")
            return
        if any(s["reg_no"].lower() == reg_no.lower() for s in self.students):
            print(Fore.RED + " Student with this register number already exists!")
            return

        grade = input("Enter grade/class (1-12): ").strip()
        grade_name = normalize_class_name(grade)
        if not grade_name:
            print(Fore.RED + " Invalid class!")
            return

        age = input("Enter age: ").strip()
        if not is_valid_age(age):
            print(Fore.RED + " Invalid age! (5–100)")
            return

        gender = input("Enter gender (Male/Female/Other): ").strip()
        if not is_valid_gender(gender):
            print(Fore.RED + " Invalid gender!")
            return

        email = input("Enter email: ").strip()
        if not is_valid_email(email):
            print(Fore.RED + " Invalid email!")
            return

        phone = input("Enter phone: ").strip()
        if not is_valid_phone(phone):
            print(Fore.RED + " Invalid phone number!")
            return

        self.students.append({
            "name": name, "reg_no": reg_no, "grade": grade_name,
            "age": age, "gender": gender, "email": email, "phone": phone
        })
        print(Fore.GREEN + f" Student {name} added successfully!")

    def view_students(self):
        print(Fore.CYAN + "\n=== Students List ===")
        if not self.students:
            print(Fore.RED + " No students available.")
            return
        for idx, s in enumerate(self.students, 1):
            print(f"{idx}. {s['name']} ({s['reg_no']}, {s['grade']}, "
                  f"Age: {s['age']}, Gender: {s['gender']}, "
                  f"Email: {s['email']}, Phone: {s['phone']})")

    def search_student(self):
        keyword = input("Enter name or reg no to search: ").strip().lower()
        results = [s for s in self.students if keyword in s["name"].lower() or keyword in s["reg_no"].lower()]
        if results:
            print(Fore.CYAN + "\n Search Results:")
            for s in results:
                print(f"- {s['name']} ({s['reg_no']}, {s['grade']})")
        else:
            print(Fore.RED + " No students found.")

    def remove_student(self):
        reg_no = input("Enter register number to remove: ").strip()
        for s in self.students:
            if s["reg_no"].lower() == reg_no.lower():
                self.students.remove(s)
                print(Fore.GREEN + f"🗑 Student {s['name']} removed.")
                return
        print(Fore.RED + " Student not found.")

    def update_student(self):
        reg_no = input("Enter student register number: ").strip()
        student = next((s for s in self.students if s["reg_no"].lower() == reg_no.lower()), None)
        if not student:
            print(Fore.RED + " Student not found.")
            return

        print("Fields: name, grade, age, gender, email, phone")
        field = input("Enter field to update: ").strip().lower()
        if field not in student:
            print(Fore.RED + " Invalid field.")
            return
        new_value = input(f"Enter new {field}: ").strip()

        # Validate updates
        if field == "name" and not is_valid_name(new_value): return print(Fore.RED + " Invalid name!")
        if field == "grade" and not normalize_class_name(new_value): return print(Fore.RED + " Invalid grade!")
        if field == "age" and not is_valid_age(new_value): return print(Fore.RED + " Invalid age!")
        if field == "gender" and not is_valid_gender(new_value): return print(Fore.RED + " Invalid gender!")
        if field == "email" and not is_valid_email(new_value): return print(Fore.RED + " Invalid email!")
        if field == "phone" and not is_valid_phone(new_value): return print(Fore.RED + " Invalid phone!")

        student[field] = normalize_class_name(new_value) if field == "grade" else new_value
        print(Fore.GREEN + f" Updated {field} for {student['name']}")

    def count_students_per_class(self):
        print(Fore.CYAN + "\n Students per Class:")
        if not self.students:
            print(Fore.YELLOW + " No students.")
            return
        class_map = {}
        for s in self.students:
            class_map[s["grade"]] = class_map.get(s["grade"], 0) + 1
        for grade, count in class_map.items():
            print(f"{grade}: {count} student(s)")

    def list_students_by_class(self):
        grade = input("Enter class: ").strip()
        grade_name = normalize_class_name(grade)
        if not grade_name:
            print(Fore.RED + " Invalid class.")
            return
        students = [s for s in self.students if s["grade"] == grade_name]
        if students:
            print(Fore.CYAN + f"\nStudents in {grade_name}:")
            for s in students:
                print(f"- {s['name']} ({s['reg_no']})")
        else:
            print(Fore.YELLOW + f" No students in {grade_name}.")


# ---------------- Teacher Manager ---------------- #

class TeacherManager:
    DEFAULT_SUBJECTS = ["Tamil", "English", "Maths", "Science", "Social Science", "Computer Science"]

    def __init__(self):
        self.teachers = []
        self.counter = 1

    def add_teacher(self):
        print(Fore.CYAN + "\n=== Add Teacher ===")
        name = input("Enter name: ").strip()
        if not is_valid_name(name):
            print(Fore.RED + " Invalid name!")
            return

        experience = input("Enter years of experience: ").strip()
        if not experience.isdigit():
            print(Fore.RED + " Experience must be numeric.")
            return

        qualification = input("Enter qualification: ").strip()
        if not qualification:
            print(Fore.RED + " Qualification required!")
            return

        teacher = {
            "id": f"T{self.counter:03d}",
            "name": name, "experience": experience,
            "qualification": qualification, "subjects": []
        }
        self.teachers.append(teacher)
        self.counter += 1
        print(Fore.GREEN + f" Teacher {name} added with ID {teacher['id']}")

    def view_teachers(self):
        print(Fore.CYAN + "\n=== Teachers List ===")
        if not self.teachers:
            print(Fore.YELLOW + " No teachers available.")
            return
        for t in self.teachers:
            subjects = ", ".join(t["subjects"]) if t["subjects"] else "None"
            print(f"{t['id']} - {t['name']} (Exp: {t['experience']} yrs, "
                  f"Qualification: {t['qualification']}, Subjects: {subjects})")

    def update_teacher(self):
        tid = input("Enter Teacher ID: ").strip()
        teacher = next((t for t in self.teachers if t["id"].lower() == tid.lower()), None)
        if not teacher:
            print(Fore.RED + " Teacher not found.")
            return
        print("Fields: name, experience, qualification")
        field = input("Enter field to update: ").strip().lower()
        if field not in teacher:
            print(Fore.RED + " Invalid field.")
            return
        new_value = input(f"Enter new {field}: ").strip()
        teacher[field] = new_value
        print(Fore.GREEN + f" Updated {field} for {teacher['name']}")

    def remove_teacher(self):
        tid = input("Enter Teacher ID to remove: ").strip()
        for t in self.teachers:
            if t["id"].lower() == tid.lower():
                self.teachers.remove(t)
                print(Fore.GREEN + f"🗑 Teacher {t['name']} removed.")
                return
        print(Fore.RED + " Teacher not found.")

    def assign_subject(self):
        tid = input("Enter Teacher ID: ").strip()
        teacher = next((t for t in self.teachers if t["id"].lower() == tid.lower()), None)
        if not teacher:
            print(Fore.RED + " Teacher not found.")
            return
        subject = input(f"Enter subject ({', '.join(self.DEFAULT_SUBJECTS)}): ").strip()
        if subject not in self.DEFAULT_SUBJECTS:
            print(Fore.RED + " Invalid subject.")
            return
        if subject in teacher["subjects"]:
            print(Fore.YELLOW + f" {teacher['name']} already teaches {subject}.")
        else:
            teacher["subjects"].append(subject)
            print(Fore.GREEN + f" {subject} assigned to {teacher['name']}.")

    def view_subjects_and_teachers(self):
        print(Fore.CYAN + "\n Subjects and Teachers:")
        for subject in self.DEFAULT_SUBJECTS:
            assigned = [t["name"] for t in self.teachers if subject in t["subjects"]]
            if assigned:
                print(f"{subject}: {', '.join(assigned)}")
            else:
                print(f"{subject}: No teacher assigned")


# ---------------- Main System ---------------- #

class SchoolManagementSystem:
    def __init__(self):
        self.student_manager = StudentManager()
        self.teacher_manager = TeacherManager()

    def main_menu(self):
        while True:
            print(Fore.MAGENTA + "\n===== Main Menu =====")
            print(Fore.LIGHTGREEN_EX+"1. Students")
            print(Fore.LIGHTGREEN_EX + "2. Teachers")
            print(Fore.LIGHTGREEN_EX + "3. Exit")

            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.student_menu()
            elif choice == "2":
                self.teacher_menu()
            elif choice == "3":
                print(Fore.GREEN + " Exiting... Thank you!")
                break
            else:
                print(Fore.RED + " Invalid option!")

    def student_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Student Menu ---")
            print(Fore.LIGHTYELLOW_EX +"1. Add Student")
            print(Fore.LIGHTYELLOW_EX +"2. View Students")
            print(Fore.LIGHTYELLOW_EX +"3. Update Student")
            print(Fore.LIGHTYELLOW_EX +"4. Remove Student")
            print(Fore.LIGHTYELLOW_EX +"5. Search Student")
            print(Fore.LIGHTYELLOW_EX +"6. Count Students per Class")
            print(Fore.LIGHTYELLOW_EX +"7. List Students by Class")
            print(Fore.LIGHTYELLOW_EX +"8. Back")
            choice = input("Enter choice: ").strip()
            if choice == "1": self.student_manager.add_student()
            elif choice == "2": self.student_manager.view_students()
            elif choice == "3": self.student_manager.update_student()
            elif choice == "4": self.student_manager.remove_student()
            elif choice == "5": self.student_manager.search_student()
            elif choice == "6": self.student_manager.count_students_per_class()
            elif choice == "7": self.student_manager.list_students_by_class()
            elif choice == "8": break
            else: print(Fore.RED + " Invalid option!")

    def teacher_menu(self):
        while True:
            print(Fore.BLUE + "\n--- Teacher Menu ---")
            print(Fore.LIGHTBLUE_EX + "1. Add Teacher")
            print(Fore.LIGHTBLUE_EX + "2. View Teachers")
            print(Fore.LIGHTBLUE_EX + "3. Update Teacher")
            print(Fore.LIGHTBLUE_EX + "4. Remove Teacher")
            print(Fore.LIGHTBLUE_EX + "5. Assign Subject")
            print(Fore.LIGHTBLUE_EX + "6. View Subjects and Teachers")
            print(Fore.LIGHTBLUE_EX + "7. Back")
            choice = input("Enter choice: ").strip()
            if choice == "1": self.teacher_manager.add_teacher()
            elif choice == "2": self.teacher_manager.view_teachers()
            elif choice == "3": self.teacher_manager.update_teacher()
            elif choice == "4": self.teacher_manager.remove_teacher()
            elif choice == "5": self.teacher_manager.assign_subject()
            elif choice == "6": self.teacher_manager.view_subjects_and_teachers()
            elif choice == "7": break
            else: print(Fore.RED + "Invalid option!")


# ---------------- Run ---------------- #

print(Fore.GREEN + Back.WHITE + Style.BRIGHT + "===== 🎓 Welcome to School Management System 🎓 =====")
SchoolManagementSystem().main_menu()


