# mosamatic2
Advanced desktop and API tool for body composition analysis

## Desktop vs. API vs. CLI
mosamatic2 can be started in 3 ways: (1) as a desktop application (written in PySide6),
(2) as a web server that can be called through its REST interface or (3)
as a Command Line Interface (CLI). This allows mosamatic2 to be used inside larger data 
processing and analysis pipelines.


## Installation
mosamatic2 is available on PyPI.org and can be installed using the following command (after
installing Python 3.11):

    python -m pip install mosamatic2

## Desktop
mosamatic2 can be started as a desktop application with the command:

    mosamatic2

## API
You can also start mosamatic2 as a web server with the command:

    mosamatic2-server

The API server can be accessed through its REST interface at the following URL:

    http://localhost:8000

## CLI
mosamatic2 can be used as a CLI with the following command:

    mosamatic2-cli <command>

If you only type "mosamatic2-cli" you will see help information about which commands are available.
By typing "mosamatic2-cli showdoc <command>" you will more detailed help information about the 
given command.