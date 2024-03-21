import streamlit as st
from database import setup_database, get_students, add_to_students, add_to_evaluation_types, get_evaluation_types, add_to_tests, get_tests, add_test_evaluation_to_test, get_test_evaluations, get_all_test_evaluations, add_student_to_tests, add_test_evaluation_to_student, get_student_tests, get_student_test_evaluations, get_all_student_test_evaluations

def main():
    setup_database()
    st.write("Add student:")
    # Student name input and call to add_to_students after button click
    student_name = st.text_input("Enter student name")
    if st.button("Add student"):
        add_to_students(student_name)
        st.success(f"Student {student_name} added successfully!")

    st.write("Students:")
    students = get_students()
    for student in students:
        # Show id and name
        st.write(student.id, student.name)
        # Show student's tests
        student_tests = get_student_tests(student.id)
        for student_test in student_tests:

            st.write(student_test.id, student_test.test_name)
            #Write test evaluations
            test_evaluations = get_student_test_evaluations(student.id, student_test.id)
            for test_evaluation in test_evaluations:
                st.write('Student test evaluation', test_evaluation.id, "Evaluation id:", test_evaluation.test_evaluation_id, "Score:", test_evaluation.score, "Comments:", test_evaluation.comments)

    st.write("Add evaluation type:")
    evaluation_type = st.text_input("Enter evaluation type")
    if st.button("Add evaluation type"):
        add_to_evaluation_types(evaluation_type)
        st.success(f"Evaluation type {evaluation_type} added successfully!")

    st.write("Evaluation types:")
    evaluation_types = get_evaluation_types()
    for evaluation_type in evaluation_types:
        st.write(evaluation_type.id, evaluation_type.type)

    st.write("Add test:")
    # Test name input and call to add_to_tests after button click
    test_name = st.text_input("Enter test name")
    if st.button("Add test"):
        add_to_tests(test_name)
        st.success(f"Test {test_name} added successfully!")

    st.write("Tests:")
    tests = get_tests()
    for test in tests:
        st.write(test.id, test.test_name)
        # Show test evaluations
        test_evaluations = get_test_evaluations(test.id)
        for test_evaluation in test_evaluations:
            st.write('Test id:', test_evaluation.test_id, "Evaluation id:", test_evaluation.evaluation_type_id)

    st.write("Add test evaluation to test:")
    test_id = st.text_input("Enter test id")
    evaluation_type_id = st.text_input("Enter evaluation type id")
    if st.button("Add test evaluation to test"):
        add_test_evaluation_to_test(test_id, evaluation_type_id)
        st.success(f"Test evaluation added successfully!")

    st.write("Add test to student:")
    student_test_student_id = st.text_input("Enter student id to add test to")
    student_test_id = st.text_input("Enter student's test id")
    if st.button("Add test to student"):
        add_student_to_tests(student_test_student_id, student_test_id)
        st.success(f"Test added to student successfully!")

    st.write("Add test evaluation to student:")
    evaluation_student_id = st.text_input("Enter student id to add evaluation to")
    evaluation_test_evaluation_id = st.text_input("Enter evaluation id")
    score = st.text_input("Enter score")
    comments = st.text_input("Enter comments")
    if st.button("Add test evaluation to student"):
        add_test_evaluation_to_student(evaluation_student_id, evaluation_test_evaluation_id, score, comments)
        st.success(f"Test evaluation added successfully!")

    # All student test evaluations
    st.write("All student test evaluations:")
    all_test_evaluations = get_all_student_test_evaluations()
    for all_test_evaluation in all_test_evaluations:
        st.write(all_test_evaluation.student_id, all_test_evaluation.test_evaluation_id, all_test_evaluation.score, all_test_evaluation.comments)

if __name__ == '__main__':
    main()