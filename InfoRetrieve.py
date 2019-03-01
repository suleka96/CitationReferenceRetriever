import requests
import json
import csv


repeat = True
fileName_data_graph = "paperData.csv"
all_papers = {}


def main(doi):

    global repeat, fileName_data_graph

    for entry in doi:

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

            fileName_cited_referenced_graph = '{}{}{}{}'.format("paper_", id, "_CitedReferenced", ".csv")
            fileName_json = '{}{}{}'.format("paper_", id, ".json")

            with open(fileName_data_graph, "a") as f:
                writer = csv.writer(f)
                writer.writerows(
                    zip([id], [title], [url], [year], [venue], [citationVelocity],
                        [influentialCitationCount]))

            with open(fileName_json, 'w') as outfile:
                json.dump(response_native, outfile)

            with open(fileName_cited_referenced_graph, "a") as f:
                writer = csv.writer(f)
                writer.writerows(
                    zip(["Paper"], ["Cited Paper"]))

            citations = response_native.get('citations')
            for citation in citations:
                # authors = citation.get('authors')
                # allAuthors_cited = None
                # for author in authors:
                #     name = author.get('name')
                #     if allAuthors_cited == None:
                #         allAuthors_cited =  name
                #     else:
                #         allAuthors_cited = allAuthors_cited + "," + name

                citation_title = citation.get('title')
                # citation_doi =citation.get('doi')
                # citation_url =citation.get('url')
                citation_year = citation.get('year')
                citation_id = citation.get('paperId')

                temp_paper_list.append(citation_id)

                citedPaper_name_year = citation_title + " - " + str(citation_year)

                with open(fileName_cited_referenced_graph, "a") as f:
                    writer = csv.writer(f)
                    writer.writerows(
                        zip([paper_name_year], [citedPaper_name_year]))

            references = response_native.get('references')
            for reference in references:
                # authors = reference.get('authors')
                # allAuthors_referenced = None
                # for author in authors:
                #     name = author.get('name')
                #     if allAuthors_referenced == None:
                #         allAuthors_referenced = name
                #     else:
                #         allAuthors_referenced = allAuthors_referenced + "," + name

                reference_title = reference.get('title')
                # reference_doi =reference.get('doi')
                # reference_url =reference.get('url')
                reference_year = reference.get('year')
                reference_id = reference.get('paperId')

                temp_paper_list.append(reference_id)

                referencedPaper_name_year = reference_title + " - " + str(reference_year)

                with open(fileName_cited_referenced_graph, "a") as f:
                    writer = csv.writer(f)
                    writer.writerows(
                        zip([referencedPaper_name_year], [paper_name_year]))

            if repeat:
                repeat = False
                main(temp_paper_list)
                repeat = True


doi = ["10.1145/974036.974037","10.1145/3175684.3175695"]
with open(fileName_data_graph, "a") as f:
    writer = csv.writer(f)
    writer.writerows(
        zip(["Paper Id"], ["Title"], ["URL"], ["Year"], ["Venue"],
            ["CitationVelocity"], ["InfluentialCitationCount"]))
main(doi)