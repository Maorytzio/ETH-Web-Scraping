import json
import time

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_restful import Api
from selenium import webdriver

from scrape import scrape_uniswap_doc_to_csv, save_json_to_csv

app = Flask(__name__)
api = Api(app)


@app.route('/scrape-addresses', methods=['POST'])
def scrape():
    addresses = json.loads(request.data)
    result = {}

    for address in addresses:
        etherscan_url = f"https://etherscan.io/address/{address}/"
        web_driver = webdriver.Chrome()
        web_driver.get(etherscan_url)
        time.sleep(1)

        soup = BeautifulSoup(web_driver.page_source, 'html.parser')
        try:
            tag1 = soup.find_all("a", class_="mb-1")[0].text
            tag2 = soup.find_all("a", class_="mb-1")[1].text
            tag3 = soup.select("span.u-label.u-label--secondary")[0].text

            tags = {"tag1": tag1, "tag2": tag2, "tag3": tag3}
            result[address] = tags
        except:  # continue when URL is not matching, Assignment criteria
            continue
        else:
            print(tags)

    return jsonify(result)


if __name__ == '__main__':
    save_json_to_csv()
    scrape_uniswap_doc_to_csv()
    app.run(debug=True)
