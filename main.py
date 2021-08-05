import cv2
import sys
import fpstimer
import moviepy.editor as mp
from PIL import Image
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

# Constants
ascii_letters = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
frame_width = 233

# Function that plays the bad apple song using the mixer from pygame
def playAudio(path):
    mixer.pre_init(buffer = 2048)
    mixer.init()
    mixer.music.load(path)
    mixer.music.set_volume(0.1)
    mixer.music.play()

# Function that plays the bad apple video in terminal
def playVideo(video, total_frames):
    os.system("color F0")
    os.system("mode con: cols=233 lines=68")

    timer = fpstimer.FPSTimer(60)
    frame_num = 0

    while frame_num < total_frames:
        sys.stdout.write(video[frame_num])
        sys.stdout.flush()
        frame_num += 1
        timer.sleep()

# Function that will extract the ascii frames from the video and append it to memory
def extractFrames(path, total_frames):
    cap = cv2.VideoCapture(path)
    memory = [] # Array that contains the ASCII video to be played

    count = 1 # Frame counter
    success, frame = cap.read() 

    while success and count <= total_frames:
        memory.append(processFrames(frame)) 

        success, frame = cap.read() 
        
        progressBar(count, total_frames) 

        count += 1
    
    cap.release()

    return memory

# Progress bar code taken from StackOverflow, user: Aravind Voggu.
# Link: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progressBar(current, total, barLength = 25):
    progress = float(current) * 100 / total
    arrow = '#' * int(progress / 100 * barLength - 1)
    spaces = ' ' * (barLength - len(arrow))
    sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current, total))

# Function that will generate ASCII frames of the video
def processFrames(frame):
    image = Image.fromarray(frame)
    ascii_chars = transformAscii(resizeImage(image))
    length = len(ascii_chars)
    ascii_image = "\n".join([ascii_chars[index:(index + frame_width)] for index in range(0, length, frame_width)])

    return ascii_image

# Resizing the frames of each image
def resizeImage(frame):
    width, height = frame.size

    aspect_ratio = (height / float(width * 2.5))
    new_height = int(aspect_ratio * frame_width)
    resized_gray_image = frame.resize((frame_width, new_height)).convert('L')

    return resized_gray_image

# Transform pixels into ascii characters
def transformAscii(frame):
    pixels = frame.getdata()
    chars = "".join([ascii_letters[pixel // 25] for pixel in pixels])

    return chars

# Function that inititializes the variables and frame count as well as grabs frames from the video
def initialize(path):
    if os.path.exists(path):
        path = path.strip()

        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        cap.release()
    
        video = mp.VideoFileClip(path)
        audio_path = "audio.mp3"
        video.audio.write_audiofile(audio_path)

        sys.stdout.write("ASCII generating...\n")
        video = extractFrames(path, total_frames)

        return total_frames, video
        
    else:
        sys.stdout.write('File not found\n')

# Main function
def main():
    total_frames, video = initialize("BadApple.mp4")
    playAudio("audio.mp3")
    playVideo(video, total_frames)

# Driver code
if __name__ == '__main__':
    main()  