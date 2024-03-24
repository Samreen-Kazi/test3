from flask import Flask, render_template, request
from libgen_api import LibgenSearch

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        if query:
            try:
                libgen = LibgenSearch()
                results = libgen.search_title(query)  # Search by title
                if not results:
                    results = libgen.search_author(query)  # Search by author if no results found by title
                if results:
                    book_info = []
                    count = 1
                    for result in results:
                        book_info.append({
                            'number': count,
                            'title': result.get('Title', ''),
                            'author': result.get('Author', ''),
                            'publisher': result.get('Publisher', ''),
                            'year': result.get('Year', ''),
                            'language': result.get('Language', ''),
                            'file_type': result.get('Extension', ''),
                            'file_size': result.get('Size', ''),
                            'download_link': result.get('Mirror_1', '')
                        })
                        count += 1
                    if book_info:
                        return render_template('results.html', book_info=book_info)
                    else:
                        return "No download links found for the given book or author."
                else:
                    return "No results found for the given book or author."
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "Please enter a book title or author."
    else:
        return render_template('index.html')
