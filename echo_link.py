import json
import requests
import time

TOKEN = "TOKEN"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
ADMIN1 = ""
ADMIN2 = ""

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if (offset):
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# def get_last_chat_id_and_text(updates):
#     print "here"
#     num_updates = len(updates["result"])
#     last_update = num_updates - 1
#     text = updates["result"][last_update]["message"]["text"]
#     chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#     USER_ID = updates["result"][last_update]["message"]["from"]["username"]
#     print USER_ID
#     return (text, chat_id)

def send_message(text, chat_id, parse_mode):
    url = URL + "sendMessage?chat_id=" + str(chat_id) + "&text=" + text + "&parse_mode=" + parse_mode
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"]
            username = update["message"]["from"]["username"]

            if username == ADMIN1 or username == ADMIN2 :
                link_index_start =  text.find("http")
                if link_index_start != -1:
                    link_index_end = text.find("\n", link_index_start)
                    inline_URL_index_start = link_index_end + 1
                    inline_URL_index_end = text.find("\n", inline_URL_index_start+1)
                    link = text[link_index_start:link_index_end]
                    inline_URL = text[inline_URL_index_start:len(text)]
                    parse_mode = "markdown"
                    text = text[0:link_index_start] + "[" + inline_URL + "]" + "(" + link + ")"
                    send_message(text, chat_id, parse_mode)


        except Exception as e:
            print(e)

def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
