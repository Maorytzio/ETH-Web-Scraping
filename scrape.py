import csv
import glob
import json
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_uniswap_doc_to_csv():
    uni_res = requests.get("https://docs.uniswap.org/contracts/v3/reference/deployments")
    uni_soup = BeautifulSoup(uni_res.text, "html.parser")

    # scrape Chains
    ths = uni_soup.find_all('th')
    chains = ths[1].text.split(",")
    celo_chain = ths[2].text.strip(" Address")
    chains.append(celo_chain)

    # for each row scrape data, and add it to Pandas DataFrame
    table = uni_soup.find('table')
    df = pd.DataFrame(columns=['Chain', 'Address', 'Label'])
    for row in table.tbody.find_all('tr'):

        columns = row.find_all('td')
        label = columns[0].text
        address = columns[1].text
        celo_address = columns[2]

        for chain in chains[:len(chains) - 1]:
            df = df.append(
                {'Chain': chain.strip("Address"), 'Address': address, 'Label': label}, ignore_index=True)

        df = df.append(
            {'Chain': chains[-1], 'Address': celo_address, 'Label': label}, ignore_index=True)

    df.to_csv(r'.\uniswap_doc.csv', index=False)


def save_json_to_csv():
    with open("info.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Chain", "Address", "Label"])

        data_dir = os.path.abspath("data")
        for filename in glob.iglob(f'{data_dir}/*'):
            with open(filename) as f:
                data = json.loads(f.read())
                writer.writerow([data["name"], data["address"], data["description"]])
