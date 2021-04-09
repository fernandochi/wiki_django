from django.shortcuts import render

from . import util
import re


def index(request):
	if request.method == 'POST':
		querry = request.POST['q'].lower()

		all_pages = util.list_entries()

		for i in range(len(all_pages)):
			if querry in all_pages[i].lower():
				return wiki_page(request, all_pages[i])

		return render(request, "encyclopedia/index.html", {
			"entries": util.list_entries()
		})

	return render(request, "encyclopedia/index.html", {
		"entries": util.list_entries()
	})


def wiki_page(request, title):
	description = util.get_entry(title.capitalize())

	if title == "css" or title == 'html':
		description = util.get_entry(title.upper())

	array = re.split('\n+', description)

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

		if "##" in array[i]:
			array[i] = array[i].replace('##', '<h2>') + '</h2>'

		if '**' in array[i]:
			count = array[i].count('**')
			for j in range(count):
				if j % 2:
					array[i] = array[i].replace('**', '</b>', 1)
				else:
					array[i] = array[i].replace('**', '<b>', 1)

		if '*' in array[i]:
			array[i] = array[i].replace('*', '<li>') + '</li>'

	description = "\n".join(array)

	return render(request, "encyclopedia/pages.html", {
		"title": title.capitalize(),
		"description": description,
	})


def search(request):
	if request.method == 'POST':
		query = request.POST['q']

		all_pages = [entries.lower for entries in util.list_entries()]

		if query.lower() in all_pages:
			...

	# 	user = authenticate(request, username=username, password=password)
	# 	if user is not None:
	# 		login(request, user)
	# 		return HttpResponseRedirect(reverse('index'))
	# 	return render(request, "users/login.html", {
	# 		"message": 'Invalid Credentials'
	# 	})
	# return render(request, "users/login.html")
