import click
import uuid
from datetime import date, datetime
import pickle
import os
import csv

from dataclasses import dataclass

CSV_PATH = "data/todo_list.csv"

@dataclass
class Todo:
    id: uuid.UUID
    task: str
    due: date
    complete: bool

    def __str__(self) -> str :
        show_date = self.due.strftime('%d/%m/%Y')
        if self.due.strftime('%d/%m/%Y') == '11/11/1111' :
            show_date = "-- None --"
        return f"id: {self.id}, due date: {show_date}, task: {self.task}, complete: {self.complete}"


@click.group()
def cli():
    pass


def load_csv(path : str) -> list[Todo]:
    todo_list = list()
    if os.path.exists(path):
        with open(path, "r") as lf :
            spamreader = csv.reader(lf, delimiter=',')

            for e in spamreader :
                new_date = datetime.strptime(e[2], "%Y-%m-%d").date()
                todo_list.append(Todo(e[0], e[1], new_date, e[3]))
    
    return todo_list


def save_csv(path : str, todo_list : list[Todo]) -> None:
    with open(path, "w") as sf :
        writer = csv.writer(sf)
        for e in todo_list :
            writer.writerow(e.__dict__.values())


todo_list = load_csv(CSV_PATH)


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=datetime(1111,11,11,1,1).strftime("%d/%m/%Y"), prompt="Due", help="Due of task.", show_default=False)
def create(task: str, due: date):
    todo = Todo(uuid.uuid4(), task, due.date(), False)
    click.echo(todo)
    todo_list.append(todo)

    with open('todo.p', 'wb') as f:
        pickle.dump(todo, f)

    save_csv(CSV_PATH, todo_list)



@cli.command()
def read():
    with open('todo.p', 'rb') as f:
        todo = pickle.load(f)
    
    click.echo(todo)



@cli.command()
def update():
    with open('todo.p', 'rb') as f:
        todo = pickle.load(f)
        
    click.echo(todo)
    
    cont = True

    while cont :
        click.echo("What do you want to change ? [task: t / due: d / state: s / nothing: n]")
        ans = click.getchar()

        if ans in ["t", "d", "s"]:
            if ans == "t" :
                todo.task = click.prompt("New task")
            if ans == "d" :
                new_date = click.prompt("New date", default=date.today().strftime("%d/%m/%Y")).split("/")
                if len(new_date) == 3 :
                    todo.due = date(int(new_date[2]), int(new_date[1]), int(new_date[0]))
            if ans == "s" :
                todo.complete = not todo.complete

            click.echo()
            click.echo(todo)
            click.echo()


        click.echo("Continue changes ? [Y/n]")
        ans = click.getchar()

        if ans == "n" :
            cont = False
    
    todo_exist: bool = False
    for i in range(len(todo_list)) :
        print(todo_list[i])
        if todo_list[i].id == todo.id :
            todo_list[i] = todo
            todo_exist = True
            break
    
    if not todo_exist :
        todo_list.append(todo)

    with open('todo.p', 'wb') as f:
        pickle.dump(todo, f)
    
    save_csv(CSV_PATH, todo_list)


@cli.command()
def delete():
    os.system("rm todo.p")


@cli.command()
def display_list():
    for e in todo_list :
        click.echo(e)