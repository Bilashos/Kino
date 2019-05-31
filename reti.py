import telepot
from config_reti import TOKEN
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import bs4 as bs
import urllib.request
import json
from pprint import pprint
import time
from apiclient.discovery import build
import requests
import os
import request

class MessageHandler:
    # Preserve all different user stages between messages
    URL = ""
    USER_STATE = {}
    counter = 1

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        photos = []
        links = []
        titoli = []
        posizioni = []

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Trama', callback_data='trama')],
                 ])


        # Check user state
        try:
            self.USER_STATE[chat_id]
        except KeyError:
            self.USER_STATE[chat_id] = 0

        # se messaggio ricevuto è un testo
        if content_type == "text":

            input_msg = msg['text']

            if input_msg == "/start":
            # messaggio di benvenuto
                bot.sendMessage(chat_id, "Benvenuto "+msg['chat']['first_name']+" questo bot ti aiuterà a scegliere il film che più è adatto a te")
                send_options(self, chat_id)

            # Se è scritto HOME, messaggio di inizio.
            elif input_msg == "HOME" or input_msg == "/HOME":
                send_options(self, chat_id)

            # apre la schermata di ricerca di un film
            elif input_msg == "Ricerca Regista, Film, SerieTV" and self.USER_STATE[chat_id] == 1:
                reply_markup = ReplyKeyboardRemove()
                bot.sendMessage(chat_id, 'Digita il film che vuoi cercare...\nSe sai già il titolo... ', reply_markup=reply_markup)
                self.USER_STATE[chat_id] = 3.1

            # e in caso di corrispondenza stampa la lista dei film
            elif self.USER_STATE[chat_id] == 3.1:
                r = requests.get("http://127.0.0.1:9544/{0}".format(input_msg.replace(' ', '-')))
                myresult = r.json()
                links = myresult['links']
                stampa_lista_film(chat_id, links)

            # apre la schermata di ricerca delle serie tv
            elif input_msg == "SerieTV" and self.USER_STATE[chat_id] == 1:
                entries = [["Genere", "Piu Viste"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id, 'Seleziona il filtraggio...', reply_markup=markup)
                self.USER_STATE[chat_id] = 7

            # filtro delle serieTV in base al Genere
            elif input_msg == "Genere" and self.USER_STATE[chat_id] == 7:
                entries = [["Drama", "Science Fiction","Fantasy"],["Crime","Animation","Comedy"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id, 'Seleziona il filtraggio...', reply_markup=markup)
                self.USER_STATE[chat_id] = 8

            # stampa le locandine delle varie serietv del genere selezionato
            elif self.USER_STATE[chat_id] == 8:
                r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                myresult = r.json()
                myresult = r.json()
                photos = myresult['photos']
                links = myresult['links']
                titoli = myresult['titoli']
                posizioni = myresult['posizioni']
                cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)

            # cerca e stampa le serieTV più Viste
            elif(input_msg == "Piu Viste" and self.USER_STATE[chat_id] == 7):
                r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                myresult = r.json()
                myresult = r.json()
                photos = myresult['photos']
                links = myresult['links']
                titoli = myresult['titoli']
                posizioni = myresult['posizioni']
                cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)

            # apre la schermata dei film con i vari modi di filtraggio delle ricerche
            elif input_msg == "Film" and self.USER_STATE[chat_id] == 1:
                entries = [["Genere", "Anno"],["Nazione"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id, 'Seleziona il filtraggio...', reply_markup=markup)
                self.USER_STATE[chat_id] = 2

            # Filtro in base all'Anno
            elif input_msg == "Anno" and self.USER_STATE[chat_id] == 2:
                entries = [["2019"],["2018"],["2017"],["2016"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id, 'Seleziona l\'Anno', reply_markup=markup)
                self.USER_STATE[chat_id] = 6

            # Restituisce i film dell'Anno selezionato
            elif self.USER_STATE[chat_id] == 6:
                r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                myresult = r.json()
                myresult = r.json()
                photos = myresult['photos']
                links = myresult['links']
                titoli = myresult['titoli']
                posizioni = myresult['posizioni']
                cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)

            # filtro dei film in base al Genere
            elif input_msg == "Genere" and self.USER_STATE[chat_id] == 2:
                entries = [["Drammatici", "Commedie","Biografici"],["Animazione cartoni animati","Fantascienza","Horror"],["Musical","Documentari","Supereroi"],["Western","Guerra","Thriller Suspence"],["Per tutta la famiglia"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id,'Scegli l\'opzione', reply_markup=markup)
                self.USER_STATE[chat_id] = 5

            # filtro dei Film in base alla nazione
            elif input_msg == "Nazione" and self.USER_STATE[chat_id] == 2:
                entries = [["Italiani", "Giapponesi", "Cinesi Hong-kong Taiwan"],["Francesi","Russi","Australiani"],["HOME"]]
                markup = ReplyKeyboardMarkup(keyboard=entries)
                bot.sendMessage(chat_id,'Scegli l\'opzione', reply_markup=markup)
                self.USER_STATE[chat_id] = 4

            # restitusce i film della nazione cercata
            elif self.USER_STATE[chat_id] == 4:
                r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                print(str(r))
                myresult = r.json()
                photos = myresult['photos']
                links = myresult['links']
                titoli = myresult['titoli']
                posizioni = myresult['posizioni']
                cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)

            # Restituisce i migliori film di ogni Genere
            elif self.USER_STATE[chat_id] == 5 and input_msg != "HOME":
                if input_msg == "Commedie":
                    entries = [["Le commedie piu belle"],["migliori commedie 2018"],["migliori commedie 2017"],["migliori commedie 2016"],["HOME"]]
                    markup = ReplyKeyboardMarkup(keyboard=entries)
                    bot.sendMessage(chat_id,'Scegli l\'opzione', reply_markup=markup)
                    self.USER_STATE[chat_id] = 5.1

                else:
                    if input_msg == "Fantascienza":
                        input_msg = "fantascienza-sci-fi"
                    r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                    myresult = r.json()
                    photos = myresult['photos']
                    links = myresult['links']
                    titoli = myresult['titoli']
                    posizioni = myresult['posizioni']
                    if(photos == []):
                        self.USER_STATE[chat_id] = 5.2
                        r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                        myresult = r.json()
                        photos = myresult['photos']
                        links = myresult['links']
                        titoli = myresult['titoli']
                        posizioni = myresult['posizioni']
                    self.USER_STATE[chat_id] = 5

                    cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)


            elif self.USER_STATE[chat_id] == 5.1:
                r = requests.get("http://127.0.0.1:9544/tipologia/{0}/{1}".format(self.USER_STATE[chat_id], input_msg.replace(' ', '-')))
                myresult = r.json()
                photos = myresult['photos']
                links = myresult['links']
                titoli = myresult['titoli']
                posizioni = myresult['posizioni']
                cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg)

            else:
                bot.sendMessage(chat_id,"Comando non trovato...")

########################################################################################################################################
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        photos = []
        links = []
        titoli = []
        posizioni = []
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='Trama', callback_data='trama')],
                 ])



        if query_data == "trama":
            link = msg['message']['caption'].split(':')[3]+":"+msg['message']['caption'].split(':')[4]
            message_id =  msg['message']['message_id']

            stampa_trama(link, from_id, message_id)

        elif self.USER_STATE[from_id] == 3.1:
            self.URL = "https://www.nientepopcorn.it"+query_data
            cerca_film_regista_serie(self, from_id)

        else:
            input_msg =  msg['message']['text'].split(':')[0]
            print(self.URL)
            r = requests.get("http://127.0.0.1:9544/tipologia/page/{0}/{1}/{2}".format(self.USER_STATE[from_id], query_data, input_msg))
            print(r)
            myresult = r.json()
            photos = myresult['photos']
            links = myresult['links']
            titoli = myresult['titoli']
            posizioni = myresult['posizioni']



            self.counter = query_data
            i = 0
            for element in photos:
                c = bot.sendPhoto(from_id, element, "Titolo: "+titoli[i]+"\nPosizione: "+posizioni[i]+"\nLink: https://www.nientepopcorn.it"+links[i],reply_markup = keyboard)
                print(c['message_id'])
                i = i + 1
            if(self.counter == '1'):
                next = InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='succ>>', callback_data=str(int(self.counter)+1))],
                         ])
            else:
                next = InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text='<<prec', callback_data=str(int(self.counter)-1)),
                             InlineKeyboardButton(text='succ>>', callback_data=str(int(self.counter)+1))],
                         ])
            bot.sendMessage(from_id, input_msg+": "+"Pagina "+str(self.counter),reply_markup = next)



