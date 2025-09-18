# -------------------- School Management System --------------------
from colorama import Fore, Back, Style, init
from prettytable import PrettyTable
from datetime import datetime

init(autoreset=True)

# -------------------- Helper validation functions --------------------

def is_valid_name(name):
    return bool(name) and name.replace(" ", "").isalpha()

def is_alphanumeric(s):
    return bool(s) and s.isalnum()

def is_valid_age(age_str):
    return age_str.isdigit() and 3 <= int(age_str) <= 120

def is_valid_gender(gender):
    return gender.lower() in ("male", "female", "other")

def is_valid_email(email):
    # simple check
    return "@" in email and "." in email and len(email.strip()) > 5

def is_valid_phone(phone):
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 7 <= len(digits) <= 15

def normalize_class_name(c):
    digits = "".join(ch for ch in c if ch.isdigit())
    if digits.isdigit():
        n = int(digits)
        if 1 <= n <= 12:
            return f"Class {n}"
    return None

def is_valid_weekday(day_str):
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return day_str.capitalize() in valid_days



def header(title):
    print(Fore.MAGENTA + "\n" + "-" * 48)
    print(Fore.MAGENTA + f"  {title}")
    print(Fore.MAGENTA + "-" * 48 + Style.RESET_ALL)

# -------------------- Student Manager --------------------

