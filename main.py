import re
import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import pandas as pd


def crawl_text_from_html(html_content, target_prefix='article_content_article_body'):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        target_elements = soup.find_all(class_=re.compile(f'^{re.escape(target_prefix)}'))

        text_content = ' '.join(line.strip() for element in target_elements for line in element.stripped_strings)

        return text_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def translate_to_vietnamese(text):
    translator = Translator()

    if not text:
        return None

    max_chars_per_request = 5000

    if len(text) <= max_chars_per_request:
        translation = translator.translate(text, dest='vi')
        return translation.text
    else:
        chunks = [text[i:i + max_chars_per_request] for i in range(0, len(text), max_chars_per_request)]
        translated_chunks = [translator.translate(chunk, dest='vi').text for chunk in chunks]
        return ' '.join(translated_chunks)


def save_to_json(data, filename='output.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def fetch_html_content(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# read data from excel to get link url
excel_file_path = 'file1.csv'

df = pd.read_csv(excel_file_path)

# fetching from link
for i in range(len(df["Url"])):
    url_to_scrape = df["Url"][i]
    html_content = fetch_html_content(url_to_scrape)

    if html_content:
        result = crawl_text_from_html(html_content, target_prefix='article_content_article_body')

        if result:
            translated_result = translate_to_vietnamese(result)

            output_data = {}
            output_file = 'output.json'

            try:
                with open(output_file, 'r', encoding='utf-8') as json_file:
                    output_data = json.load(json_file)
            except FileNotFoundError:
                pass
            output_data[df["post_name"][i]] = translated_result

            save_to_json(output_data, output_file)

            print("Data appended to output.json")

