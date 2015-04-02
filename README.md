# CAFR Parsing
Automated data extraction from U.S. state Comprehensive Annual Financial Reports (CAFR).

## Current status
1. A state cafr is added to the hot folder by a user
2. The state is identified based on the file name
3. The cafr PDF is converted to a flat text file using pdfminer's "text" interpreter.
4. The state's template file(s) are loaded by the miner
5. The "anchor" of the template (essentially the target table's headers) is used to find the right part of the cafr text file to parse
6. The text file is iterated over and each line is loaded into the template
7. At this point we have the data in JSON format
8. Using the JSON data, output the XML result

### Notes: 
- The template format is completely thoughtless right now (we need to talk through the schema first).  But it can only get better.
- Each state will need a template, but that template should work for all years so long as the format doesn't change from year to year
- The structure of the miner is also completely thoughtless right now -- I wanted to validate the approach before making it robust.

## Installation

### First-time setup (Linux)

You'll need a basic Python environment and the ability to check out this
code repository, so you'll need at least the following packages to run CivOmega:

* **git**
* **python** (specifically **python2**)

Depending on your OS distribution of Python, you may need to manually install
[setuptools](https://pypi.python.org/pypi/setuptools). See that page for info.

Then install `pip` to facilitate the rest of the dependency installation
process:

`sudo easy_install pip`

(If your distribution uses Python 3 by default, you *may* need to change
`easy_install` to `easy_install-2.7`.)

Now install some Python tools that will help you bootstrap your CivOmega
Python environment.

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

## Resources
These are resources that were helpful while exploring:

- I want [http://www.unixuser.org/~euske/python/pdfminer/programming.html](basic information on using pdfminer).
- I want [http://denis.papathanasiou.org/2010/08/04/extracting-text-images-from-pdf-files/](a more complete example of a pdfminer parser).