"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def homepage():
    """ Show homepage. """
    
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html", students = students, projects = projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    results = hackbright.get_grades_by_github(github)

    # return f"{github} is the GitHub account for {first} {last}"
    return render_template('student_info.html', first_name=first, last_name=last, github_account=github, results = results)


@app.route("/student-search")
def get_student_form():
    """Show a form for searching a student. """

    return render_template('student_search.html')


@app.route("/student-add", methods=['POST'])
def student_add():
    """ Add a student."""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template('student_added.html', github_account = github)


@app.route("/student-add-form")
def student_add_form():
    """ Show a form to add a new student. """    

    return render_template("student_add_form.html")

@app.route("/project")
def show_project_info():
    """Show information about a student."""

    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)

    results = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", project_title = title, description = description, max_grade = max_grade, results = results)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
