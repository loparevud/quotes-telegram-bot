import requests, random, telebot
from bs4 import BeautifulSoup

bot = telebot.TeleBot('6756494812:AAFb9M1qrhpu0Pf11BH6yPLsXhxOIB6GSlc')
@bot.message_handler(commands=['quote', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я - чат-бот с цитатами великих людей')
    bot.send_message(message.chat.id, text=f"{'Введите фамилию и/или имя: '}")

    @bot.message_handler(content_types=['text'])
    def send_echo(message):

        Name = message.text
        site = requests.get('https://ru.citaty.net/poisk/?h=' + Name)
        html_text = BeautifulSoup(site.text, 'html.parser')
        alert = html_text.find('div', class_="alert alert-warning alert-block")
        alt_Name = html_text.find('p', class_='mb-12 font-semibold')
        if alert != None:
            bot.send_message(message.chat.id, text=f"{alert.text}")
        else:
            checkAuthor = html_text.find('div', class_="flex items-center mb-3")
            quotes_main = html_text.find_all('p', class_='blockquote-text')
            author_main = html_text.find_all('p', class_='blockquote-origin')
            length_main = len(author_main) - 1
            if checkAuthor is None:
                bot.send_message(message.chat.id,text='Я не совсем понял запрос, возможно вы ищете что-то вроде этого:' +
                                                      '\n' + '\n' + quotes_main[random.randint(0, length_main)].text + '\n' + '\n' +
                                                      author_main[random.randint(0, length_main)].text)
            else:
                author_site = requests.get(
                    'https://ru.citaty.net' + html_text.find('a', class_="w-10 mr-3 flex-none").get("href"))
                author_site_text = BeautifulSoup(author_site.text, 'html.parser')
                quotes = author_site_text.find_all('p', class_='blockquote-text')
                author = author_site_text.find_all('p', class_='blockquote-origin')
                length = len(author) - 1
                button_next = author_site_text.find('a', class_='page-link page-link-next iscroll-next')
                small_photo_search = author_site_text.find('div', class_='w-full sm:w-1/4 lg:w-1/3')
                i = 1
                while button_next != None:
                    author_site = requests.get('https://ru.citaty.net' + html_text.find('a', class_="w-10 mr-3 flex-none").get("href") + '?page=' + str(i))
                    i += 1
                    author_site_text = BeautifulSoup(author_site.text, 'html.parser')
                    button_next = author_site_text.find('a', class_='page-link page-link-next iscroll-next')
                    quotes = quotes + author_site_text.find_all('p', class_='blockquote-text')
                    author = author + author_site_text.find_all('p', class_='blockquote-origin')
                    length = len(author) - 1
                text = quotes[random.randint(0, length)].text + '\n' + '\n' + author[random.randint(0, length)].text
                small_photo_check = small_photo_search.find('source')

                if small_photo_check != None:
                    small_photo = small_photo_search.find('source').get('srcset')
                    x = 1
                    small_photo_link = small_photo[0]
                    while 1:
                        small_photo_link = small_photo_link + small_photo[x]
                        x += 1
                        if small_photo[x] == ' ':
                            break
                    link_photo = 'https://ru.citaty.net' + small_photo_link
                    photo = link_photo
                    bot.send_photo(message.chat.id, photo=photo, caption=text)
                else:
                    bot.send_message(message.chat.id, text=text)

        if alt_Name != None:
            bot.send_message(message.chat.id, text=f"{'Возможно, ' + alt_Name.text}")

bot.polling(none_stop = True)
