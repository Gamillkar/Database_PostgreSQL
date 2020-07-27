import psycopg2 as pg

def create_db():
    """Создание таблиц"""

    #таблица студента
    cur.execute('''
        create table if not exists Student(student_id serial primary key,
        name varchar(100) not null,
        gpa numeric(10,2) null,
        birth timestamp with time zone null);''')

    #таблица курса
    cur.execute('''
        create table if not exists Course(
        course_id integer primary key,
        name varchar(100) not null
        );
        ''')

    #связующая таблица
    cur.execute('''
        create table if not exists intermediate_Course_Stud(
        id_course integer references  Course(course_id),
        id_stud integer references  Student(student_id)
        
        );
        ''')
def add_students(course_id, students):
    """создает студентов и записывает их на курс"""
    for man in students:
        cur.execute('''insert into Student(name, gpa, birth) values(%s, %s, %s) RETURNING student_id;''',
                    (man['name'], man['gpa'], man['birth']))
        man_id = cur.fetchall()[0][0]
        cur.execute('''insert into intermediate_Course_Stud(id_course, id_stud) values(%s, %s);''',
        (course_id, man_id))

def get_students(course_id):
    """возвращает студентов определенного курса"""
    cur.execute('''select s.student_id, s.name, s.birth, c.name from intermediate_Course_Stud as ics
    join Student s on s.student_id = ics.id_stud
    join Course c on c.course_id = ics.id_course where c.course_id = (%s);''', (course_id, ))
    print(cur.fetchall())
    return (cur.fetchall())

def add_student(student):
    """Создает студента"""
    cur.execute('''
                insert into Student(name, gpa, birth) values(%s, %s, %s);''',
                (student['name'], student['gpa'], student['birth']))


def get_student(student_id):
    """Возвращает данные студента"""
    cur.execute('select * from Student where student_id=(%s);', (student_id,))
    print(cur.fetchall())
    data = cur.fetchall()
    return data


def create_course(course_id, name):
    """Создает курс"""
    cur.execute('''insert into Course(course_id, name) values(%s, %s);''', (course_id, name))


if __name__ == '__main__':
    with pg.connect(database='neto_hw', user='neto',
                    password='1234', host='localhost', port=5432) as conn:
        cur = conn.cursor()
    create_db()
    create_course(1, 'Python')
    create_course(2, 'Java')

    students = [
        {'name': 'Vasia', 'gpa': '5.0', 'birth': '1870-12-16'},
        {'name': 'Gena', 'gpa': '1.3', 'birth': '2021-11-16'},
        {'name': 'Lena', 'gpa': '4.0', 'birth': '1992-01-13'}
    ]

    students_1 = [
        {'name': 'Vasia', 'gpa': '5.0', 'birth': '1870-12-16'},
        {'name': 'Gena', 'gpa': '1.3', 'birth': '2021-11-16'},
        {'name': 'Lena', 'gpa': '4.0', 'birth': '1992-01-13'}
    ]

    student = {'name': 'Lena', 'gpa': '4.0', 'birth': '1992-01-13'}
    add_students(1, students)
    add_students(2, students_1)
    get_students(2)