# J. Haley and A. Liu, 12 Dec 2018
import librosa
import numpy as np
from PIL import Image, ImageColor
import math
import soundfile as sf #pip install soundfile
import random


possible_extensions = ['mp3', 'm4a', 'wav', 'aif', 'aiff', 'ogg']

def name_valid(name):
    """Searches for the path associated with the song name in the current folder;
    returns True if found, False otherwise.
    """
    is_valid = False
    for x in possible_extensions:
        try:
            y, sr = librosa.core.load(name + '.' + x)
        except:
            continue
        else:
            is_valid = True
            break
    return is_valid

def find_path(name):
    """Finds and returns the path associated with the song name in the current directory,
    or None if not found.
    """
    for x in possible_extensions:
        try:
            y, sr = librosa.core.load(name + '.' + x)
        except:
            pass
        else:
            return name + '.' + x
    return None

def generate_song_and_image_snippets(filename, extension='ogg'):
    """This is the main method to be called from music_interface.py.

    Generates audio file snippets from filename using given extension (default is
    .ogg for good compatibility with Pygame).

    @return: numpy array of lists, each containing (segment_len) number of audio events.
    """
    snippets, sr = cut_up(filename, segment_len=20000) # segment length 20000 is approx 1 sec
    name = remove_extension(filename)
    #snippets.sort()
    for s in range(len(snippets)):
        if len(snippets[s]) > 0:
            song_to_image(name + ' image ' + str(s + 1), data=snippets[s])
            if extension == 'wav':
                librosa.output.write_wav(name + ' music ' + str(s + 1) + '.wav', np.array(snippets[s]), sr)
            else:
                sf.write(name + ' music ' + str(s + 1) + '.' + extension, snippets[s], sr, format=extension)
    return snippets

def remove_extension(path):
    """Removes extension between 2 and 5 characters long from path, based on the
    location of the leftmost '.' character.

    If no '.' exists in path, simply return path.
    """
    if '.' not in path: #there's no extension
        return path
    if path[len(path)-3] == '.':  #extension is 2 characters long
        return path[:len(path)-3]
    elif path[len(path)-4] == '.': #3 chars long
        return path[:len(path)-4]
    elif path[len(path)-5] == '.': #4 chars long
        return path[:len(path)-5]
    elif path[len(path)-6] == '.': #5 chars long
        return path[:len(path)-6]
    else: #generally this happens when there's no extension given but the song name has a '.' in it (ie "Mr. XYZ")
        raise ValueError('Invalid extension length')

def cut_up(filename, segment_len):
    """Load song from filename and then cut up the song
    into smaller pieces based on segment_len.

    @return: numpy array of lists, each containing (segment_len) number of audio events.
    @return: sample rate of song file.
    """
    y, sr = librosa.core.load(filename)
    snippets = []
    temp = []
    total = len(y)
    for i in range(total):
        if i % segment_len == 0 and i > 0:
            snippets.append(temp)
            temp = []
        temp.append(y[i])
    if len(temp) > 0:
        snippets.append(temp)
    return snippets, sr

def song_to_image(name, image_type='bmp', data=[], count_on=False):
    """Reads audio data and generates an image with pixel colors based on the data.
    The data is then saved to the current directory (to be later removed by remove_files).

    In generate_song_and_image_snippets above, in which data is already given,
    this method just generates images from the input data.
    """
    if len(data) > 0: #if there's already music data given, name is just used for the output image
        y = data
    else: #name is used for loading music data as well as output image
        y, sr = librosa.core.load(name)
    height = int(math.sqrt(len(y)))
    width = len(y) // height
    img = Image.new('RGB', (width, height))
    minimum = -1.16
    maximum = 1.16
    #minimum = min(y)
    #maximum = max(y)
    available_range = maximum - minimum
    median = (maximum + minimum) / 2

    for r in range(height):
        for c in range(width):
            moment = y[c + (r * width)]
            red = min((int(((moment - minimum) / (maximum - minimum)) * 255)) + 50, 255)
            green = 50 if moment > median else 200
            blue = max((int(((moment - minimum) / (maximum - minimum)) * 255)) - 50, 0)
            img.putpixel((c,r), (red, green, blue)) # it's (c, r) because the format is (x, y)
    img.save(remove_extension(name) + '.' + image_type)

def remove_files(name, music_ex, image_ex):
    """Removes music files and/or image files associated with the given song name
    from the current directory.

    @return: None
    """
    import os
    s = 0
    done = False
    if music_ex or image_ex: #make sure one of them exists, otherwise we have an infinite loop
        while not done:
            if music_ex:
                if os.path.exists(name + ' music ' + str(s + 1) + '.' + music_ex):
                    os.remove(name + ' music ' + str(s + 1) + '.' + music_ex)
                    done = False
                else:
                    done = True
            if image_ex:
                if os.path.exists(name + ' image ' + str(s + 1) + '.' + image_ex):
                    os.remove(name + ' image ' + str(s + 1) + '.' + image_ex)
                    done = False
                else:
                    done = True
            s += 1


if __name__ == '__main__':
    filename = "White Wind.m4a"
    generate_song_and_image_snippets(filename=song_path, extension='ogg', rate_multiply=1.0)
