from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from datetime import datetime, timedelta


Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


class DBHelper:
    def __init__(self, filename):
        self.filename = filename
        self.engine = create_engine(f"sqlite:///{filename}?check_same_thread=False")
        self.conn = self.engine.connect()
        self.Base = Base
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def safe_commit(self):
        try:
            self.session.commit()
        except Exception as e:
            print(e, "\n\nPlease fix the issues above and try again")
            self.session.rollback()
            self.session = self.Session()


def all_tasks(db_helper):
    list_of_tasks = db_helper.session.query(Task).order_by(Task.deadline).all()
    print("All Tasks:")
    print_all_tasks(list_of_tasks, NOTHING_MSG)


def add_task(db_helper):
    task_input = input("Enter a task\n")
    deadline_input = input("Enter a deadline\n")  # need to validate this in the future
    datetime_deadline = datetime.strptime(deadline_input, DATE_INPUT_FMT)  # use a try-except to loop validation
    entry_to_add = Task(task=task_input, deadline=datetime_deadline.date())
    db_helper.session.add(entry_to_add)
    db_helper.safe_commit()
    print("The task has been added!\n")


def exit_menu(db_helper):
    print(EXIT_MSG)


def week_tasks(db_helper):  # this is just today_tasks but repeated for the week
    tasks = db_helper.session.query(Task)\
            .filter(TODAY.date() <= Task.deadline, Task.deadline < (TODAY + ONE_WEEK).date())\
            .all()
    for day in range(7):
        curr_date = (TODAY + timedelta(days=day)).date()
        curr_tasks = filter(lambda task: task.deadline == curr_date, tasks)
        print_day_tasks(list(curr_tasks), curr_date)


def today_tasks(db_helper):
    tasks = db_helper.session.query(Task).filter(Task.deadline == TODAY.date()).all()
    print_day_tasks(tasks, TODAY)


def missed_tasks(db_helper):
    tasks = db_helper.session.query(Task).filter(Task.deadline < TODAY.date()).order_by(Task.deadline).all()
    print("Missed tasks:")
    print_all_tasks(tasks, ALL_DONE_MSG)


def delete_task(db_helper):
    tasks = db_helper.session.query(Task).order_by(Task.deadline).all()
    if tasks:
        print(DELETE_MSG)
        print_all_tasks(tasks, NOTHING_MSG)
        delete_input = int(input())  # need to add validation to this
        to_delete = delete_input - 1
        task = tasks[to_delete]
        db_helper.session.query(Task).filter(Task.id == task.id).delete()
        db_helper.safe_commit()
        print("The task has been deleted!")
    else:
        print(NO_DELETE_MSG)


def print_day_tasks(task_list, date):
    print(date.strftime("%A"), f"{date.strftime(SHORT_DATE_FMT).lstrip('0')}:")
    if task_list:
        for i, task_tuple in enumerate(task_list):
            print(f"{i + 1}. {task_tuple}")
    else:
        print(NOTHING_MSG)
    print()


def print_all_tasks(task_list, none_msg):
    if task_list:
        for i, task in enumerate(task_list):
            print(f"{i + 1}. {task.task}. {task.deadline.strftime(SHORT_DATE_FMT).lstrip('0')}")
    else:
        print(none_msg)
    print()


def start_todo_list(menu_options, db_helper):
    user_input = 99
    menu_copy = menu_options[:]
    menu_string = ""
    for i, option in enumerate(menu_copy):
        num = i + 1 if i < len(menu_copy) - 1 else 0
        menu_string += f"{num}) {option[0]}\n"
    menu_copy.insert(0, menu_copy.pop())  # shift exit to beginning of list
    while user_input != 0:
        print(menu_string)
        user_input = int(input())  # Need to create menu validation later
        menu_copy[user_input][1](db_helper)


MENU_OPTIONS = [("Today's tasks", today_tasks),
                ("Week's tasks", week_tasks),
                ("All tasks", all_tasks),
                ("Missed tasks", missed_tasks),
                ("Add a task", add_task),
                ("Delete a task", delete_task),
                ("Exit", exit_menu)]

DB_NAME = "todo.db"

NOTHING_MSG = "Nothing to do!"
DELETE_MSG = "Choose the number of the task you want to delete:"
EXIT_MSG = "Bye!"
ALL_DONE_MSG = "All tasks have been completed!"
NO_DELETE_MSG = "There are no tasks!"

TODAY = datetime.today()
ONE_WEEK = timedelta(days=7)
SHORT_DATE_FMT = "%d %b"
DATE_INPUT_FMT = "%Y-%m-%d"


if __name__ == "__main__":
    my_db_helper = DBHelper(DB_NAME)
    start_todo_list(MENU_OPTIONS, my_db_helper)
