from django.shortcuts import render

from . import util
import re


def index(request):
	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def wiki_page(request, title):
	description = util.get_entry(title.capitalize())

	if title == "css" or title == 'html':
		description = util.get_entry(title.upper())

	array = re.split('\n+', description)

	description = description[len(title) + 2:]

	array[0] = array[0].replace('#', '<h1>', 1) + '</h1>'

	for i in range(len(array)):
		num = array[i].count('[')

		if num >= 1:
			matches = re.findall(r'(\[\w+\]\(\/wiki\/\w+\))', array[i])
			for j in range(num):
				first = array[i].find('[')
				second = array[i].find(']')
				text_link = array[i][first + 1:second]
				href = f"/wiki/{text_link.lower()}"
				array[i] = array[i].replace(matches[j], f"<a href={href}> {text_link} </a>")
			array[i] = '<p>' + array[i] + '</p>'

	description = "\n".join(array)

	return render(request, "encyclopedia/pages.html", {
		"title": title.capitalize(),
		"description": description,
	})