class StudentManager:
    DEFAULT_SUBJECTS = ["Tamil", "English", "Maths", "Science", "Social Science", "Computer Science"]

    def __init__(self):
        # list of student dicts; key fields: reg_no, name, grade, age, gender, email, phone
        self.students = []

    def get_student(self, reg_no):
        return next((s for s in self.students if s["reg_no"].lower() == reg_no.lower()), None)

    def add_student(self):
        header("Add Student")
        name = input("Name: ").strip()
        if not is_valid_name(name):
            print(Fore.RED + " Invalid name (letters and spaces only).")
            return

        reg_no = input("Register number (alphanumeric): ").strip()
        if not is_alphanumeric(reg_no):
            print(Fore.RED + " Invalid register number (must be alphanumeric).")
            return
        if self.get_student(reg_no):
            print(Fore.RED + " A student with this register number already exists.")
            return

        grade_raw = input("Class (1-12 or 'Class N'): ").strip()
        grade = normalize_class_name(grade_raw)
        if not grade:
            print(Fore.RED + " Invalid class (must be 1..12).")
            return

        age = input("Age: ").strip()
        if not is_valid_age(age):
            print(Fore.RED + " Invalid age. Must be numeric between 3 and 120.")
            return

        gender = input("Gender (Male/Female/Other): ").strip()
        if not is_valid_gender(gender):
            print(Fore.RED + " Invalid gender.")
            return

        email = input("Email: ").strip()
        if not is_valid_email(email):
            print(Fore.RED + " Invalid email.")
            return

        phone = input("Phone: ").strip()
        if not is_valid_phone(phone):
            print(Fore.RED + " Invalid phone.")
            return

        student = {
            "reg_no": reg_no,
            "name": name,
            "grade": grade,
            "age": int(age),
            "gender": gender.title(),
            "email": email,
            "phone": phone
        }
        self.students.append(student)
        print(Fore.GREEN + f" Student '{name}' added to {grade} (Reg: {reg_no}).")

    def view_students(self):
        header("Students List")
        if not self.students:
            print(Fore.YELLOW + "No students found.")
            return
        # default sorted by grade then roll
        sorted_list = sorted(self.students, key=lambda s: (int("".join(ch for ch in s["grade"] if ch.isdigit())), s["reg_no"]))
        for s in sorted_list:
            print(f"{Fore.CYAN}{s['reg_no']}{Style.RESET_ALL} | {s['name']} | {s['grade']} | Age: {s['age']} | {s['gender']} | {s['email']} | {s['phone']}")

    def update_student(self):
        header("Update Student")
        reg_no = input("Enter register number of student to update: ").strip()
        s = self.get_student(reg_no)
        if not s:
            print(Fore.RED + " Student not found.")
            return
        print(Fore.YELLOW + f"Current record: {s}")
        valid_fields = ("name", "grade", "age", "gender", "email", "phone")
        while True:
            print("Which field to update? (name / grade / age / gender / email / phone)")
            field = input("Field: ").strip().lower()
            if field not in valid_fields:
                print(Fore.RED + " Invalid field.")
                continue
            new_val = input(f"Enter new value for {field}: ").strip()
            # validate
            if field == "name":
                if not is_valid_name(new_val):
                    print(Fore.RED + " Invalid name (letters and spaces only).")
                    continue
                s["name"] = new_val
            elif field == "grade":
                norm = normalize_class_name(new_val)
                if not norm:
                    print(Fore.RED + " Invalid class (must be 1..12).")
                    continue
                s["grade"] = norm
            elif field == "age":
                if not is_valid_age(new_val):
                    print(Fore.RED + " Invalid age. Must be numeric between 3 and 120.")
                    continue
                s["age"] = int(new_val)
            elif field == "gender":
                if not is_valid_gender(new_val):
                    print(Fore.RED + " Invalid gender.")
                    continue
                s["gender"] = new_val.title()
            elif field == "email":
                if not is_valid_email(new_val):
                    print(Fore.RED + " Invalid email.")
                    continue
                s["email"] = new_val
            elif field == "phone":
                if not is_valid_phone(new_val):
                    print(Fore.RED + " Invalid phone.")
                    continue
                s["phone"] = new_val
            print(Fore.GREEN + f" Updated {field} for {s['name']}.")
            break

    def remove_student(self):
        header("Remove Student")
        reg_no = input("Enter register number to remove: ").strip()
        s = self.get_student(reg_no)
        if not s:
            print(Fore.RED + " Student not found.")
            return
        confirm = input(Fore.YELLOW + f"Confirm remove {s['name']} (y/N): ").strip().lower()
        if confirm == "y":
            self.students.remove(s)
            print(Fore.GREEN + f" Student {s['name']} removed.")
        else:
            print("Cancelled.")

    def search_student(self):
        header("Search Student")
        kw = input("Enter name or register number to search: ").strip().lower()
        results = [s for s in self.students if kw in s["name"].lower() or kw in s["reg_no"].lower()]
        if not results:
            print(Fore.YELLOW + "No matching students.")
            return
        for s in results:
            print(f"{s['reg_no']} | {s['name']} | {s['grade']}")

    def count_students_per_class(self):
        header("Students per Class")
        summary = {}
        for s in self.students:
            summary[s["grade"]] = summary.get(s["grade"], 0) + 1
        if not summary:
            print(Fore.YELLOW + "No students.")
            return
        for grade in sorted(summary.keys(), key=lambda g: int("".join(ch for ch in g if ch.isdigit()))):
            print(f"{grade}: {summary[grade]} students")

    def list_students_by_class(self):
        header("Students by Class")
        class_input = input("Enter class (1-12 or 'Class N'): ").strip()
        grade = normalize_class_name(class_input)
        if not grade:
            print(Fore.RED + " Invalid class.")
            return
        students = [s for s in self.students if s["grade"] == grade]
        if not students:
            print(Fore.YELLOW + f"No students in {grade}.")
            return
        for s in students:
            print(f"{s['reg_no']} | {s['name']}")

# -------------------- Teacher Manager --------------------

