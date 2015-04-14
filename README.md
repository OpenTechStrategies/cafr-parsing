# CAFR Parsing
Automated data extraction from U.S. state Comprehensive Annual Financial Reports (CAFR).

## Directory Structure
- **analysis**: Various explorations performed around XBRL, CAFR, and PDF conversions.  This is also where the current versions of the working schema are located.
- **data**: The state CAFR files that have been downloaded thus far.
- **results**: Where `miner.py` places its output.
- **templates**: Where table templates (explained below) should be located.  Any .txt files in this directory will be loaded automatically by `miner.py`.

## Installation

### First-time setup (Linux)

You'll need a basic Python environment and the ability to check out this
code repository, so you'll need at least the following packages:

* **git**
* **python** (specifically **python2**)

Depending on your OS distribution of Python, you may need to manually
install [setuptools](https://pypi.python.org/pypi/setuptools).  See
that page for info; on Debian GNU/Linux and probably Ubuntu, you can
just do `sudo apt-get update && sudo apt-get install python-setuptools`.

Then install `pip` to facilitate the rest of the dependency installation
process:

`sudo easy_install pip`

(If your distribution uses Python 3 by default, you *may* need to change
`easy_install` to `easy_install-2.7`.)

Now install some Python tools that will help you bootstrap the Python
environment.

```shell
sudo pip install -UI setuptools pip virtualenv
```

Pick a place to store the repo. I usually put projects in a `Code` directory
in my home folder, but you can adjust this accordingly. `cd` into that
directory. (i.e. `cd ~/Code`) Then:

```shell
git clone https://github.com/OpenTechStrategies/cafr-parsing
virtualenv cafr-parsing
```

(If your distribution uses Python 3 by default, you'll need to change the
`virtualenv` line to be `virtualenv -p /usr/bin/python2 cafr-parsing` or something
along those lines.)

Now we'll `cd` into the cafr-parsing repo and "activate" this environment.
Then, using `pip`, we'll install all the Python libraries defined in the
`requirements.txt` file. (This is sort of like a Ruby `Gemfile`.)

```shell
cd cafr-parsing
source bin/activate
pip install -r requirements.txt
```

You can ensure that the virtual environment is using an isolated version
of Python 2:

```shell
`which python`
python --version
```

## Usage

`miner.py` parses CAFR files, which are PDF documents, and produces JSON files, which can be automatically translated to other formats easily (e.g., XBRL, CSV, .xlsx).

In order to know which tables to extract from the PDF files and what their fields mean, `miner.py` must be supplied with a "template" for each table: a manually-constructed JSON file that tells `miner.py` exactly how to recognize that table and how to map the data in the table to the desired output fields.

For now, the invocation process is just to open up `miner.py` in a text editor and add calls to the end like this:

        process_pdf("data/AL_cafr2011.pdf")

Once you've set up as many calls as you want, run `miner.py` (assuming you've already done the setup steps listed above in the "Installation" section):

        $ python miner.py

It may take a while to run, possibly minutes.  When it's done, the results will be in the `results/` directory.  There will be one result file for each table for a given state CAFR in a given year.

* `data/AL_cafr2011.pdf` is an example CAFR input file
* `templates/AL_statewidenetassets.txt` is an example template file
* `results/AL_cafr2011-statewide_net_assets.json` is an example output file (this won't exist until you run `miner.py`)

## Resources
These are resources that were helpful while exploring:

- [Basic information on using pdfminer](http://www.unixuser.org/~euske/python/pdfminer/programming.html).
- [A more complete example of a pdfminer parser](http://denis.papathanasiou.org/2010/08/04/extracting-text-images-from-pdf-files/).
