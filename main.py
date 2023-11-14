import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from googletrans import Translator


def crawl_text_from_html_file(file_path, target_prefix='article_content_article_body'):
    try:
        # Set up Chrome options
        chrome_options = Options()

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(file_path)

        driver.implicitly_wait(10)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        target_elements = soup.find_all(class_=re.compile(f'^{re.escape(target_prefix)}'))

        text_content = ' '.join(line.strip() for element in target_elements for line in element.stripped_strings)

        driver.quit()

        return text_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def translate_to_vietnamese(text):
    translator = Translator()

    # Check if the text is None or empty
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


html_file_path = 'file:///C:/Users/Admin/Downloads/Signs%20and%20Symptoms%20of%20Dog%20Food%20Allergies%20_%20PetMD.html'
result = crawl_text_from_html_file(html_file_path, target_prefix='article_content_article_body')

if result:
    translated_result = translate_to_vietnamese(result)

    save_to_json({'text_content': translated_result}, 'output.json')
    print("Data saved to output.json")