########################################################################################################################################
def send_options(self, chat_id):

    entries = [["Film", "SerieTV"],["Ricerca Regista, Film, SerieTV"]]
    markup = ReplyKeyboardMarkup(keyboard=entries)
    bot.sendMessage(chat_id,'Scegli l\'opzione', reply_markup=markup)
    self.USER_STATE[chat_id] = 1
########################################################################################################################################
def stampa_trama(link, chat_id, message_id):
    link = link.replace('/', '£').replace(' ', '')
    r = requests.get("http://127.0.0.1:9544/trama/{0}".format(link))
    print(r)
    myresult = r.json()
    try:
        bot.editMessageCaption((chat_id, message_id), "Trama:\n"+myresult['answer'])
    except telepot.exception.TelegramError as err:
        if err.error_code == 400:
            bot.editMessageCaption((chat_id, message_id), "Trama:\nLa trama è lunga ti invio un messaggio")
            bot.sendPhoto(chat_id, myresult['utile'])
            bot.sendMessage(chat_id, "Trama:\n"+myresult['answer'])
def stampa_lista_film(chat_id, links):
    if links != []:
        for r in links:
            ricerca = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text='ricerca', callback_data=r)],
                     ])
            utile = r.split('/')[2].replace('-', ' ')
            bot.sendMessage(chat_id, utile, reply_markup=ricerca)

    else:
        bot.sendMessage(chat_id, "Nessun risultato per questa ricerca...\nRiprova oppure torna nella /HOME")
########################################################################################################################################
def cerca_film_regista_serie(self, chat_id):
    answer = ''
    link = self.URL
    link = link.replace('/', '£').replace(' ', '')
    r = requests.get("http://127.0.0.1:9544/trama/{0}".format(link))
    print(r)
    myresult = r.json()
    if(myresult['answer'] != ''):
        bot.sendPhoto(chat_id, myresult['utile'], "Trama:\n"+myresult['answer'])
    else:
        bot.sendMessage(chat_id, "Nessun film con questo nome è stato trovato!\nRiprova oppure torna nella /HOME")

########################################################################################################################################
def cerca_locandine(self, chat_id, photos, links, titoli, posizioni, input_msg):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text='Trama', callback_data='trama')],
             ])
    if photos != []:
        i = 0
        for element in photos:
            c = bot.sendPhoto(chat_id, element, "Titolo: "+titoli[i]+"\nPosizione: "+posizioni[i]+"\nLink: https://www.nientepopcorn.it"+links[i],reply_markup = keyboard)
            print(c['message_id'])
            i = i + 1
        self.counter = 1
        next = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='succ>>', callback_data=str(int(self.counter)+1))],
                 ])
        bot.sendMessage(chat_id, input_msg+": "+"Pagina "+str(self.counter),reply_markup = next)
    else:
        bot.sendMessage(chat_id, "Pagina NON trovata...")

########################################################################################################################################
handler = MessageHandler()
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat':handler.handle,
                  'callback_query': handler.on_callback_query})

while 1:
    time.sleep(10)
