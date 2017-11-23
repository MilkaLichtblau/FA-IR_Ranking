# A Tool for Fair Rankings in Search

This repository consists of a collection of approaches to make learning-to-rank frameworks fairer with respect to modern anti-discrimination laws. The master branch contains most recent developments and is therefore not stable. Please use the branches associated to the respective papers if you want to reproduce any experiments.

The repository includes the source code and data sets associated with the the following research papers:

* Meike Zehlike, Francesco Bonchi, Carlos Castillo, Sara Hajian, Mohamed Megahed and Ricardo Baeza-Yates. FA\*IR: A Fair Top-k Ranking Algorithm. CIKM 2017. *(Please use branch FA-IR_CIKM_17 for reproducing experiments of this paper)*



## Set-up

### Dependencies

This program was developed and tested in [Python 3.5](https://www.python.org/downloads/release/python-350/). It depends on the following modules:

* cycler 0.10.0
* DateTime 4.1.1
* guacamole 0.9.2
* Jinja2 2.9.6
* MarkupSafe 1.0
* matplotlib 2.0.0
* numpy 1.12.0
* padme 1.1.1
* pandas 0.19.2
* pip 9.0.1
* plainbox 0.34.0
* pyparsing 2.1.10
* PyPDF2 1.26.0
* python-dateutil 2.6.0
* pytz 2016.10
* requests 2.13.0
* scipy 0.18.1
* setuptools 28.8.0
* six 1.10.0
* utils 0.9.0
* zope.interface 4.3.3  

### Installation

1. Clone this repository:
`git clone https://github.com/MilkaLichtblau/FA-IR_Ranking.git`

2. In a command-line shell, navigate to the directory where you cloned the repository:
`$ cd ~/Downloads/FA-IR_Ranking/src`

## Datasets

The following datasets are included:

| Code  | Description |
| ----- | ----------- |
| sat   | *Scholastic Assessment Test* ([SAT](https://secure-media.collegeboard.org/digitalServices/pdf/sat/sat-percentile-ranks-composite-crit-reading-math-writing-2014.pdf)): a standardized test used in the US for university admissions  |
| compas | *Correctional Offender Management Profiling for Alternative Sanctions* ([COMPAS](https://github.com/propublica/compas-analysis)): a survey used in some US states for alternative sanctions such as parole |
| germancredit | [German Credit Scores](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)) (SCHUFA) dataset |
| xing | A dataset collected from the professional social network Xing in Jan/Feb 2017 |

The datasets are included in the repository in "raw" form, so you need to use the `-c` option first to create the processed datasets, as described below.

## Reproducing the experiments in the paper

`python3 main.py -h` can be used to obtain help.

`python3 main.py -c dataset` creates datasets. The *dataset* can be "sat," "compas," "germancredit," or "xing." If you omit the dataset, it will create all datasets.

`python3 main.py -r dataset-attribute` ranks a dataset using the FA\*IR algorithm and a baseline algorithm, with respect to a protected attribute. If you omit the *dataset-attribute* it ranks all.

* `python3 main.py -r sat` ranks the *sat* dataset with protected attribute gender=female.
* `python3 main.py -r compasgender` ranks the *compas* dataset with protected attribute gender=male
* `python3 main.py -r compasrace` ranks the *compas* dataset with protected attribute race=black
* `python3 main.py -r germancredit_25` ranks the *germancredit* dataset with protected attribute age=below 25
* `python3 main.py -r germancredit_35` ranks the *germancredit* dataset with protected attribute age=below 35
* `python3 main.py -r germancredit_gender` ranks the *germancredit* dataset with protected attribute gender=female
* `python3 main.py -r xing` ranks the *xing* dataset with protected attribute gender=female

`python3 main.py -e dataset-attribute` evaluates a set of rankings generated using the method above.

## Using the algorithm in your own code

(TBA)

## License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact

Meike Zehlike

meike.zehlike at tu-berlin.de

https://www.cit.tu-berlin.de/menue/people/zehlike_meike/
