import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    This is the main command line interface for the calculator CLI
    """


@app.command()
def add(a: int, b: int):
    """
    Add two numbers together
    """
    result = a + b
    typer.echo(result)


@app.command()
def subtract(a: int, b: int):
    """
    Subtract two numbers
    """
    result = a - b
    typer.echo(result)