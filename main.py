import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Dispatcher
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from queue import Queue

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Spotify credentials
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'https://yourdomain.com/callback'

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read"))

# Define mood to playlist mapping
MOOD_PLAYLISTS = {
    'happy': 'spotify:playlist:37i9dQZF1DXdPec7aLTmlC',
    'sad': 'spotify:playlist:37i9dQZF1DX3rxVfibe1L0',
    'energetic': 'spotify:playlist:37i9dQZF1DX76Wlfdnj7AP',
    'relaxed': 'spotify:playlist:37i9dQZF1DWU0ScTcjJBdj'
}

# Command handlers
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! I am a Music Recommendation Bot. Tell me your mood, and I will recommend some music!')

def recommend(update: Update, context: CallbackContext) -> None:
    mood = ' '.join(context.args).lower()
    if mood in MOOD_PLAYLISTS:
        playlist_id = MOOD_PLAYLISTS[mood]
        results = sp.playlist_tracks(playlist_id)
        track_names = [track['track']['name'] for track in results['items']]
        update.message.reply_text(f'Here are some {mood} songs:\n' + '\n'.join(track_names[:10]))
    else:
        update.message.reply_text('Sorry, I do not understand that mood. Try "happy", "sad", "energetic", or "relaxed".')

def main() -> None:
    # Create the Bot instance
    bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
    
    # Create a queue for updates
    update_queue = Queue()

    # Set up the Updater with the queue
    updater = Updater(bot=bot, use_context=True, update_queue=update_queue)

    # Get the dispatcher to register handlers
    dispatcher: Dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("recommend", recommend, pass_args=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
