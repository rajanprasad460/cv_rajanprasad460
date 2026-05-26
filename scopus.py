import requests
import json

API_KEY = "4a77222ca4336573bbe35c19dfec2475"
AUTHOR_ID = "57212165779"

url = f"https://api.elsevier.com/content/search/scopus?query=AU-ID({AUTHOR_ID})&apiKey={API_KEY}"

response = requests.get(url)

print("Status:", response.status_code)
print(response.text[:300])

data = response.json()

entries = data.get("search-results", {}).get("entry", [])

papers = []
total_citations = 0

for item in entries:
    title = item.get("dc:title", "")
    authors = item.get("dc:creator", "")
    venue = item.get("prism:publicationName", "")
    year = item.get("prism:coverDate", "")[:4]
    doi = item.get("prism:doi", "")
    citations = int(item.get("citedby-count", 0))

    scopus_url = ""
    for link in item.get("link", []):
        if link.get("@ref") == "scopus":
            scopus_url = link.get("@href", "")

    total_citations += citations

    papers.append({
        "title": title,
        "authors": authors,
        "venue": venue,
        "year": year,
        "doi": doi,
        "citations": citations,
        "url": scopus_url
    })

papers.sort(key=lambda x: x["year"], reverse=True)

scopus_data = {
    "source": "Scopus",
    "author_id": AUTHOR_ID,
    "total_documents": len(papers),
    "total_citations": total_citations,
    "papers": papers
}

with open("scopus.json", "w", encoding="utf-8") as f:
    json.dump(scopus_data, f, indent=2, ensure_ascii=False)

print("scopus.json saved")
print("Documents:", len(papers))
print("Total citations:", total_citations)