class TeacherManager:
    DEFAULT_SUBJECTS = StudentManager.DEFAULT_SUBJECTS

    def __init__(self):
        self.teachers = []  # dict: id, name, experience, qualifications, subjects(list)
        self._counter = 1

    def get_teacher(self, tid):
        return next((t for t in self.teachers if t["id"].lower() == tid.lower()), None)

    def add_teacher(self):
        header("Add Teacher")
        name = input("Name: ").strip()
        if not is_valid_name(name):
            print(Fore.RED + " Invalid name.")
            return
        experience = input("Experience (years): ").strip()
        if not experience.isdigit():
            print(Fore.RED + " Experience must be numeric.")
            return
        qual = input("Qualifications: ").strip()
        tid = f"T{self._counter:03d}"
        t = {"id": tid, "name": name, "experience": int(experience), "qualifications": qual, "subjects": []}
        self.teachers.append(t)
        self._counter += 1
        print(Fore.GREEN + f" Teacher {name} added with ID {tid}")

    def view_teachers(self):
        header("Teachers List")
        if not self.teachers:
            print(Fore.YELLOW + "No teachers.")
            return
        for t in self.teachers:
            subj = ", ".join(t["subjects"]) if t["subjects"] else "None"
            print(f"{t['id']} | {t['name']} | Exp: {t['experience']} yrs | Qual: {t['qualifications']} | Subjects: {subj}")

    def update_teacher(self):
        header("Update Teacher")
        tid = input("Teacher ID: ").strip()
        t = self.get_teacher(tid)
        if not t:
            print(Fore.RED + " Teacher not found.")
            return
        valid_fields = ("name", "experience", "qualifications")
        while True:
            print("Fields: name, experience, qualifications")
            field = input("Field to update: ").strip().lower()
            if field not in valid_fields:
                print(Fore.RED + " Invalid field.")
                continue
            new = input(f"Enter new {field}: ").strip()
            if field == "name":
                if not is_valid_name(new):
                    print(Fore.RED + " Invalid name.")
                    continue
                t["name"] = new
            elif field == "experience":
                if not new.isdigit():
                    print(Fore.RED + " Experience must be numeric.")
                    continue
                t["experience"] = int(new)
            else:
                t["qualifications"] = new
            print(Fore.GREEN + f" Updated teacher {t['id']}.")
            break

    def remove_teacher(self):
        header("Remove Teacher")
        tid = input("Teacher ID: ").strip()
        t = self.get_teacher(tid)
        if not t:
            print(Fore.RED + " Teacher not found.")
            return
        confirm = input(Fore.YELLOW + f"Confirm remove {t['name']} (y/N): ").strip().lower()
        if confirm == "y":
            self.teachers.remove(t)
            print(Fore.GREEN + f" Teacher {t['name']} removed.")
        else:
            print("Cancelled.")

    def assign_subject(self):
        header("Assign Subject to Teacher")
        tid = input("Teacher ID: ").strip()
        t = self.get_teacher(tid)
        if not t:
            print(Fore.RED + " Teacher not found.")
            return
        print("Available subjects:", ", ".join(self.DEFAULT_SUBJECTS))
        subj = input("Enter subject to assign: ").strip()
        if subj not in self.DEFAULT_SUBJECTS:
            print(Fore.RED + " Invalid subject.")
            return
        if subj in t["subjects"]:
            print(Fore.YELLOW + " Subject already assigned.")
            return
        t["subjects"].append(subj)
        print(Fore.GREEN + f" Assigned {subj} to {t['name']}.")

    def view_subjects_and_teachers(self):
        header("Subjects and Teachers")
        for subject in self.DEFAULT_SUBJECTS:
            assigned = [f"{t['name']} ({t['id']})" for t in self.teachers if subject in t["subjects"]]
            if assigned:
                print(f"{subject}: {', '.join(assigned)}")
            else:
                print(f"{subject}: (none)")

# -------------------- Timetable Manager --------------------

