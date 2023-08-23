# CRAN packages parser

This python script parse dependencies for all dependencies form input file and generate full dependency list in output file, with highest versions and in right order for installation.

## Input file format 

basic csv. No header. Each row specifies R package name and it's version. Delimiter - ' '

Example:
```csv
bartcs 1.2.0
Cairo 1.6-1
accrualPlot 1.0.7
```

## Output file format

Same as input

## Python env

Project created with [poetry](https://python-poetry.org/), but also provided regular `requirements.txt`.

## Run locally from scratch

```bash
git clone ...
cd ...
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py 
```
