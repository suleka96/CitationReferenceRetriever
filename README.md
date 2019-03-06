<h1>CitationReferenceRetriever</h1>

It is a simple application that, when given a paper, retrieves information about papers that were cited in the concerning paper and also information about the papers that have referenced the concerning paper. This was done using the [semanticscholar API](http://api.semanticscholar.org/).

Considering a single paper, we will record the title and the year of the cited/referenced papers and also of the paper being evaluated itself. we will also go through this list of obtained papers and find each paper's cited and referenced papers as well. The cited and referenced information will be recorded in separate files for each paper. Furthermore, information about all the evaluated papers will be written in a separate file called "paperData". All this information can be found inside the "papers" folder which is nested inside a folder named "ResearchPapers" in your root directory. The original json files will also be saved inside a folder named "json" which is also nested inside the "ReserchPapers" folder.

<b>Note:</b> This program was made using Python version: 3.6.5

<h2>Dependencies</h2>

Before running this code you need to install the [Requests package](https://pypi.org/project/requests/) into your machine or IDE. 

<h2>How To Use?</h2>

Simply run the program and enter the DOIs of the papers you want to retrieve information of:

[picture](docs/cite.png)

<h2>Data Representation</h2>

Information about the cited/referenced papers (paper_<paper_id>_CitedReferenced.csv) will be in the following format:

| Paper | Cited Paper|
| :---: | :---: |
|Techniques for Developing and Measuring High-Performance Web Servers over ATM Networks - 1998 |  Enhancing Web Performance - 2002 |

Information about the evaluated papers (paperData.csv) will be in the following format:

| Paper Id | Title | URL | Year | Venue | CitationVelocity | InfluentialCitationCount |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
| 5db8bc966b2cd73541ae2f7a71e7d3c6ac59b9a2 | Evaluation of a just-in-time compiler retrofitted for PHP | https://www.semanticscholar.org/paper/5db8bc966b2cd73541ae2f7a71e7d3c6ac59b9a2 | 2010 | VEE | 0 | 0 |