class TimetableManger:
    DEFAULT_SUBJECTS = StudentManager.DEFAULT_SUBJECTS
    def __init__(self):
        self.time_tables = {}  # class_name -> {day: [periods]}
    def add_timetable(self):
        header("Add Timetable")
        class_name = input("Enter class Name (1-12): ")
        class_name = normalize_class_name(class_name)
        if not class_name:
            print("Invalid class")
            return
        days = self.input_weekly_timetable()
        if not days:
            print(Fore.RED + " Timetable creation cancelled or failed.")
            return
        self.time_tables[class_name] = days
        print(Fore.GREEN + f" Timetable for {class_name} added.")

    def input_weekly_timetable(self):
        days = {}
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in weekdays:
            print(Fore.CYAN + f"\nEnter subjects for {day}:")
            periods = []
            for i in range(1, 8):
                subj = input(f"  Period {i}: ").strip()
                if not subj:
                    print(Fore.RED + "  Subject cannot be empty. Try again.")
                    return None
                if subj.lower() not in (s.lower() for s in self.DEFAULT_SUBJECTS):
                    print("Invalid subject!")
                    return 
                periods.append(subj)
            days[day] = periods
        return days
    
    def display_period_table(self):
        table = PrettyTable()
        table.field_names = ["Period", "Timing"]
        # Period timings
        period_times = [
            ("Period 1", "09:15 - 10:00"),
            ("Period 2", "10:00 - 10:45"),
            ("Period 3", "11:00 - 11:45"),
            ("Period 4", "11:45 - 12:30"),
            ("Period 5", "13:45 - 14:30"),
            ("Period 6", "14:30 - 15:15"),
            ("Period 7", "15:30 - 16:15")
        ]
        for period, timing in period_times:
            table.add_row([period, timing])
        print(Fore.YELLOW + "\nPeriod Timings:")
        print(table)
        print(Fore.CYAN + "\nMorning break : 10:45 - 11:00")
        print(Fore.CYAN + "Lunch : 12:30 - 13:45")
        print(Fore.CYAN + "Evening break : 15:15 - 15:30\n")

    def view_timetable(self, class_name=None):
        header("View Timetable")
        self.display_period_table()
        if not self.time_tables:
            print(Fore.YELLOW + "No timetables available.")
            return
        if class_name is None:
            class_name = input("Enter class to view timetable (1-12 or 'Class N'): ").strip()
            class_name = normalize_class_name(class_name)
        if class_name not in self.time_tables:
            print(Fore.RED + f"No timetable found for {class_name}.")
            return
        days = self.time_tables[class_name]
        main_table = PrettyTable()
        main_table.field_names = ["Day"] + [f"Period {i}" for i in range(1, 8)]
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            periods = days.get(day, ["-"]*7)
            main_table.add_row([day] + periods)
        print(Fore.GREEN + f"\nTimetable for {class_name}:")
        print(main_table)

    def edit_timetable(self):
        header("Edit Timetable")
        if not self.time_tables:
            print(Fore.YELLOW + "No timetables available.")
            return
        class_name = input("Enter class name to edit timetable: ").strip()
        class_name = normalize_class_name(class_name)
        if class_name not in self.time_tables:
            print(Fore.RED + f"No timetable found for {class_name}.")
            return
        days = self.time_tables[class_name]
        day = input("Enter the day to edit (Monday-Friday): ").strip().capitalize()
        if day not in days:
            print(Fore.RED + "Invalid day.")
            return
        try:
            period_num = int(input("Enter period number to edit (1-7): ").strip())
            if not (1 <= period_num <= 7):
                raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid period number.")
            return
        print(f"Current subject for {day} Period {period_num}: {days[day][period_num-1]}")
        new_subject = input("Enter new subject: ").strip()
        if not new_subject:
            print(Fore.RED + "Subject cannot be empty.")
            return
        if new_subject.lower() not in (s.lower() for s in self.DEFAULT_SUBJECTS):
            print(Fore.RED + "Invalid subject!")
            return
        days[day][period_num-1] = new_subject
        print(Fore.GREEN + f"Updated {day} Period {period_num} to {new_subject} for {class_name}.")

    def remove_timetable(self):
        header("Remove Timetable")
        if not self.time_tables:
            print(Fore.YELLOW + "No timetables available.")
            return
        class_name = input("Enter class name to remove timetable from: ").strip()
        class_name = normalize_class_name(class_name)
        if class_name not in self.time_tables:
            print(Fore.RED + f"No timetable found for {class_name}.")
            return
        print("1. Remove entire timetable for this class")
        print("2. Remove a specific day's row from this timetable")
        print("3. Empty a day's row (set all periods to '-')")
        print("4. Clear all rows (reset all days, keep columns)")
        choice = input("Enter your choice (1/2/3/4): ").strip()
        if choice == "1":
            confirm = input(f"Are you sure you want to delete the entire timetable for {class_name}? (y/N): ").strip().lower()
            if confirm == "y":
                del self.time_tables[class_name]
                print(Fore.GREEN + f"Timetable for {class_name} deleted.")
            else:
                print("Cancelled.")
        elif choice == "2":
            day = input("Enter the day to remove (Monday-Friday): ").strip().capitalize()
            if day not in self.time_tables[class_name]:
                print(Fore.RED + "Invalid day.")
                return
            confirm = input(f"Are you sure you want to delete {day} from {class_name}'s timetable? (y/N): ").strip().lower()
            if confirm == "y":
                del self.time_tables[class_name][day]
                print(Fore.GREEN + f"{day} removed from {class_name}'s timetable.")
            else:
                print("Cancelled.")
        elif choice == "3":
            day = input("Enter the day to empty (Monday-Friday): ").strip().capitalize()
            if day not in self.time_tables[class_name]:
                print(Fore.RED + "Invalid day.")
                return
            confirm = input(f"Are you sure you want to empty all periods for {day} in {class_name}? (y/N): ").strip().lower()
            if confirm == "y":
                self.time_tables[class_name][day] = ["-"]*7
                print(Fore.GREEN + f"All periods for {day} in {class_name} have been emptied.")
            else:
                print("Cancelled.")
        elif choice == "4":
            confirm = input(f"Are you sure you want to clear all rows for {class_name}? (y/N): ").strip().lower()
            if confirm == "y":
                for day in self.time_tables[class_name]:
                    self.time_tables[class_name][day] = ["-"]*7
                print(Fore.GREEN + f"All rows for {class_name} have been cleared. Columns remain.")
            else:
                print("Cancelled.")
        else:
            print(Fore.RED + "Invalid option.")

