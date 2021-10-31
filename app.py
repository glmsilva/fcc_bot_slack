import logging
import os
import re
import feedparser
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Tech News Bot")
logger = logging.getLogger(__name__)

# map command here
@app.message(re.compile("^last video$")) # type: ignore
def show_last_episode(message, say):
  """Send last episode"""
  channel_type = message["channel_type"]
  if channel_type != "im":
    return

  dm_channel = message["channel"]
  user_id = message["user"]
  NewsFeed = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ")
  video = NewsFeed.entries[0]
  logger.info(f"Sent video < {video} > to user {user_id}")

  #message displayed
  say(text=f"here is your video: {video.title} {video.link}", channel=dm_channel)

def main():
  handler = SocketModeHandler(app, SLACK_APP_TOKEN)
  handler.start()

if __name__ == "__main__":
  main()