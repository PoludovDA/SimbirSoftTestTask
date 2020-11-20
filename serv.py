from flask import Flask, render_template, send_file, request
from PIL import Image
from io import BytesIO
import os
from random import randint
import requests
import urllib.request
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
import urllib3
from datetime import datetime
import os.path

def check_file(track):
    count = 1
    while os.path.isfile(track + str(count) +'.jpg'):
        count += 1
    true_name = track + str(count) +'.jpg'
    return true_name

serv = Flask(__name__)
serv.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
serv.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(serv)

class Histories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(20), nullable=False)
    processed_image = db.Column(db.String(100))
    url_adr = db.Column(db.String(300))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

cat_folder = 'templates/images/cat/'
dog_folder = 'templates/images/dog/'
fox_folder = 'templates/images/fox/'

@serv.route('/')
def root():
    return render_template('index.html')


@serv.route('/animal/cat')
def cat_image():
    type_a = 'cat'
    URL = 'http://aws.random.cat/'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def get_html(url, params=''):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('img')
        return item['src']

    html = get_html(URL)
    url = get_content(html.text)
    img = urllib.request.urlopen(url).read()
    track = 'templates/images/cat/cat_img'
    name = check_file(track)
    history_cat = Histories(animal_type=type_a, processed_image=name, url_adr=url)
    db.session.add(history_cat)
    db.session.commit()
    out = open(name, "wb")
    out.write(img)
    out.close
    img_io = BytesIO()
    cat_files = os.listdir(cat_folder)
    image_pill = Image.open(cat_folder+cat_files[len(cat_files)-1])
    image_pil_convert = image_pill.convert('L')
    image_pil_convert.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@serv.route('/animal/dog')
def dog_image():
    type_a = 'dog'

    URL = 'https://shibe.online/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def get_html(url, params=''):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('img', class_='shibe__image')
        return item['src']

    html = get_html(URL)
    url = get_content(html.text)
    p = requests.get(url)
    track = 'templates/images/dog/dog_img'
    name = check_file(track)
    history_dog = Histories(animal_type=type_a, processed_image=name, url_adr=url)
    db.session.add(history_dog)
    db.session.commit()
    out = open(name, "wb")
    out.write(p.content)
    out.close()

    img_io = BytesIO()
    dog_files = os.listdir(dog_folder)
    image_pill = Image.open(dog_folder+dog_files[len(dog_files)-1])
    image_pil_convert = image_pill.convert('L')
    image_pil_convert.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@serv.route('/animal/fox')
def fox_image():
    type_a = 'fox'

    URL = 'https://randomfox.ca/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    def get_html(url, params=''):
        r = requests.get(url, headers=HEADERS, params=params)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('img', id="fox_img_link")
        return item['src']

    html = get_html(URL)
    img = get_content(html.text)
    p = requests.get(img)
    track = 'templates/images/fox/fox_img'
    name = check_file(track)
    history_fox = Histories(animal_type=type_a, processed_image=name, url_adr=img)
    db.session.add(history_fox)
    db.session.commit()
    out = open(name, "wb")
    out.write(p.content)
    out.close()

    img_io = BytesIO()
    fox_files = os.listdir(fox_folder)
    image_pill = Image.open(fox_folder+fox_files[len(fox_files)-1])
    image_pil_convert = image_pill.convert('L')
    image_pil_convert.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@serv.route('/history', methods=['GET', 'POST'])
def show_history():
    histories = Histories.query.order_by(desc(Histories.created)).all()
    return render_template('history.html', histories=histories)

@serv.route('/history/static')
def watch_img():
    histories = Histories.query.order_by(desc(Histories.created)).all()
    return render_template('watch.html', histories=histories)


if __name__ == '__main__':
    serv.run(debug=True)
