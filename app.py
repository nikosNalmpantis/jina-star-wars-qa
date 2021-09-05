__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import os
import sys

import click
from jina import Flow, Document, DocumentArray
import logging

MAX_DOCS = int(os.environ.get("JINA_MAX_DOCS", 0))
cur_dir = os.path.dirname(os.path.abspath(__file__))


def config(dataset: str = "star-wars") -> None:
    if dataset == "star-wars":
        os.environ["JINA_DATA_FILE"] = os.environ.get("JINA_DATA_FILE", "data/StarWars_Descriptions.txt")
    os.environ.setdefault('JINA_WORKSPACE', os.path.join(cur_dir, 'workspace'))
    os.environ.setdefault(
        'JINA_WORKSPACE_MOUNT',
        f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace')
    os.environ.setdefault('JINA_LOG_LEVEL', 'INFO')
    os.environ.setdefault('JINA_PORT', str(45678))


def input_generator(file_path: str, num_docs: int):
    with open(file_path) as file:
        lines = file.readlines()
    num_lines = len(lines)
    if num_docs:
        for i in range(min(num_docs, num_lines)):
            yield Document(text=lines[i])
    else:
        for i in range(num_lines):
            yield Document(text=lines[i])


def index(num_docs: int) -> None:
    flow = Flow().load_config('flows/flow-index.yml')
    data_path = os.path.join(os.path.dirname(__file__), os.environ.get("JINA_DATA_FILE", None))
    with flow:
        flow.post(on="/index", inputs=input_generator(data_path, num_docs), show_progress=True)


def query(top_k: int) -> None:
    flow = Flow().load_config('flows/flow-query.yml')
    with flow:
        text = input('Please type a sentence: ')
        doc = Document(content=text)

        result = flow.post(on='/search', inputs=DocumentArray([doc]),
                           parameters={'top_k': top_k},
                           line_format='text',
                           return_results=True,
                           )
        print_topk(result[0])


def print_topk(resp: Document) -> None:
    for doc in resp.data.docs:
        print(f"\n\nResult from app: {doc.tags['answer']}")


@click.command()
@click.option(
    '--task',
    '-t',
    type=click.Choice(['index', 'query'], case_sensitive=False),
)
@click.option('--num_docs', '-n', default=MAX_DOCS)
@click.option('--top_k', '-k', default=5)
@click.option('--data_set', '-d', type=click.Choice(['star-wars']), default='star-wars')
def main(task: str, num_docs: int, top_k: int, data_set: str) -> None:
    config()
    workspace = os.environ['JINA_WORKSPACE']
    logger = logging.getLogger('star-wars-qa')

    if 'index' in task:
        if os.path.exists(workspace):
            logger.error(
                f'\n +------------------------------------------------------------------------------------+ \
                    \n |                                   🤖🤖🤖                                           | \
                    \n | The directory {workspace} already exists. Please remove it before indexing again.  | \
                    \n |                                   🤖🤖🤖                                           | \
                    \n +------------------------------------------------------------------------------------+'
            )
            sys.exit(1)

    if 'query' in task:
        if not os.path.exists(workspace):
            logger.error(f'The directory {workspace} does not exist. Please index first via `python app.py -t index`')
            sys.exit(1)

    if task == 'index':
        index(num_docs)
    elif task == 'query':
        query(top_k)


if __name__ == '__main__':
    main()
