import requests
import json
import csv
import os
import platform
import pandas as pd
import re
import shutil

#global variables
repeat = True
all_papers = {}
citedReferencedPapers = {}
filePath = None
fileName_cited_referenced_graph = None
paperInfoPath = None
level = 0


def write_paperInfo(paperId,title,url,year,venue,citationVelocity,influentialCitationCount,citation_count):

    global paperInfoPath
    paperInfoPath = '{}{}'.format(filePath,"/papers/paperData.csv")
    with open(paperInfoPath, "a", errors='replace',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(
            zip([paperId], [title], [url], [year], [venue],
                [citationVelocity], [influentialCitationCount], [citation_count]))

def write_citedReferencedInfo(paper,citedPaper):

    global fileName_cited_referenced_graph
    fileName_cited_referenced_graph = '{}{}'.format(filePath, "/papers/citedReferenced.csv")
    with open(fileName_cited_referenced_graph, "a", errors='replace',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(
            zip([paper], [citedPaper]))

def createDirectries():

    global filePath, fileName_cited_referenced_graph, paperInfoPath

    current_os =  platform.system()

    if current_os == 'Linux' or current_os == 'Darwin':
        filePath = os.path.expanduser('~/ResearchPapers')
    elif current_os == 'Windows':
        filePath = os.path.expanduser('~\ResearchPapers')

    if os.path.exists(filePath):
        print("deleting existing directory")
        shutil.rmtree(filePath)

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

    global repeat,level

    for entry in doi_id:

        if entry in all_papers:
            continue

        else:

            temp_paper_list = []

            url = '{}{}'.format("http://api.semanticscholar.org/v1/paper/", entry)
            response = requests.get(url)
            response_native = json.loads(response.text)

            if response_native.get('error') == "Paper not found":
                continue
            else:
                id = response_native.get('paperId')
                title = response_native.get('title')
                url = response_native.get('url')
                year = response_native.get('year')
                venue = response_native.get('venue')
                citationVelocity = response_native.get('citationVelocity')
                influentialCitationCount = response_native.get('influentialCitationCount')

                paper_id_year = id + "-" + str(year)

                all_papers[id] = title

                fileName_json = '{}{}{}{}'.format(filePath, "/json/paper_", id, ".json")

                with open(fileName_json, 'w') as outfile:
                    json.dump(response_native, outfile)

                citation_count = 0
                citations = response_native.get('citations')
                for citation in citations:
                    citation_id = citation.get('paperId')

                    if citation_id in citedReferencedPapers:
                        continue

                    else:
                        citation_count += 1

                        citation_title = citation.get('title')
                        citation_year = citation.get('year')

                        citedReferencedPapers[citation_id] = citation_title

                        temp_paper_list.append(citation_id)

                        citedPaper_id_year = citation_id + "-" + str(citation_year)

                        write_citedReferencedInfo(paper_id_year, citedPaper_id_year)

                write_paperInfo(id, title, url, year, venue, citationVelocity, influentialCitationCount, citation_count)

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

                        referencedPaper_id_year = reference_id + "-" + str(reference_year)

                        write_citedReferencedInfo(referencedPaper_id_year, paper_id_year)

                print("Retrieved Information of: " + title)


                if repeat:
                    level += 1
                    if level == 2:
                        repeat = False
                        getInfo(temp_paper_list)
                        repeat = True
                        level -= 1
                    else:
                        getInfo(temp_paper_list)
                        level -= 1





def addCitedPapers():

    # isolating id value
    df_original = pd.read_csv(fileName_cited_referenced_graph)
    for index, row in df_original.iterrows():
        temp_val = df_original.loc[index, 'Papers']
        split_list = temp_val.split("-")
        id = re.sub(r"\s+$", "", split_list[0], flags=re.UNICODE)
        df_original.loc[index, 'Papers'] = id

    # grouping
    temp_citedReferenced = df_original.groupby(['Papers'], sort=False).count()

    temp_paperInfo = pd.read_csv(paperInfoPath)

    new_data = pd.merge(temp_paperInfo, temp_citedReferenced, how='left', left_on="Paper Id",
                        right_index=True, sort=False)

    # replace nan with 0
    new_data['Cited Papers'] = new_data['Cited Papers'].fillna(0)

    # convert to int
    new_data['Cited Papers'] = new_data['Cited Papers'].astype(int)

    os.remove(paperInfoPath)

    new_data.to_csv(paperInfoPath, sep='\t', encoding='utf-8')

    print("Done")


if __name__ == '__main__':

    print("\n")
    print("  / ____(_) |      | | (_)             |  __ \    | |          (_)               ")
    print(" | |     _| |_ __ _| |_ _  ___  _ __   | |__) |___| |__ __ ___ ___   _____ _ __ ")
    print(" | |    | | __/ _` | __| |/ _ \| '_ \  |  _  // _ \ __| '__/ _ \ \ \ / / _ \ '__|")
    print(" | |____| | || (_| | |_| | (_) | | | | | | \ \  __/ |_| | |  __/ |\ V /  __/ |   ")
    print("  \_____|_|\__\__,_|\__|_|\___/|_| |_| |_|  \_\___|\__|_|  \___|_| \_/ \___|_|   ")
    print("\n")

    createDirectries()

    write_paperInfo("Paper Id","Title","URL","Year","Venue","CitationVelocity","InfluentialCitationCount","TotalCitationCount")
    write_citedReferencedInfo("Papers", "Cited Papers")

    doi = []

    print("\n"+"*********************************"+ "\n")
    print("To enter DOIs, type in the DOI and press 'space bar'." + "\n"
          "Reapeat process and when done, simply press the 'Enter' key."+ "\n")
    print("*********************************" + "\n")

    input = input("Please enter DOIs: ")

    doi = [i for i in input.split()]

    print("Retrieving Information... ")

    getInfo(doi)
    addCitedPapers()
