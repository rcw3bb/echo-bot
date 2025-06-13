# echo-bot

**echo-bot** is a simple command-line chatbot designed for quick and interactive conversations directly in your terminal.

## :computer: Prerequisites
- Python ^3.13 ([Download Python](https://www.python.org/downloads/))
- Poetry 2.0 ([Poetry installation guide](https://python-poetry.org/docs/#installation))

## :package: Installation
Clone the repository and install dependencies:

```sh
git clone https://github.com/rcw3bb/echo-bot.git
cd echo-bot
poetry install
```


Ensure that a `GITHUB_TOKEN` environment variable is in your system with your GitHub Models API token:

```env
GITHUB_TOKEN=your_github_models_token_here
```

## :zap: Usage

Run the chatbot in your terminal:

```sh
poetry run python -m echo_bot
```

### Commands
- Type your message and press Enter to chat.
- Type `exit` or `quit` to leave the chatbot.
- Type `/reset` to clear the conversation context and start a new session.

## :wrench: Development
- All source code is in the `echo_bot` package.
- Tests are in the `tests` package.

## :microscope: Testing & Coverage
Run all tests and generate an HTML coverage report:
```sh
poetry run pytest --cov=echo_bot tests --cov-report html
```
Open `htmlcov/index.html` to view the coverage report.

## :art: Formatting & Linting
Format and lint the code in one step:
```sh
poetry run black echo_bot && poetry run pylint echo_bot
```

## :scroll: Changelog
See [CHANGELOG.md](CHANGELOG.md) for release history.

## :key: License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## :pen: Author
**Ron Webb**