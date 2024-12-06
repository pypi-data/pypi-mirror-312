# Best 403 Unlocker (Python Version)

A Python CLI tool that helps you find the fastest DNS SNI proxy server for your internet service provider. This tool automatically tests multiple DNS servers and configures your system to use the fastest ones.

## Features

- Automated DNS speed testing
- Cross-platform support (Windows, macOS, Linux)
- Easy-to-use command line interface 
- Detailed performance metrics for each DNS server
- Config file support for custom DNS servers
- Progress bar visualization during testing
- Supports both interactive and command-line modes

## Prerequisites

- Python 3.12 or higher
- Poetry package manager
- Administrative/root privileges (required for DNS configuration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/403unlocker/best403unlocker-py.git
cd best403unlocker-py
```
2. Install dependencies using Poetry:

```bash
poetry install
```

## Usage
The tool provides several commands through its CLI interface:

Default Mode
Simply run without any arguments to automatically find and set the fastest DNS servers:

Search DNS Servers
To only test DNS servers without applying them:

Set Specific DNS Servers