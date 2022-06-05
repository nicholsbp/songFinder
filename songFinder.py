import asyncio, time, json
from shazamio import Shazam, Serialize
from pydub import AudioSegment
from pydub.utils import make_chunks
from pytube import YouTube, Channel

SONG_LIST = []
SHAZAM_QUERY_INTERVAL = 30 # Time between queries in seconds

def slice_audio(file_name): # Shazam seems to work best on >30 second clips
    myaudio = AudioSegment.from_file(file_name)
    chunk_length_ms = 40000 # MS
    chunks = make_chunks(myaudio,chunk_length_ms)
    for i, chunk in enumerate(chunks):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(match_audio(chunk))
        time.sleep(SHAZAM_QUERY_INTERVAL) # pls dont ban me uwu

async def match_audio(filename):
    shazam = Shazam()
    out = await shazam.recognize_song(filename)
    if 'track' in out: # Song recognized
        result = Serialize.full_track(data=out)
        youtube_data = await shazam.get_youtube_data(link=result.track.youtube_link)
        serialized_youtube = Serialize.youtube(data=youtube_data)
        print(serialized_youtube.uri)
        song_metadata = {'TITLE': out.get('track', {}).get('title'), 'ARTIST': out.get('track', {}).get('subtitle'),'YOUTUBE_LINK': serialized_youtube.uri}
        if song_metadata not in SONG_LIST:
            SONG_LIST.append(song_metadata)
        print(song_metadata)


if __name__ == "__main__":
    c = Channel('URL FOR YOUTUBE CHANNEL OR PLAYLIST')
    i = 0
    for video in c.videos:
        print(video.title)
        print(i)
        t = video.streams.filter(only_audio=True)
        t[0].download(filename='audio_track')
        slice_audio('audio_track')

        jsonString = json.dumps(SONG_LIST)
        jsonFile = open("songs.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        i+=1
