import click
import uuid
from datetime import date
import pickle

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    due: date
    complete: bool

    def __str__(self) :
        return f"id : {self.id}, task : {self.task}\n\t due date : {self.due.strftime('%d/%m/%Y')}, complete : {self.complete}"


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(formats=["%d/%m/%Y"]), default=date.today().strftime("%d/%m/%Y"), prompt="Due", help="Due of task.")
def create(task: str, due: date):
    todo = Todo(uuid.uuid4(), task, due, False)
    click.echo(todo)
    with open('todo.p', 'wb') as f:
        pickle.dump(todo, f)



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

    with open('todo.p', 'wb') as f:
        pickle.dump(todo, f)