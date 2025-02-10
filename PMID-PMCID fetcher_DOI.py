import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Headers for HTTP request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Open the input file with DOIs
with open('dois.txt', 'r') as file:
    dois = file.readlines()

# Open the output file in append mode
with open('output.csv', 'a') as output_file:
    for doi in tqdm(dois):
        doi = doi.strip()
        try:
            # Request to PubMed
            response = requests.get(f'https://pubmed.ncbi.nlm.nih.gov/?term={doi}', headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP issues
            
            # Parse the response with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract PMID
            pmid = soup.find('span', class_='identifier pubmed').find('strong').text.strip() if soup.find('span', class_='identifier pubmed') else 'None'

            # Extract PMCID
            pmc_id = soup.find('span', class_='identifier pmc').find('a').text.strip() if soup.find('span', class_='identifier pmc') else 'None'

        except requests.exceptions.RequestException as e:
            print(f"Request failed for DOI {doi}: {e}")
            pmid = 'None'
            pmc_id = 'None'
        except Exception as e:
            print(f"Parsing failed for DOI {doi}: {e}")
            pmid = 'None'
            pmc_id = 'None'

        # Write to the output file
        output_file.write(f"{doi},{pmid},{pmc_id}\n")

print("Processing complete. Data saved to 'data.csv'.")
    


