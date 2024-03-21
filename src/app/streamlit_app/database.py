import sqlite3
from app.data.competencies import get_compentencies_for_subject_code


class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class StudentTest:
    def __init__(self, id, student_id, test_id):
        self.id = id
        self.student_id = student_id
        self.test_id = test_id

    def get_student(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM students WHERE id = {self.student_id}')
        student = Student(*cursor.fetchone())
        conn.close()
        return student

    def get_test(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM tests WHERE id = {self.test_id}')
        test = Test(*cursor.fetchone())
        conn.close()
        return test

class Test:
    def __init__(self, id, test_name):
        self.id = id
        self.test_name = test_name


class CompetencyType:
    def __init__(self, id, type, code):
        self.id = id
        self.type = type
        self.code = code


class TestCompetency:
    def __init__(self, id, test_id, competency_type_id, questions=None):
        self.id = id
        self.test_id = test_id
        self.competency_type_id = competency_type_id
        self.questions = questions

    def get_competency_type(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM competency_types WHERE id = {self.competency_type_id}')
        competency_type = CompetencyType(*cursor.fetchone())
        conn.close()
        return competency_type


class StudentTestEvaluation:
    def __init__(self, id, student_id, competency_id, score=None, comments=None):
        self.id = id
        self.student_id = student_id
        self.test_competency_id = competency_id
        self.score = score  # 1, 1.5, 2, 2.5, 3, 3.5, 4
        self.comments = comments


def add_to_students(name):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO students (name) VALUES ('{name}')")
    conn.commit()
    conn.close()


def get_students():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM students')
    students = [Student(*row) for row in cursor.fetchall()]
    print(students)
    conn.close()
    return students


def add_to_tests(test_name):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO tests (test_name) VALUES ('{test_name}')")
    conn.commit()
    conn.close()


def get_tests():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM tests')
    tests = [Test(*row) for row in cursor.fetchall()]
    conn.close()
    return tests


def get_test_by_name(test_name):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f"SELECT * FROM tests WHERE test_name = '{test_name}'")
    tests = [Test(*row) for row in cursor.fetchall()]
    test = tests[-1] if tests else None
    conn.close()
    return test


def add_student_to_tests(student_id, test_id):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO student_tests (student_id, test_id) VALUES ({student_id}, {test_id})")
    conn.commit()
    conn.close()


def get_student_tests(student_id):
    # conn = sqlite3.connect('druid.db')
    # cursor = conn.execute(f'SELECT * FROM student_tests WHERE student_id = {student_id}')
    # student_tests = [StudentTest(*row) for row in cursor.fetchall()]
    # conn.close()
    # Should return tests for student not student_tests
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(
        f'SELECT * FROM tests WHERE id IN (SELECT test_id FROM student_tests WHERE student_id = {student_id})')
    tests = [Test(*row) for row in cursor.fetchall()]

    return tests


# def add_to_evaluations(test_id, evaluation_criteria):
#     conn = sqlite3.connect('druid.db')
#     conn.execute(f"INSERT INTO evaluations (test_id, evaluation_criteria) VALUES ({test_id}, '{evaluation_criteria}')")
#     conn.commit()
#     conn.close()
def add_to_competency_types(type):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO competency_types (type) VALUES ('{type}')")
    conn.commit()
    conn.close()


def get_competency_type_by_name(name):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f"SELECT * FROM competency_types WHERE type = '{name}'")
    competency_types = [CompetencyType(*row) for row in cursor.fetchall()]
    competency_type = competency_types[-1] if competency_types else None
    conn.close()
    return competency_type

def get_competency_type_by_code(code):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f"SELECT * FROM competency_types WHERE code = '{code}'")
    competency_types = [CompetencyType(*row) for row in cursor.fetchall()]
    conn.close()
    return competency_types

def get_competency_types():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM competency_types')
    competency_types = [CompetencyType(*row) for row in cursor.fetchall()]
    conn.close()
    return competency_types


def get_all_test_competency_types():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM competency_types')
    competency_types = [CompetencyType(*row) for row in cursor.fetchall()]
    conn.close()
    return competency_types


def add_test_competency_to_test(test_id, competency_type_id, questions=None):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES ({test_id}, {competency_type_id}, '{questions}')")
    conn.commit()
    conn.close()


def get_all_test_competencies():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM test_competencies')
    test_competencies = [TestCompetency(*row) for row in cursor.fetchall()]
    conn.close()
    return test_competencies


