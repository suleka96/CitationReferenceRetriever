<h1>CitationReferenceRetriever</h1>

It is a simple application that, when given a paper, retrieves information about papers that were cited in the concerning paper and also information about the papers that have referenced the concerning paper. 

<h2>How?</h2>

Simply put the DOIs of the papers you want to retrieve information of, inside the "doi" list as shown below:

doi = ["10.1145/974036.974037", "10.1145/3175684.3175695"]


Considering one paper eg ("10.1145/974036.974037") we will record the name and the year of the cited and referenced papers. we will also go through this list of obtained papers and find each paper's cited and refernced papers as well. The cited and referenced  information will be recorded in sepeate files for each  paper.Furthurmore, information about all the evauated papers will be writteen in a seperate file caleed "paperData". All this information can be found inside the "papers" folder which is nested inside a folder names "ResearchPapers" in your root directory. The original jason files will also be saved inside a folder named "json" which is also inside the "ReserchPapers" folder.

Information about the cited/referenced papers will be in below format

| Paper | Cited Paper|
| :---: | :---: |
|Techniques for Developing and Measuring High-Performance Web Servers over ATM Networks - 1998 |  Enhancing Web Performance - 2002 |

| Paper Id | Title | URL | Year | Venue | CitationVelocity | InfluentialCitationCount |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
| 5db8bc966b2cd73541ae2f7a71e7d3c6ac59b9a2 | Evaluation of a just-in-time compiler retrofitted for PHP | https://www.semanticscholar.org/paper/5db8bc966b2cd73541ae2f7a71e7d3c6ac59b9a2 | 2010 | VEE | 0 | 0 |
