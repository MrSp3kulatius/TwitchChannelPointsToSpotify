import spotipy
from uuid import UUID
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope
from twitchAPI.oauth import UserAuthenticator
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import pubsub

reward_name = "Add Song to Spotify Playlist"
streamer_name = "MrSp3kualtius"

spotify_client_id = "f692a6e59440469a8e86ee9aa54c1001"
spotify_client_secret = "93b64abbe8be430f919176d422ab3c62"
spotify_redirect_uri = "http://localhost:1337"
spotify_playlist = "2ilZWj2VEKmLaYNwRjMFhm?si=aac4f0c697334a2c&nd=1"

twitch_client_id = "2fleeknulzmytf9q3llzx5qekrmeuc"
twitch_client_secret = "kxt4j7p6n1hevydpf387qn5omhaykd"


def callback_spotify(uuid: UUID, data: dict) -> None:
    for reward in Twitch.get_custom_reward(twitch, user_id)['data']:
        if reward_name in reward['title']:
            print("Playlist ID: "+reward['id'])
            playlist_reward_id = reward['id']

    if playlist_reward_id in data['data']['redemption']['reward']['id']:
        trackid = [data['data']['redemption']['user_input'].split("/track/")[1].split("?si")[0]]
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_client_secret,
                                                    redirect_uri=spotify_redirect_uri,
                                                    scope="playlist-modify-public"))

        sp.playlist_add_items(spotify_playlist, trackid)

twitch = Twitch(twitch_client_id, twitch_client_secret)

target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
auth = UserAuthenticator(twitch, target_scope, force_verify=False)
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, target_scope, refresh_token)

user_id = twitch.get_users(logins=streamer_name)['data'][0]['id']

pubsub = PubSub(twitch)
pubsub.start()
uuid = pubsub.listen_channel_points(user_id, callback_spotify)
input('press ENTER to close...')
pubsub.unlisten(uuid)
pubsub.stop()
