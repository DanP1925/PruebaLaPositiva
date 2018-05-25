import json
import requests

class MusixMatch:

    api_key = "fbeaa24a48f870317f20e625f3e0db73"

    def getSongWithTitle(self,title):
        parameters = {"q_track": str(title),"apikey": api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        return self.getTrackIdFromResponse(response)

    def getSongWithAuthor(self, artist):
        parameters = {"q_artist": str(artist),"apikey": api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        return self.getTrackIdFromResponse(response)

    def getSongWithLyrics(self, lyrics):
        parameters = {"q_lyrics": str(lyrics),"apikey": api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        return self.getTrackIdFromResponse(response) 

    def getTrackIdFromResponse(self,response):
        parsed = json.loads(response.content.decode('utf-8'))
        track_id = parsed['message']['body']['track_list'][0]['track']['track_id']
        return track_id

    def getLyricsWithSong(self,track_id):
        parameters = {"track_id": str(track_id),"apikey": api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.lyrics.get?",params=parameters2)
        parsed = json.loads(response.content.decode('utf-8'))
        return parsed['message']['body']['lyrics']['lyrics_body']