# -------------------- Exam Manager --------------------

class ExamManager:
    def __init__(self, student_manager, teacher_manager):
        self.student_manager = student_manager
        self.teacher_manager = teacher_manager
        self.exams = []  # list of dict: id, name, grade, subjects, date
        # marks: nested dict exam_id -> reg_no -> {subject: marks}
        self.marks = {}
        self._counter = 1

    def _generate_eid(self):
        eid = f"E{self._counter:03d}"
        self._counter += 1
        return eid

    def add_exam(self):
        header("Add Exam")
        name = input("Exam name (e.g., Midterm, Final): ").strip()
        if not name:
            print(Fore.RED + " Exam name required.")
            return
        grade_raw = input("Class for exam (1-12): ").strip()
        grade = normalize_class_name(grade_raw)
        if not grade:
            print(Fore.RED + " Invalid class.")
            return
        # choose subjects (comma separated) or "all"
        print("Default subjects:", ", ".join(self.student_manager.DEFAULT_SUBJECTS))
        subj_input = input("Enter subjects (comma-separated) or 'all': ").strip()
        if subj_input.lower() == "all":
            subjects = list(self.student_manager.DEFAULT_SUBJECTS)
        else:
            subjects = [s.strip() for s in subj_input.split(",") if s.strip()]
            # validate subjects
            for s in subjects:
                if s not in self.student_manager.DEFAULT_SUBJECTS:
                    print(Fore.RED + f" Invalid subject: {s}")
                    return
        date = input("Exam date (optional YYYY-MM-DD): ").strip() or datetime.now().strftime("%Y-%m-%d")
        eid = self._generate_eid()
        exam = {"id": eid, "name": name, "grade": grade, "subjects": subjects, "date": date}
        self.exams.append(exam)
        self.marks[eid] = {}  # initialize
        print(Fore.GREEN + f" Exam '{name}' ({eid}) for {grade} created with subjects: {', '.join(subjects)}")

    def list_exams(self):
        header("Exams")
        if not self.exams:
            print(Fore.YELLOW + "No exams defined.")
            return
        for e in self.exams:
            print(f"{e['id']} | {e['name']} | {e['grade']} | {e['date']} | Subjects: {', '.join(e['subjects'])}")

    def enter_marks(self):
        header("Enter Marks for Student")
        if not self.exams:
            print(Fore.YELLOW + "No exams available.")
            return
        self.list_exams()
        eid = input("Enter Exam ID: ").strip()
        exam = next((x for x in self.exams if x["id"].lower() == eid.lower()), None)
        if not exam:
            print(Fore.RED + " Exam not found.")
            return
        reg_no = input("Enter student register number: ").strip()
        student = self.student_manager.get_student(reg_no)
        if not student:
            print(Fore.RED + " Student not found.")
            return
        if student["grade"] != exam["grade"]:
            print(Fore.RED + f" Student {student['name']} is in {student['grade']}, not eligible for {exam['grade']}.")
            return
        # prompt marks for each subject
        sub_marks = {}
        for subj in exam["subjects"]:
            m = input(f"Marks for {subj} (0-100): ").strip()
            if not (m.isdigit() and 0 <= int(m) <= 100):
                print(Fore.RED + f" Invalid marks for {subj}. Must be 0-100.")
                return
            sub_marks[subj] = int(m)
        # store
        self.marks[exam["id"]].setdefault(student["reg_no"], {})
        self.marks[exam["id"]][student["reg_no"]].update(sub_marks)
        print(Fore.GREEN + f" Marks recorded for {student['name']} in exam {exam['id']}.")

    def view_report_card(self):
        header("View Student Report Card")
        reg_no = input("Enter student register number: ").strip()
        student = self.student_manager.get_student(reg_no)
        if not student:
            print(Fore.RED + " Student not found.")
            return
        print(Fore.CYAN + f"Report Card for {student['name']} ({student['reg_no']}) - {student['grade']}")
        found = False
        for exam in self.exams:
            exam_marks_for_student = self.marks.get(exam["id"], {}).get(student["reg_no"], None)
            if exam_marks_for_student:
                found = True
                print(Fore.YELLOW + f"\nExam: {exam['name']} ({exam['id']}) date: {exam['date']}")
                total = 0
                count = 0
                for subj in exam["subjects"]:
                    m = exam_marks_for_student.get(subj, None)
                    if m is None:
                        print(f"  {subj}: -")
                    else:
                        print(f"  {subj}: {m}")
                        total += m
                        count += 1
                if count:
                    avg = total / count
                    grade_letter = self._grade_from_avg(avg)
                    print(Fore.GREEN + f"  Total: {total}  Average: {avg:.2f}  Grade: {grade_letter}")
        if not found:
            print(Fore.YELLOW + "No marks recorded for this student yet.")

    def class_result_summary(self):
        header("Exam / Class Summary")
        if not self.exams:
            print(Fore.YELLOW + "No exams.")
            return
        self.list_exams()
        eid = input("Enter Exam ID for summary: ").strip()
        exam = next((x for x in self.exams if x["id"].lower() == eid.lower()), None)
        if not exam:
            print(Fore.RED + " Exam not found.")
            return
        records = self.marks.get(exam["id"], {})
        if not records:
            print(Fore.YELLOW + "No marks entered for this exam.")
            return
        # for each subject compute avg
        print(Fore.CYAN + f"Summary for {exam['name']} ({exam['id']})")
        subject_averages = {}
        totals = {}
        for reg_no, subdict in records.items():
            total = sum(v for v in subdict.values())
            totals[reg_no] = total
            for subj in exam["subjects"]:
                if subj in subdict:
                    subject_averages.setdefault(subj, []).append(subdict[subj])
        for subj, vals in subject_averages.items():
            avg = sum(vals) / len(vals)
            print(f"  {subj}: avg = {avg:.2f}")
        # class average & toppers
        class_avg = sum(totals.values()) / (len(totals) * len(exam["subjects"]))
        print(Fore.GREEN + f"\nClass average (per subject basis): {class_avg:.2f}")
        sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        print("\nTop performers:")
        for reg_no, tot in sorted_totals[:5]:
            st = self.student_manager.get_student(reg_no)
            name = st["name"] if st else reg_no
            print(f"  {name} ({reg_no}) - Total: {tot}")

    def _grade_from_avg(self, avg):
        if avg >= 90:
            return "A+"
        if avg >= 80:
            return "A"
        if avg >= 70:
            return "B"
        if avg >= 60:
            return "C"
        if avg >= 50:
            return "D"
        return "F"

