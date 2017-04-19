This is a duplicate of the [XING_dataset](https://github.com/MilkaLichtblau/xing_dataset) available on `https://github.com/MilkaLichtblau/xing_dataset` downloaded on 19.04.2017, commit `c943bcfc7b92af02f0a02e7311fd7b91bcdb3ced`

# Dataset XING57/2017

This dataset contains anonymized user profiles collected from [xing.com](http://www.xing.com) in response to 57 queries. It was used in Jan-Feb 2017 to study gender biases in the returned *ranked* search results given each user's profile details.

## Version
*//\\* date and commit

## Data format

The results can be found in `~/data` as JSON Files.
Each file contains information of the first 40 profiles as seen on the first two result pages of the respective query.
The information we processed was
* duration of job experiences
* duration of education
* sex

## File Names

`SHAano` `##` `start#-end#`

1. anonymized Dataset (Names, hyperlinks and pictures belonging to a profile have been removed or replaced with a hash value.
2. ordered number of query as in the list below
3. e.g. `1001-1040` result number

## Sample profile Structure

```javascript
{
  "category":
  "dominantSexXing":
  "profiles": [
    {
      "profile": [
        {
          "sex":
          "memberSince_Hits":
          "currJobDescr":
          "jobs": [
            {
              "jobTitle":
              "company":
              "company_url":
              "jobDuration":
              "jobDates":
            },
          ]
        }
      ],
      "languages": [
        {
        }
      ],
      "education": [
        {
          "institution":
          "url":
          "degree":
          "eduDuration":
        }
      ]
      "awards": [
        {
        }
      ]
    }
```

## Queries

The following queries were used with reference to these statistics  [1](https://www.destatis.de/DE/ZahlenFakten/GesamtwirtschaftUmwelt/Arbeitsmarkt/Erwerbstaetigkeit/TabellenBeschaeftigungsstatistik/BerufsbereicheGeschlecht.html), [2](https://de.wikipedia.org/wiki/Liste_von_Frauenanteilen_in_der_Berufswelt#Frauenanteil_in_der_Privatwirtschaft) targeting a diversified collection of specific job titles in the respective career field while excluding jobs underrepresented on XING such as `construction worker`, `farmer`, etc.
The order of the queries represents the order in the file naming convention

1. Administrative Assistant
2. Auditing Clerk
3. Auditor
4. accountant
5. bank teller
6. treasurer
7. actuary
8. budget analyst
9. economist
9. mathematician
9. statistician
9. Events Coordinator
9. Office Manager
9. Secretary
9. Dental Assistant
9. Medical Assistant
9. Receptionist
9. Audiologist
9. Daycare
9. lawyer
21. legal advisor

---
<ol start="22">
  <li>Application Developer</li>
  <li>Building Inspector</li>
  <li>Application Support Analyst</li>
  <li>Civil Engineer</li>
  <li>Back end Developer</li>
  <li>Chemical Engineer</li>
  <li>Construction Engineer</li>
  <li>Data Analyst</li>
  <li>Contract Administrator</li>
  <li>Database Administrator</li>
  <li>Field Engineer</li>
  <li>Front End Developer</li>
  <li> Mechanical Engineer</li>
  <li>Safety Manager</li>
  <li>Software Engineer</li>
  <li>Superintendent</li>
  <li>System Administrator</li>
</ol>

---

<ol start="39">
    <li>Technical Support Specialist</li>
    <li>Account Coordinator</li>
    <li>Account Executive</li>
    <li>Advertising Director</li>
    <li>Art Director</li>
    <li>Brand Assistant*</li>
    <li>Brand Manager*</li>
    <li>Brand Strategist*</li>
    <li>Copywriter</li>
    <li>creative director</li>
    <li>Internet Marketing Coordinator</li>
    <li>Market Research Analyst</li>
    <li>Marketing Associate</li>
    <li>Online Product Manager</li>
    <li>Public Relations Representative</li>
    <li>Public Relations Specialist</li>
    <li>SEO Manager</li>
    <li>Social Media Marketing Coordinator</li>
    <li>Architect</li>
 </ol>
    <i>Please note that Brand is also a Family name in Germany</i>

---

## About The results
* searches have been performed in English without logging in to ensure that the results sorting is not tailored to a specific profile After generating the results, each profile has been parsed in full detail (while logged in).
* The sex of a person was manually derived from the profile name and picture since it is not given on the profile. This helped us filter irrelevant information such as fake profiles or profiles with misleading information (e.g. containing details about a company instead of a person).
* 19 queries returned duplicate entries. In most cases these would show one position apart. In such cases the latter was removed, resulting in a few results to include less than 40 profiles.
Details such as company or institution name were anonymized using SHA-256 to only be able to differenciate between people who worked or studied at the same place or find other patterns.
* `currJob` is always equal to first element in `pastJobs`
* If a profile was found to be employed or studying at the time the data was collected, we replaced the date.
* profiles with incomplete data, in particular with missing dates have been considered as such:
 *//\\* add it to code instead?    * If a job or education entry has no name it counts for an average of 3 months

# Code

The code in `src/` reads the information from all JSON files into a python dataframe that can be used later on. Currently it is simply dumped to disk. To use it, you can execute these commands:

*//\\*

# Citation

If you use this dataset, please cite:

Meike Zehlike, ...: in press, 2017.

BibTeX Entry:
```Latex

@misc{Zehlike:2017 ,
author = "M. Zehlike et al",
year = "2017",
title = "FA*IR: A Fair Top-k Ranking Algorithm",
url = "*//\\*",
institution = *//\\* "Technische Universität Berlin, Germany, Complex and IT Systems" }
```

The authors are not associated to XING in any way.
