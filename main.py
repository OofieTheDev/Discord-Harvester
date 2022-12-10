import requests
import json
from colorama import Fore
import os
import sys
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "958376895362244618" # place the channel ID here

URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

class DiscordHarvester:
    # these are just the filetypes I wanted to save, you can add more if you wish by seeing the full list of content-types
    IMAGE_TYPES = ("image/jpeg", "image/png")
    VIDEO_TYPES = ("video/mp4")

    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": TOKEN,
        "referer": "https://discord.com/channels/@me",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.119 Safari/537.36",
        "x-discord-locale": "en-US",
    }

    def __init__(self, number, whole=False, download_pics=False, download_videos=False, filter=[]):
        self.rounds = 0
        self.first = True
        self.number = number
        self.whole = whole
        self.download_pics = download_pics
        self.download_videos = download_videos
        self.media_count = 0

        self.MEDIA_DIR = None
        self.msgList = []
        self.filter = filter

    def make_media_dir(self):
        if self.download_pics:
            self.MEDIA_DIR = os.path.join(os.getcwd(), f"{CHANNEL_ID}_MEDIA")

        if self.MEDIA_DIR:
            try:
                os.mkdir(self.MEDIA_DIR)
            except FileExistsError:
                pass
    
    def calc_rounds(self):
        if self.number <= 100:
            self.rounds = 1
        if self.number % 100 == 0:
            self.rounds = self.number/100
        else:
            self.rounds = (self.number // 100) + 1

        print(Fore.BLUE + f"Rounds required: {self.rounds}")

    def retrieve_msgs(self):
        for _ in range(int(self.rounds)):
            if self.first:
                params = {"limit": 100}
                self.first = not self.first
            else:
                params = {"before": next_id, "limit": 100}

            res = requests.get(URL, headers=DiscordHarvester.HEADERS, params=params)

            if res.status_code != 200:
                print(Fore.RED + f"Status Code Incorrect ({res.status_code}), program terminating...")
                sys.exit(1)

            res_text = json.loads(res.text)

            try:
                next_id = res_text[-1]['id']
            except IndexError:
                break

            for msg in res_text:
                if len(self.filter) == 0:
                    self.prepare_msg(msg)
                else:
                    if msg['author']['id'] in self.filter:
                        self.prepare_msg(msg)
                    else:
                        continue

    def prepare_msg(self, msg):
        if self.whole:
            self.msgList.append(msg)

        if not self.whole:
            if msg['content'] != "":
                self.msgList.append({"username": msg['author']['username'], "id": msg['author']['id'],"timestamp": msg['timestamp'], "content": msg["content"]})

            if not self.download_pics and not self.download_videos:
                return
                    
        if self.download_pics or self.download_videos:
            if len(msg['attachments']) != 0:
                for a in msg['attachments']:
                    media_url = a['url']
                    media_extension = a['content_type'].split("/")[1]
                    if a['content_type'] in DiscordHarvester.IMAGE_TYPES and self.download_pics:
                        media_data = requests.get(media_url).content
                        with open(os.path.join(self.MEDIA_DIR, f"pic{self.media_count}.{media_extension}"), "wb") as p:
                            p.write(media_data)
                            self.media_count +=1 
                    if a['content_type'] in DiscordHarvester.VIDEO_TYPES and self.download_videos:
                        media_data = requests.get(media_url).content
                        with open(os.path.join(self.MEDIA_DIR, f"video{self.media_count}.{media_extension}"), "wb") as v:
                            v.write(media_data)
                            self.media_count +=1 
                                
            return

    def format_json(self):
        self.msgList.reverse()

        with open(f"{CHANNEL_ID}_MESSAGES.json", "w") as f:
            f.write(json.dumps(self.msgList))

        print(Fore.GREEN + f"\nComplete!\nData Length: {len(self.msgList)}")

    def print_all(self): # for debugging purposes only
        print(self.rounds)
        print(self.first)
        print(self.number)
        print(self.whole)
        print(self.download_pics)
        print(self.download_videos)
        print(self.media_count)

harvester = DiscordHarvester(300, whole=True, download_pics=True, download_videos=True)
harvester.make_media_dir()
harvester.calc_rounds()
harvester.retrieve_msgs()
harvester.format_json()
