import json
import requests

class MusixMatch:

    api_key = "fbeaa24a48f870317f20e625f3e0db73"

    def getSongWithTitle(self,title):
        parameters = {"q_track": str(title),"apikey": self.api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        title = self.getTitle(response)
        author = self.getAuthor(response)
        track_id = self.getTrackIdFromResponse(response)
        return title, author, track_id

    def getSongWithAuthor(self, artist):
        parameters = {"q_artist": str(artist),"apikey": self.api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        title = self.getTitle(response)
        author = self.getAuthor(response)
        track_id = self.getTrackIdFromResponse(response)
        return title, author, track_id

    def getSongWithLyrics(self, lyrics):
        parameters = {"q_lyrics": str(lyrics),"apikey": self.api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.search?page_size=1&page=1&s_track_rating=desc",params=parameters)
        title = self.getTitle(response)
        author = self.getAuthor(response)
        track_id = self.getTrackIdFromResponse(response)
        return title, author, track_id

    def getTitle(self,response):
        parsed = json.loads(response.content.decode('utf-8'))
        if (len(parsed['message']['body']['track_list']) != 0):
            title = parsed['message']['body']['track_list'][0]['track']['track_name']
            return title
        else:
            return None

    def getAuthor(self,response):
        parsed = json.loads(response.content.decode('utf-8'))
        if (len(parsed['message']['body']['track_list']) != 0):
            author = parsed['message']['body']['track_list'][0]['track']['artist_name']
            return author
        else:
            return None


    def getTrackIdFromResponse(self,response):
        parsed = json.loads(response.content.decode('utf-8'))
        if (len(parsed['message']['body']['track_list']) != 0):
            track_id = parsed['message']['body']['track_list'][0]['track']['track_id']
            return track_id
        else:
            return None

    def getLyricsWithSong(self,track_id):
        parameters = {"track_id": str(track_id),"apikey": self.api_key}
        response = requests.get("http://api.musixmatch.com/ws/1.1/track.lyrics.get?",params=parameters)
        parsed = json.loads(response.content.decode('utf-8'))
        print(parsed)
        if (len(parsed['message']['body']) != 0):
            return parsed['message']['body']['lyrics']['lyrics_body']
        else:
            return None 
