import requests
import json
import csv
import os
import platform


#global variables
repeat = True
all_papers = {}
citedReferencedPapers = {}
filePath = None


def write_paperInfo(paperId,title,url,year,venue,citationVelocity,influentialCitationCount):

    paperInfoPath = '{}{}'.format(filePath,"/papers/paperData.csv")
    with open(paperInfoPath, "a", errors='replace') as f:
        writer = csv.writer(f)
        writer.writerows(
            zip([paperId], [title], [url], [year], [venue],
                [citationVelocity], [influentialCitationCount]))

def write_citedReferencedInfo(fileName,paper,citedPaper):
    with open(fileName, "a", errors='replace') as f:
        writer = csv.writer(f)
        writer.writerows(
            zip([paper], [citedPaper]))

def createDirectries():

    global filePath

    current_os =  platform.system()

    if current_os == 'Linux' or current_os == 'Darwin':
        filePath = os.path.expanduser('~/ResearchPapers')
    elif current_os == 'Windows':
        filePath = os.path.expanduser('~\ResearchPapers')

    if not os.path.exists(filePath):
        print("path doesn't exist. creating..")
        os.makedirs(filePath)

    if current_os == 'Linux' or current_os == 'Darwin' :
        paperFilePath = os.path.expanduser('~/ResearchPapers/papers')
    elif current_os == 'Windows':
        paperFilePath = os.path.expanduser('~\ResearchPapers\papers')


    if not os.path.exists(paperFilePath):
        print("path doesn't exist. creating..")
        os.makedirs(paperFilePath)

    if current_os == 'Linux' or current_os == 'Darwin':
        jsonFilePath = os.path.expanduser('~/ResearchPapers/json')
    elif current_os == 'Windows':
        jsonFilePath = os.path.expanduser('~\ResearchPapers\json')


    if not os.path.exists(jsonFilePath):
        print("path doesn't exist. creating..")
        os.makedirs(jsonFilePath)

    print("Data will be saved to: ", filePath)



def getInfo(doi_id):

    global repeat

    for entry in doi_id:

        temp_paper_list = []

        url = '{}{}'.format("http://api.semanticscholar.org/v1/paper/", entry)
        response = requests.get(url)
        response_native = json.loads(response.text)

        id = response_native.get('paperId')

        if id in all_papers:
            continue

        else:

            title = response_native.get('title')
            url = response_native.get('url')
            year = response_native.get('year')
            venue = response_native.get('venue')
            citationVelocity = response_native.get('citationVelocity')
            influentialCitationCount = response_native.get('influentialCitationCount')

            paper_name_year = title + " - " + str(year)

            all_papers[id]= title

            fileName_cited_referenced_graph = '{}{}{}{}{}'.format(filePath,"/papers/paper_", id, "_CitedReferenced", ".csv")
            fileName_json = '{}{}{}{}'.format(filePath,"/json/paper_", id, ".json")

            write_paperInfo(id,title,url,year,venue,citationVelocity,influentialCitationCount)

            write_citedReferencedInfo(fileName_cited_referenced_graph,"Paper","Cited Paper")

            with open(fileName_json, 'w') as outfile:
                json.dump(response_native, outfile)


            citations = response_native.get('citations')
            for citation in citations:
                citation_id = citation.get('paperId')

                if citation_id in citedReferencedPapers:
                    continue

                else:
                    citation_title = citation.get('title')
                    citation_year = citation.get('year')

                    citedReferencedPapers[citation_id] = citation_title

                    temp_paper_list.append(citation_id)

                    citedPaper_name_year = citation_title + " - " + str(citation_year)

                    write_citedReferencedInfo(fileName_cited_referenced_graph, paper_name_year, citedPaper_name_year)


            references = response_native.get('references')
            for reference in references:
                reference_id = reference.get('paperId')

                if reference_id in citedReferencedPapers:
                    continue

                else:

                    reference_title = reference.get('title')
                    reference_year = reference.get('year')

                    citedReferencedPapers[reference_id] = reference_title

                    temp_paper_list.append(reference_id)

                    referencedPaper_name_year = reference_title + " - " + str(reference_year)

                    write_citedReferencedInfo(fileName_cited_referenced_graph, referencedPaper_name_year, paper_name_year)

            if repeat:
                repeat = False
                getInfo(temp_paper_list)
                repeat = True


if __name__ == '__main__':

    createDirectries()

    write_paperInfo("Paper Id","Title","URL","Year","Venue","CitationVelocity","InfluentialCitationCount")

    doi = []

    print("\n"+"*********************************"+ "\n")
    print("To enter DOIs, type in the DOI and press 'Enter'." + "\n"
          "Reapeat process and when done, simply press the 'Enter' key again."+ "\n")
    print("*********************************" + "\n")
    print( "Enter DOIs" )

    while True:
        line = input()
        if not line: break
        doi.append(line)

    print("Retrieving Information... ")

    getInfo(doi)
