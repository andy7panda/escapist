# README #

A small and simple script to transfer [bloger.by](bloger.by) hosted webblog to Wordpress standalone blog.

It is able to:

* scrap any bloger.by hosted webblog,
* save images into structured folders and
* save articles into CSV file, importable into Wordpress blog

### Instructions ###

* Change credentials.py according to your needs
* Run this to save a list of articles into file:
```
scrap_url_list(BLOGGER_BY_URL, 17, reversed_order=True)
```
* Run this to save articles:

```
scrap_articles()
```