# Reading List Word Cloud

This project generates word clouds from a Goodreads export (or similar CSV) of book titles using page counts as weights. 

Files included:

- `Dockerfile` — builds a Python 3.11 image with system deps required by `wordcloud`.
- `requirements.txt` — Python dependencies.
- `.dockerignore` — reduces Docker build context.
- `notebook.ipynb` — contains the word cloud generation code and example usage.

# Quick start — build and run the Docker image

```bash
# from project root 
docker build -t book-wordcloud:latest .

# run Jupyter Lab and mount the project so you can edit files from the host
docker run --rm -p 8888:8888 -v "$(pwd)":/app book-wordcloud:latest
```

Open http://localhost:8888 in your browser (Jupyter Lab is started by default).

Notes
- The `wordcloud` package requires small C libraries; the `Dockerfile` installs the build deps (`libfreetype6-dev`, `libpng-dev`, etc.).
- To run the word cloud code interactively, open `notebook.ipynb` in Jupyter Lab and run the cells.
- If you prefer running as a script, move the functions from the notebook into a `.py` module (e.g., `wordcloud_generator.py`) and call them from a small runner script. Example:

```python
# wordcloud_generator.py
from your_module import create_book_title_wordcloud, save_wordcloud
wc1, wc2 = create_book_title_wordcloud('word_cloud/yun_goodreads_library_export.csv')
save_wordcloud(wc1, 'word_cloud/book_titles_method1.png')
```

Customizing container behavior
- To run a specific Python script instead of Jupyter, change the `CMD` in `Dockerfile` or override it at runtime: `docker run ... book-wordcloud:latest python path/to/script.py`.

If you want, I can:
- Add the small `wordcloud_generator.py` runner file and example `docker run` command to execute it, or
- Change the default `CMD` in `Dockerfile` to run a script instead of Jupyter Lab.
