import csv
import requests
from bs4 import BeautifulSoup

def scrape_internshala_jobs():
    url = 'https://internshala.com/internships'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting job details
    job_cards = soup.find_all('div', class_='individual_internship_header')

    roles = []
    descriptions = []
    skills_required = []
    stipends = []
    links = []

    for card in job_cards[:10]:
        role = card.find('div', class_='company').text.strip()
        skills = card.find('div', class_='internship_other_details_container').text.strip()
        stipend = card.find('span', class_='stipend').text.strip()
        link = 'https://internshala.com' + card.find('a')['href']

        roles.append(role)
        skills_required.append(skills)
        stipends.append(stipend)
        links.append(link)

    desc_card = soup.find_all('div', class_='individual_internship_details  individual_internship_internship')
    for desc in desc_card:
        description = desc.find('div', class_='internship_other_details_container').text.strip()

    descriptions.append(description)
    

    return zip(roles, descriptions, skills_required, stipends, links)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Roles", "Description", "Skills required", "Stipend", "Link"])

        for row in data:
            writer.writerow(row)

def main():
    internshala_jobs = scrape_internshala_jobs()
    save_to_csv(internshala_jobs, 'internshala_jobs.csv')

if __name__ == "__main__":
    main()