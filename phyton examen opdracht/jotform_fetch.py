import requests
import json
import csv

class JotformAPI:
    BASE_URL = "https://eu-api.jotform.com/"  

    def __init__(self, api_key, form_id):
        """Initialiseert de JotformAPI klasse met API-sleutel en formulier-ID."""
        if not api_key or not form_id:
            raise ValueError("API-sleutel en Form ID zijn vereist.")
        self.api_key = api_key
        self.form_id = form_id

    def get_submissions(self):
        """Haalt inzendingen op van het formulier via de API."""
        url = f"{self.BASE_URL}/form/{self.form_id}/submissions"
        params = {"apiKey": self.api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Fout bij het ophalen van gegevens: {e}")
            return None

    def print_submissions_json(self):
        """Print de hele JSON response netjes op het scherm."""
        data = self.get_submissions()
        if data:
            print("Inzendingen in JSON-formaat:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
        else:
            print("Geen data om te tonen.")

    def save_submissions_to_file(self, filename="submissions.json"):
        """Slaat de JSON response op in een bestand."""
        data = self.get_submissions()
        if data:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"Data succesvol opgeslagen in '{filename}'")
            except IOError as e:
                print(f"Fout bij het opslaan van het bestand: {e}")
        else:
            print("Geen data om op te slaan.")

    def save_submissions_to_csv(self, filename="submissions.csv"):
        """Slaat inzendingen op als CSV-bestand."""
        data = self.get_submissions()
        if not data or "content" not in data:
            print("Geen data om op te slaan.")
            return

        try:
            submissions = data["content"]
            if not submissions:
                print("Geen inzendingen gevonden.")
                return

            
            first_answers = submissions[0]["answers"]
            fieldnames = [f"{v['name']} (ID: {k})" for k, v in first_answers.items()]

            with open(filename, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for submission in submissions:
                    row = {
                        f"{v['name']} (ID: {k})": v.get("answer", "")
                        for k, v in submission["answers"].items()
                    }
                    writer.writerow(row)

            print(f"Data succesvol opgeslagen als CSV in '{filename}'")
        except IOError as e:
            print(f"Fout bij het opslaan van CSV: {e}")


API_KEY = "b39f0630f2e8a42a2c39e40adceb1a21"
FORM_ID = "250933582270356"

if __name__ == "__main__":
    jotform = JotformAPI(API_KEY, FORM_ID)
    jotform.print_submissions_json()
    jotform.save_submissions_to_file("submissions.json")
    jotform.save_submissions_to_csv("submissions.csv")
