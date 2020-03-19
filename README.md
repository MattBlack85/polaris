# Polaris

Scrape data about coronavirus from WHO PDFs

# Dependencies

If you don't want to setup everything by hand then you must have already installed `pipenv`, otherwise I know you know what you're doing :)

# Setup everything

Setup everything with `make bootstrap`. This will create a virtual environment with pipenv and will install the dependencies from the Pipfile

## Get data

polariscv.py is a wrapper around the client, you can invoke via `python polariscv.py yyyy-mm-dd` or you can use the make command
`make get-data DATE=yyyy-mm-dd`

The output will be a CSV file called yyyy-mm-dd.csv containing the data for the given day.


## KNOWN ISSUES

Unfortunately, data from WHO PDFs are not consisent, they changed the table structure *A LOT* of times and in fact we can't scrape PDFs older than March, 12th (I think),
Some of the countries names are lost during coversion (weird PDF format) and a double check is needed.
