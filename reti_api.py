
import bs4 as bs
import urllib.request
import requests
import request
from flask import Flask, request
from flask_restful import Resource, Api

#Init flask
app = Flask(__name__)
api = Api(app)
PORT = 9544


class Cerca(Resource):

    def get(self, nome):
        links = []
        print("sadaadasd")
        print(nome)
        nome = "https://www.nientepopcorn.it/cerca-un-film/?titolo="+nome
        try:
            sauce = urllib.request.urlopen(nome).read()
            soup = bs.BeautifulSoup(sauce, 'html.parser')
            for item in soup.find_all('a', 'btn_np'):
                print(str(item))
                link = item.get('href')
                links.append(link)
        except urllib.error.HTTPError as err:

            if err.code == 404:
                links = []

        return {"status": 200, "links": links}, 200

class Cerca_Locandine(Resource):

    def get(self, user_state, filtraggio):
        URL = "https://www.nientepopcorn.it/PAGINA-NON-TROVATA"
        photos = []
        links = []
        titoli = []
        posizioni = []
        print(user_state+" "+filtraggio)
        if(user_state == "6"):
            URL = "https://www.nientepopcorn.it/classifiche-film/film-Anno/i-migliori-film-del-"+filtraggio
        elif (user_state == "4"):
            URL = "https://www.nientepopcorn.it/classifiche-film/Nazione/migliori-film-"+filtraggio
        elif user_state == "5":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/film-"+filtraggio
        elif user_state == "5.1":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/"+filtraggio
        elif user_state == "5.2":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/classifica-migliori-film-"+filtraggio
        elif user_state == "7":
            URL = "https://www.nientepopcorn.it/classifiche-serie-tv/classifica-serie-tv-"+filtraggio
        elif user_state == "8":
            URL = "https://www.nientepopcorn.it/classifiche-serie-tv/Genere-serie-tv/classifica-serie-tv-"+filtraggio

        print(URL)
        try:
            sauce = urllib.request.urlopen(URL).read()
            soup = bs.BeautifulSoup(sauce, 'html.parser')
            for item in soup.find_all('ul',{"id":"chart"}):
                answer = ''.join(item.text)
                for posizione in item.find_all('li'):
                    posizioni.append(posizione.get('id').split('_')[1])
                for film in item.find_all('div', 'rated_locandina'):
                    for c in film.find_all('img'):
                        photos.append(c.get('data-original'))

                    for c in film.find_all('a'):
                        titoli.append(c.get('title'))
                        links.append(c.get('href'))


            i = True
        except urllib.error.HTTPError as err:

            if err.code == 404:
                i = False
                print("Pagina non trovata...")
        return {"status": 200, "links": links, "photos": photos, "titoli": titoli, "posizioni": posizioni}, 200



class Scorri_Pagine(Resource):

    def get(self, user_state, page, filtraggio):
        URL = "https://www.nientepopcorn.it/PAGINA-NON-TROVATA"
        photos = []
        links = []
        titoli = []
        posizioni = []
        if(user_state == "6"):
            URL = "https://www.nientepopcorn.it/classifiche-film/film-Anno/i-migliori-film-del-"+filtraggio
        elif (user_state == "4"):
            URL = "https://www.nientepopcorn.it/classifiche-film/Nazione/migliori-film-"+filtraggio
        elif user_state == "5":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/film-"+filtraggio
        elif user_state == "5.1":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/"+filtraggio
        elif user_state == "5.2":
            URL = "https://www.nientepopcorn.it/classifiche-film/Genere-film/classifica-migliori-film-"+filtraggio
        elif user_state == "7":
            URL = "https://www.nientepopcorn.it/classifiche-serie-tv/classifica-serie-tv-"+filtraggio
        elif user_state == "8":
            URL = "https://www.nientepopcorn.it/classifiche-serie-tv/Genere-serie-tv/classifica-serie-tv-"+filtraggio

        if user_state == "4":
            URL = URL+"?start="+str(int(page)-1)+"0"
        else:
            URL = URL+"/page/"+page+"/"
            print (URL)
        try:
            sauce = urllib.request.urlopen(URL).read()
            soup = bs.BeautifulSoup(sauce, 'html.parser')
            for item in soup.find_all('ul',{"id":"chart"}):
                answer = ''.join(item.text)
                for posizione in item.find_all('li'):
                    posizioni.append(posizione.get('id').split('_')[1])
                for film in item.find_all('div', 'rated_locandina'):
                    for c in film.find_all('img'):
                        photos.append(c.get('data-original'))

                    for c in film.find_all('a'):
                        titoli.append(c.get('title'))
                        links.append(c.get('href'))
        except urllib.error.HTTPError as err:
            print(err)
            bot.sendMessage(from_id,"Classifica terminata...")

        return {"status": 200, "links": links, "photos": photos, "titoli": titoli, "posizioni": posizioni}, 200



class Stampa_Trama(Resource):

    def get(self, link):
        link = link.replace('£', '/')
        try:
            sauce = urllib.request.urlopen(link).read()
            soup = bs.BeautifulSoup(sauce, 'html.parser')
            for item in soup.find_all('p','trama' ):
                answer = ''.join(item.text)

            for item in soup.find_all('div','locandina_sf' ):
                i = 0
                for links in item:
                    if i == 0:
                        utile = links.get('src')
                    i = i+1

        except urllib.error.HTTPError as err:
            print("error")
        return {"status": 200, "utile": utile, "answer": answer}, 200


api.add_resource(Cerca, '/<nome>')
api.add_resource(Cerca_Locandine, '/tipologia/<user_state>/<filtraggio>')
api.add_resource(Scorri_Pagine, '/tipologia/page/<user_state>/<page>/<filtraggio>')
api.add_resource(Stampa_Trama, '/trama/<link>')
#api.add_resource(ApiGoogle, '/signup/')

if __name__ == '__main__':


        app.run(host='127.0.0.1', port=PORT)
