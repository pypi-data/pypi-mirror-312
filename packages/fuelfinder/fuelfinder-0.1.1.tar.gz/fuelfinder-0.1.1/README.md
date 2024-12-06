# Fuelfinder

Fuelfinder is a Python tool to scrape fuel prices from [fuelfinder.dk](https://www.fuelfinder.dk). It provides functionality to fetch current fuel prices while maintaining rate limiting and local caching, ensuring minimal requests to the server.

## Features
- **Scrape Fuel Prices**: Get up-to-date fuel prices from the `fuelfinder.dk` website.
- **Rate Limiting**: Ensures that requests to the server are made no more than once every 5 minutes using a persistent cache.
- **Command-Line Interface (CLI)**: Built using Typer, allowing easy usage and configuration.
- **Debug Logging**: Optional debug logging using Python's built-in logging for better transparency and troubleshooting.
- **Pre-commit Setup**: Uses `ruff` to ensure the code meets quality and consistency standards.

## Installation

To install Fuelfinder, clone the repository and use [uv](https://github.com/astral-sh/uv) to manage dependencies:

```sh
# Clone the repository
git clone https://github.com/yourusername/fuelfinder.git
cd fuelfinder

# Install dependencies using uv
uv sync
```

## Usage

You can use the Fuelfinder CLI to fetch danish fuel prices directly from the command line:

```sh
# Run Fuelfinder
uvx run fuelfinder
```

### Command-line Options
- `--url`: The URL to fetch gas prices from (can also be set via the environment variable `FUELLIST_URL`).
- `--debug`: Enable debug logging for more detailed output.

For example:

```sh
uvx fuelfinder --debug
```

## Pre-commit Hooks
This project uses [pre-commit](https://pre-commit.com/) to ensure code quality. The hooks used include:
- **Ruff**: A fast Python linter and code formatter.
- **Pre-commit Hooks**: Various checks, including trailing whitespace and YAML/JSON validation.

To set up pre-commit hooks:

```sh
pre-commit install
```

To run the hooks manually on all files:

```sh
pre-commit run --all-files
```

## Configuration

The caching for fuel prices is implemented using `diskcache` and is stored in `~/.cache/fuelfinder_cache` to persist across invocations. The default caching duration is 5 minutes.

## Development

If you want to contribute to Fuelfinder, feel free to submit a pull request. Please make sure your code adheres to the following guidelines:
- Ensure the code passes all pre-commit hooks.
- Write clear and concise documentation for any new functionality.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [fuelfinder.dk](https://www.fuelfinder.dk) for providing the data source.
- The authors of `ruff`, `typer`, `diskcache`, and other open-source projects used in this tool.
