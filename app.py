from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrap', methods=['POST'])
def scrap():
    if request.method == 'POST':
        url = request.form.get('url')
        url = 'https://www.geeksforgeeks.org/'

        uClient = uReq(url)
        page_html_date = uClient.read()
        uClient.close()

        parsed_data = soup(page_html_date, 'html.parser')
        containers = parsed_data.findAll('div', {'class': 'site-content'})
        container = containers[0]

        articles = container.findAll('article')

        data = []
        for article in articles:
            document = {}
            temp = []

            document['post_title'] = article.find('h2').text.strip()

            x = article.find('a', {'title': 'Medium'})
            if x is None:
                document['post_ratings'] = 'No ratings available'
            else:
                document['post_ratings'] = x.text.strip()

            post_tags = article.findAll('div', {'class': 'practiceButton'})
            for x in post_tags:
                temp.append(x.text.strip())
            document['tags'] = temp
            data.append(document)

        return render_template('results.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)