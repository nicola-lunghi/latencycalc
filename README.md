# latencycalc

A tool to calculate the input/output latency of your audio interface using Python and ASIO.

## Installation

### Using pipx (recommended)

```bash
pipx install git+https://github.com/nicola-lunghi/latencycalc.git
```

### Using pip

### Development installation

For development with linting and formatting tools:

```bash
pip install -e ".[dev]"
```

### Manual installation

Download `latencycalc.py` and run it directly:

```bash
python latencycalc.py --help
```

## Usage

After installation, you can run the tool with:

```bash
latencycalc --help
```

### List available interfaces

```bash
latencycalc list-interfaces
```

### Measure latency for a specific device

```bash
latencycalc measure --device-id 0
```

### Specify input and output channels

```bash
latencycalc measure --device-id 0 --input-channel 0 --output-channel 0
```

### Disable CSV export

```bash
latencycalc measure --device-id 0 --no-csv-export
```

## Commands

- `list-interfaces`: List all available audio interfaces
- `measure`: Measure audio latency (see options below)

## Measure Options

- `--device-id`: Device ID for ASIO device
- `--input-channel`: Input channel index (0-based, default 0)
- `--output-channel`: Output channel index (0-based, default 0)
- `--csv-export/--no-csv-export`: Enable/disable CSV export (default True)
- `--version`: Show version information

## Requirements

- Python 3.8+
- ASIO-compatible audio device
- ASIO4ALL driver (for non-native ASIO devices)

## Development

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting, and [bump2version](https://github.com/c4urself/bump2version) for version management.

To run linting:

```bash
ruff check .
```

To format code:

```bash
ruff format .
```

### Version Management

To bump the version:

```bash
# Patch version (0.1.0 -> 0.1.1)
bump2version patch

# Minor version (0.1.0 -> 0.2.0)
bump2version minor

# Major version (0.1.0 -> 1.0.0)
bump2version major
```

This will update the version in `pyproject.toml` and `src/latencycalc.py`, commit the changes, and create a git tag.

## License

MIT License - see LICENSE file for details.
