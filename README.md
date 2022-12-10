# :speech_balloon: Discord Harvester

## :star: Introduction
This is a simple Python script that harvests as many messages as you want from a DM channel/server channel (potentially everything, though that could take a while). It stores them in JSON format, which is human-readable and easily filtered/manipulated. I made this as I wanted to save the chat history of certain channels. Thought that someone out there might find it useful, which is why I'm publishing it.

## :keyboard: Quick Start
To get started, simply run 
```
pip install -r requirements.txt
```

After that, you just need to add the discord token of the account you are using, either inside a .env file in the same directory or inside the `TOKEN` variable in main.py. Then, add the channel ID you wish to scrape inside the variable `CHANNEL_ID`, and you're good to go.

To get the ID of most channels, just enable Developer Mode in your Account Settings, then you can right click any channel and select "Copy ID".

However, if you wish to scrape a DM channel, you cannot get the ID like that. Instead, right click any message in the channel and select "Copy Message Link". Inside this link are 2 long strings of numbers separated by a /. The first string of numbers is the channel ID.

## :computer: Features
The script allows you to choose whether or not to save the media contained in the channel, such as photos and videos. It automatically creates the directories and files to store the media as well, so no work on your part is needed for that. If you wish to save other types of media, such as PDFs, executables, GIFs etc, I have written the code such that anyone with base Python knowledge should be able to easily modify the script to save such files.

This script harvests close to 200 messages/s. So just keep in mind that if you're retrieving tens of thousands of messages, you'll need to wait a couple minutes.

## :thinking: Code Walkthrough
### Understanding the __init__
The __init__ method in the script is defined as follows.
```py
def __init__(self, number, whole=False, download_pics=False, download_videos=False, filter=[]):
```
`number` is the number of messages you wish to retrieve (starting from most recent).

When you retrieve messages from Discord, it is returned to you in JSON format. However, there are tens of key-value pairs, which might be hard for a human to read. The `whole` parameter here, if set to True, saves every key-value pair of each message into the JSON file. If set to False however (recommended), only essential key-value pairs such as author username, author ID, timestamp, and message content are saved, improving readability.

I believe that `download_pics` and `download_videos` are self-explanatory.

As for filter, this is a list that should contain the user IDs of the message authors whose messages/media you wish to save. For example, if you and Person B have a DM channel that you wish to scrape, but you only want to scrape Person B's messages, then you should put Person B's user ID in the `filter` list, as a STRING. **Do not put it as an integer.**

By doing this, the script will ignore your messages and only save the messages and files sent by Person B. You may put as many user IDs as you want in the `filter` list.

### Understanding retrieve_messages
This is no doubt the longest method besides `prepare_msgs`. However, I am too lazy to explain everything and will just explain one important part.

```py
if self.first:
    params = {"limit": 100}
    self.first = not self.first
else:
    params = {"before": next_id, "limit": 100}
```
This sets the parameters of the GET request that is sent to Discord to retrieve the messages. `Limit` is the amount of messages to retrieve. You might have noticed that it set at 100. **This does not mean you can change it to 30000 to retrieve 30,000 messages at once.** Discord limits the amount of messages that you are able to retrieve with a single request to 100. In order to retrieve more, the `before` parameter needs to be set as the message ID of the message whose previous comrades you want to view. This is automatically set and updated constantly for you in the script (obviously) depending on how many messages you decide to retrieve, so just don't touch this part.

Note that because of this hardcoding, the minimum amount of messages it will retrieve is 100. Even if you put the `number` parameter in __init__ as 50, it will still retrieve 100. I do not see this as a flaw, as there is no point in using my script unless you wish to save a large amount of messages, which is obviously very inconvenient for a human to manually do.

### Understanding format_json
In the method `format_json`, this line is present:
```py
self.msgList.reverse()
```
This reverses the list of messages harvested before storing them in JSON format. This is because when the messages are retrieved, the latest message will be at the top of the JSON file, which is not intuitive and does not make sense to a human. Hence, this line reverses the order, such that the first message is at the top, and the last message is at the bottom.

## :slightly_smiling_face: Fin
I hope this script helps someone out there! Peace out :v:





