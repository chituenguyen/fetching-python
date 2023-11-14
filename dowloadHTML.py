import requests


def save_html_from_url(url, output_file='output.html'):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(output_file, 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
            print(f"HTML saved to {output_file}")
        else:
            print(f"Failed to retrieve HTML. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage with a URL
url_to_scrape = 'https://www.freevpn.one/connect/'
save_html_from_url(url_to_scrape, output_file='output.html')
