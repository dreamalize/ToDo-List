from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker



engine = create_engine("sqlite:///todo.db?check_same_thread=False")

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="task name")
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    print("Enter task")
    task_name = input()
    print("Enter deadline")
    deadline = input()
    new_task = Table(task=task_name, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
    session.add(new_task)
    session.commit()
    print("The task has been added! \n")


def all_task_list():
    all_tasks = session.query(Table).order_by(Table.deadline).all()

    if len(all_tasks) == 0:
        print("All tasks: \nNothing to do! \n")
    else:
        print("All tasks:")
        for i in range(len(all_tasks)):
            row = all_tasks[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")
    print()


def today_list(today):
    all_tasks = session.query(Table).filter(Table.deadline == today.date()).all()
    print(f"Today {today.strftime('%#d %b')}:")

    if len(all_tasks) == 0:
        print("Nothing to do!")
    else:
        for i in range(len(all_tasks)):
            row = all_tasks[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")
    print()


def week_day(int):
    days_dict = {0: "Monday",
                 1: "Tuesday",
                 2: "Wednesday",
                 3: "Thursday",
                 4: "Friday",
                 5: "Saturday",
                 6: "Sunday"}
    for day in days_dict:
        if int == day:
            return days_dict[int]


def week_list(today):
    week = dict()
    for i in range(7):
        day = today + timedelta(days=i)
        day_of_week = week_day(day.weekday())
        week[day] = day_of_week

    for day in week:
        all_tasks = session.query(Table).filter(Table.deadline == day.date()).all()
        print(f"{week[day]} {day.strftime('%#d %b')}:")
        if len(all_tasks) == 0:
            print("Nothing to do!\n")
        else:
            for i in range(len(all_tasks)):
                row = all_tasks[i]
                print(f"{row.id}. {row.task}")
            print()


def missed_tasks(today):
    all_tasks = session.query(Table).filter(Table.deadline < today.date()).all()
    print("Missed tasks:")
    if len(all_tasks) == 0:
        print("Nothing is missed!")
    else:
        for i in range(len(all_tasks)):
            row = all_tasks[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")
    print()


def delete_task():
    all_tasks = session.query(Table).order_by(Table.deadline).all()

    if len(all_tasks) == 0:
        print("All tasks: \nNothing to do! \n")
    else:
        print("Choose the number of the task you want to delete:")
        for i in range(len(all_tasks)):
            row = all_tasks[i]
            print(f"{i + 1}. {row.task}. {row.deadline.strftime('%#d %b')}")
        user_choice = int(input())
        del_task = all_tasks[user_choice - 1]
        session.delete(del_task)
        session.commit()
        print("The task has been deleted!")
    print()


def menu():
    today = datetime.today()
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        user_input = input()
        if user_input == "1":
            today_list(today)

        elif user_input == "2":
            week_list(today)

        elif user_input == "3":
            all_task_list()

        elif user_input == "4":
            missed_tasks(today)

        elif user_input == "5":
            add_task()

        elif user_input == "6":
            delete_task()

        elif user_input == "0":
            print("Bye! \n")
            break

menu()
