# Star Wars Question-Answering Search System

This is a simple example to show how to build a Question-Answering Search System based on Star Wars descriptions. It indexes the first paragraph of every text description found in [Wookieepedia](https://starwars.fandom.com/wiki/Main_Page) and then, when provided with a search query uses the most simillar ones to generate an answer.

The app:

- Reads text descriptions from a txt file
- Builds a searchable index by creating vector embeddings from the text descriptions
- Opens up a terminal interface to get an answer to a text query

## Instructions

## Prerequisites

- Running Mac or Linux (or [WSL2 on Windows](https://docs.microsoft.com/en-us/windows/wsl/install-win10)) with [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed
- Python 3.8 or later (with [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) installed)

### Clone this repo

```shell
git clone https://github.com/nikosNalmpantis/jina-star-wars-qa.git
cd jina-star-wars-qa
```

### Create a virtual environment

We wouldn't want our project clashing with our system libraries, now would we?

```shell
virtualenv env --python=python3.8
source env/bin/activate
```

### Get the data

```shell
sh get_data.sh
```

### Install everything

Make sure you're in your [virtual environment](#create-a-virtual-environment) first!

```shell
pip install -r requirements.txt
```

### Run the program

```shell
cd jina-star-wars-qa
python app.py -t index
python app.py -t query
```

### Search from the terminal

```shell
>> Please type a question: Who is Darth Vader?
Answer: Sith Lord Darth Vader
```