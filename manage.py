import os

import typer

from app.app import get_application
from app.core.config import settings

cli = typer.Typer()
app = get_application()


@cli.command()
def serve(workers: int = 1):
    os.system(f'gunicorn manage:app --workers {workers} --worker-class uvicorn.workers.UvicornWorker '
              f'--bind {settings.HOST}:{settings.PORT}')


if __name__ == '__main__':
    cli()
