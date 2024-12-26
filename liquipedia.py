import json
import re

import requests
import urllib.parse

def fetch_tournament_info(tournament_name):
    # NOTE FOR TOMORROW:
    # Need to do a query that uses the search function to find the tournament
    # THEN parse a tournament by ID
    # BUT you need to save the tournament HTML for later!
    # They dont like you doing multiple queries for the same tournament if you can prevent it!
    base_url = f"https://liquipedia.net/overwatch/api.php"
    headers = {
        "User-Agent": "OverwatchOverlayHelper/1.0 (oligeenty@gmail.com)",
        'Accept-Encoding': 'gzip'
    }
    params = {
        "action": "query",
        "format": "json",
        "titles": urllib.parse.quote_plus(tournament_name),
        "prop": "revisions",
        "rvprop": "content",
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page_id, page_data in pages.items():
            if page_id != "-1":  # "-1" indicates the page does not exist
                return {
                    "title": page_data.get("title", "Unknown"),
                    "content": page_data.get("revisions", [{}])[0].get("*", "No content available"),
                }
        return {"error": "Tournament not found"}
    except requests.RequestException as e:
        return {"error": str(e)}


def parseBans():
    data = json.load(open("data.json"))
    html = data["parse"]["text"]["*"]
    parts = html.split("brkts-popup-comment\" style=\"font-size:85%;white-space:normal\">")
    partsFiltered = []
    for i, part in enumerate(parts):
        if i == 0:
            continue
        partFiltered = part.split("</div>")
        partFiltered = re.sub(r"</?(?!br\b)[^>]+>", "", partFiltered[0])
        partFiltered = partFiltered.replace("  "," ").replace("<br /> ", "\n")
        partsFiltered.append(partFiltered)

    print(partsFiltered[21])

if __name__ == "__main__":
    parseBans()
    # tournament = "Overwatch League 2023 Playoffs"
    # result = fetch_tournament_info(tournament)
    #
    # if "error" in result:
    #     print(f"Error: {result['error']}")
    # else:
    #     print(f"Title: {result['title']}")
    #     print(f"Content: {result['content']}")
