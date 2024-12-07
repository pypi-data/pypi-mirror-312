import typer

app=typer.Typer()

@app.callback()
def callback():
    """
    Awesome portal gun
    """

@app.command()
def shoot():
    """
    shoot the portal gun
    """
    typer.echo("shooting gun")


@app.command()
def load():
    """
    load the portal gun
    """
    typer.echo("loading gun")