def get_test_competencies(test_id):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f'SELECT * FROM test_competencies WHERE test_id = {test_id}')
    test_competencies = [TestCompetency(*row) for row in cursor.fetchall()]
    conn.close()
    return test_competencies


def add_test_evaluation_to_student(student_id, test_competency_id, score, comments):
    conn = sqlite3.connect('druid.db')
    conn.execute(
        f"INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES ({student_id}, {test_competency_id}, {score}, '{comments}')")
    conn.commit()
    conn.close()


def get_test_students(test_id):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f'Select * from students where id in (SELECT student_id FROM student_tests WHERE test_id = {test_id})')
    students = [Student(*row) for row in cursor.fetchall()]
    conn.close()
    return students


## Should also include a test id
def get_student_test_evaluations(student_id, test_id):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(
        f'SELECT ste.id, ste.student_id, ste.test_competency_id, ste.score, ste.comments FROM student_test_evaluations ste WHERE ste.student_id = {student_id} AND ste.test_competency_id IN (SELECT te.id FROM test_competencies te WHERE te.test_id = {test_id})')
    student_test_evaluations = [StudentTestEvaluation(*row) for row in cursor.fetchall()]
    print(student_test_evaluations)
    conn.close()
    return student_test_evaluations


def get_all_student_test_evaluations():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM student_test_evaluations')
    student_test_evaluations = [StudentTestEvaluation(*row) for row in cursor.fetchall()]
    conn.close()
    return student_test_evaluations


def seed_database():
    conn = sqlite3.connect('druid.db')
    # Insert sample data into the 'students' table
    conn.execute("INSERT INTO students (name) VALUES ('Alice')")
    conn.execute("INSERT INTO students (name) VALUES ('Bob')")
    conn.execute("INSERT INTO students (name) VALUES ('Charlie')")

    # Insert sample data into the 'tests' table
    conn.execute("INSERT INTO tests (test_name) VALUES ('Math Test')")
    conn.execute("INSERT INTO tests (test_name) VALUES ('Science Test')")
    conn.execute("INSERT INTO tests (test_name) VALUES ('History Test')")


    all_competencies = get_compentencies_for_subject_code("")[['bezeichnung', 'code']]
    for competency, code in all_competencies:

        conn.execute(f"INSERT INTO competency_types (type, code) VALUES ('{competency}', '{code}')")

    # # Insert sample data into the 'competency_types' table
    conn.execute("INSERT INTO competency_types (type, code) VALUES ('Subtraction', '123')")
    conn.execute("INSERT INTO competency_types (type, code) VALUES ('Addition', '222')")
    conn.execute("INSERT INTO competency_types (type, code) VALUES ('Multiplication', '333')")

    # Assuming the IDs for 'tests' and 'test_competencies' start from 1 and increment
    # Insert sample data into the 'test_competencies' table
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (1, 1, 'jaahuu')")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id) VALUES (2, 2)")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id) VALUES (3, 3)")

    # Assuming the IDs for students start from 1 and increment
    # Insert sample data into the 'student_tests' table linking students to tests
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (1, 1)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (2, 2)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (3, 3)")

    # Assuming the IDs for 'test_competencies' start from 1 and increment
    # Insert sample data into the 'student_test_evaluations' table with scores and comments
    conn.execute(
        "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 1, 3.5, 'Good job')")
    conn.execute(
        "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 2, 4, 'Excellent')")
    conn.execute(
        "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 3, 1, 'Needs improvement')")

    conn.commit()
    conn.close()

def setup_database():
    conn = sqlite3.connect('druid.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY,
        test_name VARCHAR(255) NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_tests (
        id INTEGER PRIMARY KEY,
        student_id INT,
        test_id INT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (test_id) REFERENCES tests(id)
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS competency_types (
        id INTEGER PRIMARY KEY,
        type VARCHAR(255) NOT NULL,
        code VARCHAR(255) NOT NULL
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS test_competencies (
        id INTEGER PRIMARY KEY,
        test_id INT,
        competency_type_id INT,
        questions VARCHAR(255),
        FOREIGN KEY (test_id) REFERENCES tests(id),
        FOREIGN KEY (competency_type_id) REFERENCES competency_types(id)
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_test_evaluations (
        id INTEGER PRIMARY KEY,
        student_id INT,
        test_competency_id INT,
        score DECIMAL(5,2),
        comments TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (test_competency_id) REFERENCES test_competencies(id)
    )''')
    # Add more setup code here as necessary
    conn.close()
