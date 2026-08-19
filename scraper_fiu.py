import requests
import json

BASE_URL = "https://www.cis.fiu.edu/wp-json/wp/v2/staff-member"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cis.fiu.edu/faculty-staff/"
}

FACULTY_CATEGORIES = {
    543, 544, 545, 549, 550, 551
}


def scrape_faculty():

    professors = []

    for page_number in range(1, 11):

        url = f"{BASE_URL}?page={page_number}"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        for professor in data:

            categories = professor["staff-member-category"]

            if not FACULTY_CATEGORIES.isdisjoint(categories):

                professors.append({
                    "Name": professor["title"]["rendered"].strip(),
                    "Title": professor["metadata"]["title"],
                    "Email": professor["metadata"]["email"],
                    "URL": professor["link"]
                })

    professors.sort(
        key=lambda professor: professor["Name"].lower()
    )

    return professors


if __name__ == "__main__":

    professors = scrape_faculty()

    with open("faculty.json", "w", encoding="utf-8") as file:
        json.dump(
            professors,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {len(professors)} faculty members.")
