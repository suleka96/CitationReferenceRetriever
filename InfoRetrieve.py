import requests
import json
import csv


def main(doi):

    for entry in doi:
        url = '{}{}'.format("http://api.semanticscholar.org/v1/paper/", entry)
        response = requests.get(url)
        response_native = json.loads(response.text)
        citations = response_native.get('citations')
        title = response_native.get('title')

        fileName = '{}{}'.format(title,".csv")
        fileName_json = '{}{}'.format(title, ".json")

        with open(fileName_json, 'w') as outfile:
            json.dump(response_native, outfile)

        for citation in citations:
            authors = citation.get('authors')

            allAuthors_cited = None
            for author in authors:
                name = author.get('name')
                if allAuthors_cited == None:
                    allAuthors_cited =  name
                else:
                    allAuthors_cited = allAuthors_cited + "," + name

            citation_title = citation.get('title')
            citation_doi =citation.get('doi')
            citation_url =citation.get('url')
            citation_year = citation.get('year')
            print(title, ",", citation_title)
            citation_maintitle = title +"," + citation_title

            with open(fileName, "a") as f:
                writer = csv.writer(f)
                writer.writerows(
                    zip([citation_maintitle],[citation_title],[allAuthors_cited],[citation_doi],[citation_url],[citation_year]))

        references = response_native.get('references')
        for reference in references:
            authors = reference.get('authors')
            allAuthors_referenced = None
            for author in authors:
                name = author.get('name')
                if allAuthors_referenced == None:
                    allAuthors_referenced = name
                else:
                    allAuthors_referenced = allAuthors_referenced + "," + name

            reference_title = reference.get('title')
            reference_doi =reference.get('doi')
            reference_url =reference.get('url')
            reference_year = reference.get('year')
            print(reference_title, ",", title)
            reference_maintitle = reference_title + "," + title
            with open(fileName, "a") as f:
                writer = csv.writer(f)
                writer.writerows(
                    zip([reference_maintitle],[reference_title],[allAuthors_referenced],[reference_doi],[reference_url],[reference_year]))


doi = ["10.1145/974036.974037","10.1145/3175684.3175695"]


main(doi)