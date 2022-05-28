from flask import Flask, render_template, redirect, url_for, request 
import random 
import requests
import os 

# Import wikipedia
import wikipedia as wiki 

#Import html
from lxml import html

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

# Main 
@app.route('/') 
def index():
    text = open('dane/xd.txt').read()
    return render_template("index.html", text=text)


@app.route('/flaga)

def flaga():
	create_folders()  

	# Flag.
	xd = random.choice(range(22))
	if 'Polska_Flaga__{}.jpg'.format(xd) not in os.listdir('static/flag_image/'):
		xd = 11
	flaga = os.path.join(app.config['UPLOAD_FOLDER'], 'flag_image/Polska_Flaga__{}.jpg'.format(xd))
	xdd = xd +1 
	if 'Polska_Flaga__{}.jpg'.format(xdd) not in os.listdir('static/flag_image/'):
		xdd = 11
	flaga2 = os.path.join(app.config['UPLOAD_FOLDER'], 'flag_image/Polska_Flaga__{}.jpg'.format(xdd))
	

	# Gather heroes.
	heroes = gather_heroes() 
	random.shuffle(heroes)

	return render_template("flaga.html", flaga=flaga, flaga2=flaga2, heroes=heroes)

def gather_heroes():

	# heroes = open(plik).readlines() 

	heroes = [
 		'Mikołaj Kopernik', 
 		'Witold Pilecki',
 		'Maria Skłodowska-Curie',
 		'Fryderyk Chopin',
        'Adolf Maria Bocheński'		
	]
	
	greetings = [
		'pozdrawia',
		'/wave',
		'/wink',
		'wita',
	]

	wiki.set_lang("pl")

	saved_heroes = os.listdir('saved_heroes')
	saved_heroes = [h.split('.')[0] for h in saved_heroes]

	for hero in heroes:
		if hero not in saved_heroes:

			# Get some info and link.
			some_info = wiki.page(hero)
			content = some_info.content.split('\n')[0:3] 
			info_intro = ' '.join(content) 
			url = '<a href="'+some_info.url+'">Poszukaj więcej info o: '+hero+"</a>"
			
			# Get what hero thinks.
			hero_think(hero)
			
			# Get & save images.
			images = some_info.images
			hero_images = [] 
			for image in images:
				if requests.get(image).status_code == 200:
					if image.endswith('jpg') or image.endswith('JPG') or image.endswith('jpeg'):
						# if hero.split(' ')[0][0:4] or hero.split(' ')[1][0:4] in image: 
						hero_images.append(image) 
			n_photos = 0
			for i, image_url in enumerate(hero_images):
				# if i < 3:
				n_photos += 1
				hero_str = '_'.join(hero.split())
				image_name = '{}_{}.jpg'.format(hero_str, n_photos)
				save_image(image_url, image_name)
				
			# Save all.
			with open('saved_heroes/'+hero+".hero", "w+") as f:
				f.write(hero + '\n')
				f.write(str(n_photos) + '\n') # '\n') 
				f.write(info_intro + '\n')
				f.write(url)

		else:
			greeting = random.choice(greetings)
			print(hero, greeting)

	heroes = []
	for hero_file in os.listdir('saved_heroes'):
		hero = {}
		some_info = open('saved_heroes/'+hero_file).readlines()
		hero['name'] = some_info[0]
		random_photo_nr = random.choice(range(int(some_info[1])))  #(1, 2)) 
		photo_nr = random_photo_nr
		if random_photo_nr == 0:
			photo_nr = 1 
		hero_str = '_'.join(hero['name'].split())
		hero['image'] = '{}_{}.jpg'.format(hero_str, photo_nr) #[:-1]
		if '{}_{}.jpg'.format(hero_str, photo_nr) not in os.listdir('static/hero_image/'):
			continue
		hero_quotes = open('hero_think/' + hero['name'][:-1] + ".hero").readlines()
		hero['quote'] = random.choice(hero_quotes)
		hero['description'] = '\n'.join(some_info[2:-1])
		hero['description'] = bold(hero['description'])
		hero['url'] = some_info[-1]
		heroes.append(hero)

	return heroes

#save_image
def save_image(image_url, image_name):
	image = requests.get(image_url)
	save_as = 'static/hero_image/{}'.format(image_name)
	if image.status_code == 200: 
		with open(save_as, 'wb') as ap:
			ap.write(image.content)
	return save_as

def bold(hero_info):

	nice = [
		'nauk',
		'gen',
		'zwy',
		'odk',
		'zał',
		'rod',
		'organizator',
		'astronom',
		'inżynier',
		'herbu',
		'wojska',
		'uczona',
		'nobla',
		'wybitniej',
		'romantyczny',
		'fizyk',
		'filozof',
		'kocha',
		'woli',
		'kawalerii',
		'skazany',
	]

	heroes = [
		'Kopernik', 
 		'Pilecki',
 		'Skłodowska-Curie',
 		'Chopin',
        'Bocheński'
	]

	for hero in heroes:
		nice.append(hero)


	right_desc = []
	words = [w for w in hero_info.split()]
	for w in words:
		for woah in nice:
			if w.startswith(woah):
				w = '<b>'+w+'</b>'
		right_desc.append(w)
	right_desc = " ".join(right_desc) 
	return right_desc

def hero_think(name):
	url_name = name.replace(' ', '_')
	url = 'https://pl.wikiquote.org/wiki/{}'.format(url_name)
	hero_wikiquotes = requests.get(url)
	with open('hero_think/'+name+".hero", "w+") as f:
		
		for line in hero_wikiquotes.text.split('\n'):
			if line.startswith('<h2>O'):
				continue
			if line.startswith('<ul><li>'):
				
				tree = html.fromstring(line)
				quote = tree.text_content().strip()
				
				if not quote.startswith('Opis') and not quote.startswith('Autor') and not quote.startswith('Źródło') and not quote.startswith('Zobacz'): 
					f.write(quote + '\n')
					print('-', quote)
				
def create_folders():
	os.system("mkdir static/hero_image")
	os.system("mkdir static/flag_image")
	os.system("mkdir saved_heroes")
	os.system("mkdir hero_think")


if __name__=="__main__":
    app.run(debug=True)
