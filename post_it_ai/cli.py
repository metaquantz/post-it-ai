"""Post It AI Init"""
import click
from app import PostItAI


@click.command()
@click.argument("query")
def cli(query):
    """CLI class"""
    post_it_ai = PostItAI()
    post_it_ai.run_app(query)


if __name__ == "__main__":
    cli()
