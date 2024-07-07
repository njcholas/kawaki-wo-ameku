import cv2
from PIL import Image
import os
import time
from playsound import playsound
import threading

music_path = ''
music_playing = True

def play_music(music_path):
    while True:
            playsound(music_path)

threading.Thread(target=play_music, args=(music_path,), daemon=True).start()

ASCII_CHARS = "!></();:=?@%#*+=-:. "

def map_pixels_to_ascii(gray_scale_value):
    return ASCII_CHARS[gray_scale_value * len(ASCII_CHARS) // 256]

def convert_frame_to_ascii(frame, new_width=100):
    image = Image.fromarray(frame)
    width, height = image.size
    aspect_ratio = height/float(width)
    new_height = int(aspect_ratio * new_width)
    resized_gray_image = image.resize((new_width, new_height)).convert('L')
    pixels = list(resized_gray_image.getdata())
    ascii_str = ''.join([map_pixels_to_ascii(pixel) for pixel in pixels])
    ascii_str_len = len(ascii_str)
    ascii_img=""
    for i in range(0, ascii_str_len, new_width):
        ascii_img += ascii_str[i:i+new_width] + "\n"
    return ascii_img

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def video_to_ascii(video_path, frame_rate=30, new_width=100):
    music_thread = threading.Thread(target=play_music, args=(music_path,), daemon=True)
    music_thread.start()
    cap = cv2.VideoCapture(video_path)
    delay = 1 / frame_rate
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        aspect_ratio = frame.shape[0] / frame.shape[1]
        new_height = int(new_width * aspect_ratio)
        
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        ascii_frame = convert_frame_to_ascii(gray_frame)

        clear_console() 
        print(ascii_frame)
        time.sleep(delay)  
        
    cap.release()

video_path = ''
video_to_ascii(video_path)