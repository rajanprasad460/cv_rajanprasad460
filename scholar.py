


from scholarly import scholarly
import json

AUTHOR_ID = "I253qyAAAAAJ"

author = scholarly.search_author_id(AUTHOR_ID)
author = scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

papers = []

for pub in author.get("publications", []):
    pub = scholarly.fill(pub)
    bib = pub.get("bib", {})

    papers.append({
        "title": bib.get("title", ""),
        "authors": bib.get("author", ""),
        "venue": bib.get("venue", ""),
        "year": bib.get("pub_year", ""),
        "citations": pub.get("num_citations", 0),
        "url": pub.get("pub_url", ""),
        "bibtex": pub.get("bibtex", "")
    })

data = {
    "name": author.get("name", ""),
    "citations": {
        "all": author.get("citedby", 0),
        "since_2021": author.get("citedby5y", 0)
    },
    "h_index": {
        "all": author.get("hindex", 0),
        "since_2021": author.get("hindex5y", 0)
    },
    "i10_index": {
        "all": author.get("i10index", 0),
        "since_2021": author.get("i10index5y", 0)
    },
    "citations_per_year": author.get("cites_per_year", {}),
    "papers": papers
}

with open("scholar.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("scholar.json saved")