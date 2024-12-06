import click

from .instance import get_instances
from .setup import setup as setup_miplib
from .solve import solve as solve_instance

@click.group()
def cli():
    pass

@cli.command()
def setup():
    setup_miplib()

@cli.command()
@click.option("--instance", "-i", type=str, help="Instance name", default="app1-1")
@click.option("--runtime", "-r", type=int, help="Runtime limit", default=20)
def solve(instance: str, runtime: int):
    solve_instance(instance, runtime)

@cli.command()
@click.option("--count", "-c", type=int, help="Number of instances to return", default=5)
def instances(count: int):
    instances = get_instances(count)
    print(instances)


