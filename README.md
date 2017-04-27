# FA*IR: A Fair Top-k Ranking Algorithm (code and data)

This repository includes the source code and data sets associated with the the following research paper:

* Meike Zehlike, Francesco Bonchi, Carlos Castillo, Sara Hajian, Mohamed Megahed and Ricardo Baeza-Yates FA\*IR: A Fair Top-k Ranking Algorithm. Submitted for review. 2017.

## Installation

### System Requirements

This program was developed and tested in [Python 3.5](https://www.python.org/downloads/release/python-350/). It uses the following modules:

    * DateTime	4.1.1
    * Jinja2	2.9.6
    * MarkupSafe	1.0
    * PyPDF2	1.26.0
    * cycler	0.10.0
    * guacamole	0.9.2
    * matplotlib	2.0.0
    * numpy	1.12.0
    * padme	1.1.1
    * pandas	0.19.2
    * pip	9.0.1
    * plainbox	0.34.0
    * pyparsing	2.1.10
    * python-dateutil	2.6.0
    * pytz	2016.10
    * requests	2.13.0
    * scipy	0.18.1
    * setuptools	28.8.0
    * six	1.10.0
    * utils	0.9.0
    * zope.interface	4.3.3


### Installation
1. Download the repository to your local disk:
https://github.com/MilkaLichtblau/FA-IR_Ranking/archive/master.zip
alternatively clone the repository in the desired directory:
`git clone https://github.com/MilkaLichtblau/FA-IR_Ranking.git`

2. Open the Shell:
 - Terminal (Mac/Linux) is located under Applications
 - Command Line (Windows) is reachable from the Start menu > Run > `cmd`

3. Navigate to the directory where you downloaded / cloned the repository
`$ cd ~/Downloads/FA-IR_Ranking/src`

4. Run one or any of the following commands:
    * `python3 main.py` for the full program
    * `python3 main.py -h` to obtain help and know which commands to run.
    * `python3 main.py -c` to create all datasets.
    * `python3 main.py -c sat` to create only the SAT scores dataset.
    * `python3 main.py -c compas` to create only the COMPAS dataset.
    * `python3 main.py -c germancredit` to create only the German Credit (SCHUFA) dataset.
    * `python3 main.py -c xing` to create only the Xing dataset.
    * `python3 main.py -r` to rank all datasets.
    * `python3 main.py -r sat` to rank only the SAT dataset with respect to Gender.
    * `python3 main.py -r compasgender` to rank only the COMPAS dataset with respect to gender.
    * `python3 main.py -r compasrace` to rank only the COMPAS dataset with respect to race.
    * `python3 main.py -r germancredit_25` to rank only the German Credit (SCHUFA) dataset with respect to age (below 25 / 25 and above).
    * `python3 main.py -r germancredit_35` to rank only the German Credit (SCHUFA) dataset with respect to age (below 35 / 35 and above).
    * `python3 main.py -r germancredit_gender` to rank only the German Credit (SCHUFA) dataset with respect to age gender.
    * `python3 main.py -r xing` to rank only the Xing dataset with respect to gender.
    * `python3 main.py -e` to evaluate all datasets.
    * `python3 main.py -e sat` to evaluate only the SAT dataset with respect to Gender.
    * `python3 main.py -e compasgender` to evaluate only the COMPAS dataset with respect to gender.
    * `python3 main.py -e compasrace` to evaluate only the COMPAS dataset with respect to race.
    * `python3 main.py -e germancredit_25` to evaluate only the German Credit (SCHUFA) dataset with respect to age (below 25 / 25 and above).
    * `python3 main.py -e germancredit_35` to evaluate only the German Credit (SCHUFA) dataset with respect to age (below 35 / 35 and above).
    * `python3 main.py -e germancredit_gender` to evaluate only the German Credit (SCHUFA) dataset with respect to age gender.
    * `python3 main.py -e xing` to evaluate only the Xing dataset with respect to gender.


## Algorithms
On a list of candidates sorted by ranking, FA*IR algorithms aim to determine bias towards individuals and minority groups *k* in a large sets *n (n >> k)*.
It provides an alternative ranking that includes a proportional number of members from each of the two subsets (protected and non-protected members/groups).
For more information regarding the algorithms, please refer to *section 4* of the paper.

<!-- It is divided into the following Parts: -->

<!-- * Using the Code -->

<!-- * Algorithm 1 -->
<!-- descr -->
<!-- * Available Methods -->

<!-- * Algorithm 2 -->
<!-- * Available Methods -->

<!-- * Algorithm 3 -->
<!-- * Available Methods -->


## Data Sets
Description available in `readme.md` of the respective dataset - check `~/files/testdata`
* [COMPAS](https://github.com/propublica/compas-analysis) - *a dataset related to risk assessment in criminal sentencing in the USA*
* [German Credit Scores](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)) - *a dataset related to credit ratings of individual by the SCHUFA agency in Germany.*
* [SAT](https://secure-media.collegeboard.org/digitalServices/pdf/sat/sat-percentile-ranks-composite-crit-reading-math-writing-2014.pdf) - *a dataset of SAT scores for college-bound high school students in Critical Reading + Mathematics + Writing available from The College Board*
* XING - *a dataset of profiles on XING.com ranked by their search Engine, collected in Jan/Feb 2017*

## Release Notes
*//\\*

## Copyright
*//\\*

### License
*//\\*

## acknowledgements
*//\\*

## references
*//\\* feldmann

## Contact
Meike Zehlike
meike.zehlike at tu-berlin.de
https://www.cit.tu-berlin.de/menue/people/zehlike_meike/

### Keywords
Algorithmic fairness, Ranking, Top-k selection, Discrimination Discovery, Bias, Information Retrieval, Machine Learning


TODOs:

Ger. Credit:  https://archive.ics.uci.edu/ml/citation_policy.html
*//\\* - to fill in
remove the not anonymized xing dataset
a readme for each dataset?
check if it works as it should with the SHAano

guideline: https://data.research.cornell.edu/content/readme