# -------------------- Fees Manager --------------------

class FeesManager:
    def __init__(self, student_manager):
        self.student_manager = student_manager
        # fee structure: class -> amount (default 10000 if not set)
        self.fee_structure = {}
        # payments: reg_no -> list of payments {amount, date, method}
        self.payments = {}

    def set_fee_for_class(self):
        header("Set Fee for Class")
        cls = input("Enter class (1-12 or 'Class N'): ").strip()
        grade = normalize_class_name(cls)
        if not grade:
            print(Fore.RED + " Invalid class.")
            return
        amt = input("Enter fee amount (numeric): ").strip()
        if not amt.isdigit():
            print(Fore.RED + " Amount must be numeric.")
            return
        self.fee_structure[grade] = int(amt)
        print(Fore.GREEN + f" Fee set for {grade}: {amt}")

    def record_payment(self):
        header("Record Fee Payment")
        reg_no = input("Enter student register number: ").strip()
        student = self.student_manager.get_student(reg_no)
        if not student:
            print(Fore.RED + " Student not found.")
            return
        grade = student["grade"]
        fee_amount = self.fee_structure.get(grade, None)
        if fee_amount is None:
            # default
            fee_amount = 10000
        already_paid = sum(p["amount"] for p in self.payments.get(reg_no, []))
        due = fee_amount - already_paid
        print(Fore.CYAN + f"{student['name']} - {grade} | Fee: {fee_amount} | Paid: {already_paid} | Due: {max(due,0)}")
        amt = input("Enter payment amount: ").strip()
        if not amt.isdigit():
            print(Fore.RED + " Invalid amount.")
            return
        amt = int(amt)
        method = input("Payment method (Cash/Card/Online): ").strip() or "Cash"
        pay = {"amount": amt, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "method": method}
        self.payments.setdefault(reg_no, []).append(pay)
        print(Fore.GREEN + f" Recorded payment of {amt} for {student['name']}.")

    def view_pending_fees(self):
        header("Pending Fees for Student")
        reg_no = input("Enter student register number: ").strip()
        student = self.student_manager.get_student(reg_no)
        if not student:
            print(Fore.RED + " Student not found.")
            return
        grade = student["grade"]
        fee_amount = self.fee_structure.get(grade, 10000)
        paid = sum(p["amount"] for p in self.payments.get(reg_no, []))
        due = fee_amount - paid
        print(Fore.CYAN + f"{student['name']} | Fee: {fee_amount} | Paid: {paid} | Due: {max(due,0)}")

    def view_payment_history(self):
        header("Payment History")
        reg_no = input("Enter student register number: ").strip()
        history = self.payments.get(reg_no, [])
        if not history:
            print(Fore.YELLOW + "No payments found.")
            return
        for p in history:
            print(f"{p['date']} | {p['amount']} | {p['method']}")

    def fee_report_for_class(self):
        header("Fee Report for Class")
        cls = input("Enter class (1-12): ").strip()
        grade = normalize_class_name(cls)
        if not grade:
            print(Fore.RED + " Invalid class.")
            return
        students = [s for s in self.student_manager.students if s["grade"] == grade]
        if not students:
            print(Fore.YELLOW + "No students in this class.")
            return
        fee_amount = self.fee_structure.get(grade, 10000)
        total_due = 0
        total_paid = 0
        for s in students:
            paid = sum(p["amount"] for p in self.payments.get(s["reg_no"], []))
            total_paid += paid
            total_due += max(fee_amount - paid, 0)
        print(Fore.CYAN + f"Class {grade} - Students: {len(students)} | Total Paid: {total_paid} | Total Due: {total_due}")

