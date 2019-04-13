Music Visualizer - J. Haley and A. Liu, December '18

Built in Python, using the PyGame, Librosa, Soundfile, and PIL libraries.

Takes a music file (.mp3, .ogg, .wav, etc) and produces a slideshow of images that plays simultaneously with the song.
The images are based on the file's musical information at that specific point in the song;
when the song changes to a very different part, you can see that the images also change drastically.
To do this, we divide the music file into smaller "snippets", each of which is then scanned to produce a corresponding image.
When you run this program, you may see a number of image and audio files popping up in the project folder - not to worry,
they'll be destroyed once the program ends or is exited.

For this program to work properly, you'll need to take at least one audio file (preferably 45-60 seconds in length)of a supported format,
and add it into the project directory.
Supported audio formats include: mp3, m4a, wav, aif, aiff, ogg.

To run the application: using Terminal/Command Prompt, navigate to the project directory,
then execute the command "python3 music_interface.py".
From there, you'll be prompted to enter a song name; type in the name of any audio file you've added to the project directory,
without the extension (e.g. Bohemian Rhapsody).
