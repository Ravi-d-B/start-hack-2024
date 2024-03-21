import sqlite3
import datetime as dt
import pandas as pd

from app.data.competencies import get_compentencies_for_subject_code


class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_evaluations(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM student_test_evaluations WHERE student_id = {self.id}')
        student_test_evaluations = [StudentTestEvaluation(*row) for row in cursor.fetchall()]
        conn.close()
        return student_test_evaluations

    #
    def get_student_graph_data(self):
        conn = sqlite3.connect('druid.db')
        sql_query = """
        SELECT
            st.name as student_name,
            t.date as test_date,
            c.type as competency_type,
            c.code as code,
            t.test_name as test_name,
            AVG(st_e.score) as score
        FROM
            student_test_evaluations st_e
        JOIN
            test_competencies tc ON st_e.test_competency_id = tc.id
        JOIN
            competency_types c ON tc.competency_type_id = c.id
        JOIN
            tests t ON tc.test_id = t.id
        JOIN
            students st ON st_e.student_id = st.id
        WHERE st.id = ?
        GROUP BY
            student_name, test_date, competency_type, code, test_name
        ORDER BY
            st_e.id
        """

        # Execute the query and load the result set into a pandas DataFrame
        df = pd.read_sql_query(sql_query, conn, params=(self.id,))

        # Display the DataFrame to verify its structure
        print(df.head())
        conn.close()
        return df

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
    def __init__(self, id, test_name, date):
        self.id = id
        self.test_name = test_name
        # Parse date string to date object
        self.date = dt.datetime.strptime(date, "%Y-%m-%d").date()


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

    def get_student(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM students WHERE id = {self.student_id}')
        student = Student(*cursor.fetchone())
        conn.close()
        return student
    
    def get_test_competency(self):
        conn = sqlite3.connect('druid.db')
        cursor = conn.execute(f'SELECT * FROM test_competencies WHERE id = {self.test_competency_id}')
        test_competency = TestCompetency(*cursor.fetchone())
        conn.close()
        return test_competency


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


def add_to_tests(test_name, date):
    conn = sqlite3.connect('druid.db')
    conn.execute(f"INSERT INTO tests (test_name, date) VALUES ('{test_name}', '{date.strftime('%Y-%m-%d')}')")
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
    # conn.execute("INSERT INTO tests (test_name, date) VALUES ('Math Test', '2021-01-01')")
    # conn.execute("INSERT INTO tests (test_name, date) VALUES ('Science Test', '2021-01-02')")
    # conn.execute("INSERT INTO tests (test_name, date) VALUES ('History Test', '2021-01-03')")
    conn.execute("INSERT INTO tests (test_name, date) VALUES ('Math Test 1', '2021-01-01')")
    conn.execute("INSERT INTO tests (test_name, date) VALUES ('Science Test 1', '2021-01-02')")
    conn.execute("INSERT INTO tests (test_name, date) VALUES ('History Test 1', '2021-01-03')")
    conn.execute("INSERT INTO tests (test_name, date) VALUES ('Math Test 2', '2021-01-01')")
    conn.execute("INSERT INTO tests (test_name, date) VALUES ('Science Test 2', '2021-01-02')")



    all_competencies = get_compentencies_for_subject_code("")
    for i, competency in all_competencies.iterrows():
        conn.execute(f"INSERT INTO competency_types (type, code) VALUES ('{competency['bezeichnung']}', '{competency['code']}')")

    # Assuming the IDs for 'tests' and 'test_competencies' start from 1 and increment
    # Insert sample data into the 'test_competencies' table
    # conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (1, 1, 'jaahuu')")
    # conn.execute("INSERT INTO test_competencies (test_id, competency_type_id) VALUES (2, 2)")
    # conn.execute("INSERT INTO test_competencies (test_id, competency_type_id) VALUES (3, 3)")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (1, 1, 'Q1,Q2,Q3')")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (2, 2, 'Q1,Q2')")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (3, 3, NULL)")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (4, 1, 'Q4,Q5')")
    conn.execute("INSERT INTO test_competencies (test_id, competency_type_id, questions) VALUES (5, 2, 'Q3,Q4')")


    # Assuming the IDs for students start from 1 and increment
    # Insert sample data into the 'student_tests' table linking students to tests
    # conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (1, 1)")
    # conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (2, 2)")
    # conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (3, 3)")

    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (1, 1)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (2, 2)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (3, 3)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (1, 4)")
    conn.execute("INSERT INTO student_tests (student_id, test_id) VALUES (2, 5)")

    

    # Assuming the IDs for 'test_competencies' start from 1 and increment
    # Insert sample data into the 'student_test_evaluations' table with scores and comments
    # conn.execute(
    #     "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 1, 3.5, 'Good job')")
    # conn.execute(
    #     "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 2, 4, 'Excellent')")
    # conn.execute(
    #     "INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 3, 1, 'Needs improvement')")

    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 1, 3.5, "Good job on Math Test 1")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 2, 4.0, "Excellent work on Science Test 1")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 3, 1.0, "Needs improvement in History")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 4, 4.5, "Outstanding performance on Math Test 2")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 5, 2.5, "Average understanding in Science Test 2")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 1, 2.0, "Satisfactory but could improve")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 2, 3.0, "Decent effort, but needs more practice")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 3, 4.5, "Great understanding of the concepts")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 4, 1.5, "Struggled with advanced topics in Math")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (1, 5, 3.8, "Good, but watch out for tricky questions")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (2, 1, 4.2, "Very good performance overall")')
    conn.execute('INSERT INTO student_test_evaluations (student_id, test_competency_id, score, comments) VALUES (3, 2, 2.3, "Needs to focus more on the basics")')

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
        test_name VARCHAR(255) NOT NULL,
        date DATE NOT NULL
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