# -------------------- Main Class --------------------

class SchoolManagementSystem:
    def __init__(self):
        self.student_manager = StudentManager()
        self.teacher_manager = TeacherManager()
        self.timetable_manager = TimetableManger()
        self.exam_manager = ExamManager(self.student_manager, self.teacher_manager)
        self.fees_manager = FeesManager(self.student_manager)

    def main_menu(self):
        while True:
            header("Main Menu")
            print("1. Students")
            print("2. Teachers")
            print("3. Class Timetables")
            print("4. Exams & Results")
            print("5. Fees Management")
            print("6. Exit")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.student_menu()
            elif choice == "2":
                self.teacher_menu()
            elif choice == "3":
                self.timetable_menu()
            elif choice == "4":
                self.exam_menu()
            elif choice == "5":
                self.fees_menu()
            elif choice == "6":
                print(Fore.GREEN + "Exiting, Thank you")
                break
            else:
                print(Fore.RED + " Invalid option.")

    def student_menu(self):
        while True:
            header("Student Menu")
            print("1. Add Student")
            print("2. View Students")
            print("3. Update Student")
            print("4. Remove Student")
            print("5. Search Student")
            print("6. Count Students per Class")
            print("7. List Students by Class")
            print("8. Back")
            choice = input("Choice: ").strip()
            if choice == "1": self.student_manager.add_student()
            elif choice == "2": self.student_manager.view_students()
            elif choice == "3": self.student_manager.update_student()
            elif choice == "4": self.student_manager.remove_student()
            elif choice == "5": self.student_manager.search_student()
            elif choice == "6": self.student_manager.count_students_per_class()
            elif choice == "7": self.student_manager.list_students_by_class()
            elif choice == "8": break
            else: print(Fore.RED + " Invalid option.")

    def teacher_menu(self):
        while True:
            header("Teacher Menu")
            print("1. Add Teacher")
            print("2. View Teachers")
            print("3. Update Teacher")
            print("4. Remove Teacher")
            print("5. Assign Subject")
            print("6. View Subjects & Teachers")
            print("7. Back")
            choice = input("Choice: ").strip()
            if choice == "1": self.teacher_manager.add_teacher()
            elif choice == "2": self.teacher_manager.view_teachers()
            elif choice == "3": self.teacher_manager.update_teacher()
            elif choice == "4": self.teacher_manager.remove_teacher()
            elif choice == "5": self.teacher_manager.assign_subject()
            elif choice == "6": self.teacher_manager.view_subjects_and_teachers()
            elif choice == "7": break
            else: print(Fore.RED + " Invalid option.")

    def timetable_menu(self):
        while True:
            header("Class Timetables")
            print("1. Create Timetable")
            print("2. View Timetable")  
            print("3. Edit Timetable")      
            print("4. Remove Timetables")
            print("5. Back")
            choice = input("Choice: ").strip()
            if choice == "1":
                self.timetable_manager.add_timetable()
            elif choice == "2":
                self.timetable_manager.view_timetable()
            elif choice == "3":
                 self.timetable_manager.edit_timetable()
            elif choice == "4":
                 self.timetable_manager.remove_timetable()
            elif choice == "5":
                break
            else:
                print(Fore.RED + " Invalid option.")

    def exam_menu(self):
        while True:
            header("Exams & Results Menu")
            print("1. Add Exam")
            print("2. List Exams")
            print("3. Enter Marks for Student")
            print("4. View Student Report Card")
            print("5. Exam/Class Summary")
            print("6. Back")
            choice = input("Choice: ").strip()
            if choice == "1": self.exam_manager.add_exam()
            elif choice == "2": self.exam_manager.list_exams()
            elif choice == "3": self.exam_manager.enter_marks()
            elif choice == "4": self.exam_manager.view_report_card()
            elif choice == "5": self.exam_manager.class_result_summary()
            elif choice == "6": break
            else: print(Fore.RED + " Invalid option.")

    def fees_menu(self):
        while True:
            header("Fees Management Menu")
            print("1. Set Fee for Class")
            print("2. Record Payment")
            print("3. View Pending Fees for Student")
            print("4. View Payment History")
            print("5. Fee Report for Class")
            print("6. Back")
            choice = input("Choice: ").strip()
            if choice == "1": self.fees_manager.set_fee_for_class()
            elif choice == "2": self.fees_manager.record_payment()
            elif choice == "3": self.fees_manager.view_pending_fees()
            elif choice == "4": self.fees_manager.view_payment_history()
            elif choice == "5": self.fees_manager.fee_report_for_class()
            elif choice == "6": break
            else: print(Fore.RED + " Invalid option.")

# -------------------- Run --------------------

print(Fore.MAGENTA + "\n" + "=" * 40)
print(Fore.GREEN + Back.WHITE + Style.BRIGHT + "\n Welcome to School Management System" + Style.RESET_ALL)
print(Fore.MAGENTA + "\n" + "=" * 40 + Style.RESET_ALL,end="")
system = SchoolManagementSystem()
system.main_menu()
