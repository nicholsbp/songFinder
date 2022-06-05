# songFinder
### Find songs used in youtube videos for an entire channel or playlist

Youtube sucks at identifying songs used in videos, especially if they are played briefly. This python program accepts a youtube channel or user and will scan every video they have uploaded for audio tracks and output Title, Artist, and a youtube link to the song (if available) to a file. 

Shazam is used to identify tracks, by default we are very gentle with their API to avoid getting banned. This means it will take a very long time to process a large youtube channel (days). Decrease SHAZAM_QUERY_WAIT if needed.
