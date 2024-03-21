import sqlite3

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
class StudentTest:
    def __init__(self, id, student_id, test_id):
        self.id = id
        self.student_id = student_id
        self.test_id = test_id

class Test:
    def __init__(self, id, test_name):
        self.id = id
        self.test_name = test_name

class EvaluationType:
    def __init__(self, id, type):
        self.id = id
        self.type = type

class TestEvaluation:
    def __init__(self, id, test_id, evaluation_type_id):
        self.id = id
        self.test_id = test_id
        self.evaluation_type_id = evaluation_type_id

class StudentTestEvaluation:
    def __init__(self, id, student_id, test_evaluation_id, score = None, comments = None):
        self.id = id
        self.student_id = student_id
        self.test_evaluation_id = test_evaluation_id
        self.score = score # 1, 1.5, 2, 2.5, 3, 3.5, 4
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
    cursor = conn.execute(f'SELECT * FROM tests WHERE id IN (SELECT test_id FROM student_tests WHERE student_id = {student_id})')
    tests = [Test(*row) for row in cursor.fetchall()]

    return tests

# def add_to_evaluations(test_id, evaluation_criteria):
#     conn = sqlite3.connect('druid.db')
#     conn.execute(f"INSERT INTO evaluations (test_id, evaluation_criteria) VALUES ({test_id}, '{evaluation_criteria}')")
#     conn.commit()
#     conn.close()
def add_to_evaluation_types(type):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO evaluation_types (type) VALUES ('{type}')")
    conn.commit()
    conn.close()

def get_evaluation_types():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM evaluation_types')
    evaluation_types = [EvaluationType(*row) for row in cursor.fetchall()]
    conn.close()
    return evaluation_types

def add_test_evaluation_to_test(test_id, evaluation_type_id):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO test_evaluations (test_id, evaluation_type_id) VALUES ({test_id}, {evaluation_type_id})")
    conn.commit()
    conn.close()

def get_all_test_evaluations():
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute('SELECT * FROM test_evaluations')
    test_evaluations = [TestEvaluation(*row) for row in cursor.fetchall()]
    conn.close()
    return test_evaluations


def get_test_evaluations(test_id):

    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f'SELECT * FROM test_evaluations WHERE test_id = {test_id}')
    test_evaluations = [TestEvaluation(*row) for row in cursor.fetchall()]
    conn.close()
    return test_evaluations

def add_test_evaluation_to_student(student_id, test_evaluation_id, score, comments):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO student_test_evaluations (student_id, test_evaluation_id, score, comments) VALUES ({student_id}, {test_evaluation_id}, {score}, '{comments}')")
    conn.commit()
    conn.close()

def get_test_students(test_id):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f'SELECT st.id, st.student_id, st.test_id FROM student_tests st WHERE st.test_id = {test_id}')
    test_students = [StudentTest(*row) for row in cursor.fetchall()]
    conn.close()
    return test_students

## Should also include a test id
def get_student_test_evaluations(student_id, test_id):
    conn = sqlite3.connect('druid.db')
    cursor = conn.execute(f'SELECT ste.id, ste.student_id, ste.test_evaluation_id, ste.score, ste.comments FROM student_test_evaluations ste WHERE ste.student_id = {student_id} AND ste.test_evaluation_id IN (SELECT te.id FROM test_evaluations te WHERE te.test_id = {test_id})')
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

    # Insert sample data into the 'evaluation_types' table
    conn.execute("INSERT INTO evaluation_types (type) VALUES ('Subtraction')")
    conn.execute("INSERT INTO evaluation_types (type) VALUES ('Addition')")
    conn.execute("INSERT INTO evaluation_types (type) VALUES ('Multiplication')")

    # Assuming the IDs for 'tests' and 'evaluation_types' start from 1 and increment
    # Insert sample data into the 'test_evaluations' table
    conn.execute("INSERT INTO test_evaluations (test_id, evaluation_type_id) VALUES (1, 1)")
    conn.execute("INSERT INTO test_evaluations (test_id, evaluation_type_id) VALUES (2, 2)")
    conn.execute("INSERT INTO test_evaluations (test_id, evaluation_type_id) VALUES (3, 3)")

    # Assuming the IDs for students start from 1 and increment
    # Insert sample data into the 'student_tests' table linking students to tests
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (1, 1)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (2, 2)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (3, 3)")

    # Assuming the IDs for 'test_evaluations' start from 1 and increment
    # Insert sample data into the 'student_test_evaluations' table with scores and comments
    conn.execute("INSERT INTO student_test_evaluations (student_id, test_evaluation_id, score, comments) VALUES (1, 1, 3.5, 'Good job')")
    conn.execute("INSERT INTO student_test_evaluations (student_id, test_evaluation_id, score, comments) VALUES (2, 2, 4, 'Excellent')")
    conn.execute("INSERT INTO student_test_evaluations (student_id, test_evaluation_id, score, comments) VALUES (3, 3, 1, 'Needs improvement')")

    conn.commit()


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
    conn.execute('''CREATE TABLE IF NOT EXISTS evaluation_types (
        id INTEGER PRIMARY KEY,
        type VARCHAR(255) NOT NULL
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS test_evaluations (
        id INTEGER PRIMARY KEY,
        test_id INT,
        evaluation_type_id INT,
        FOREIGN KEY (test_id) REFERENCES tests(id),
        FOREIGN KEY (evaluation_type_id) REFERENCES evaluation_types(id)
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_test_evaluations (
        id INTEGER PRIMARY KEY,
        student_id INT,
        test_evaluation_id INT,
        score DECIMAL(5,2),
        comments TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (test_evaluation_id) REFERENCES test_evaluations(id)
    )''')
    # Add more setup code here as necessary
    conn.close()
