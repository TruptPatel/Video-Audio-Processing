import os
import moviepy.editor as mp
import speech_recognition as sr
from tkinter.filedialog import *
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import subprocess
import texttranslate
import text_to_audio
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
def process_video_audio(file_path):
    # vid=askopenfilename()
    video=mp.VideoFileClip(file_path)

    aud=video.audio

    aud.write_audiofile(os.path.join(PROCESSED_FOLDER, "demo.wav"))

    print("Task completed")
    inputAudio = os.path.join(PROCESSED_FOLDER, "demo.wav")
    return inputAudio
def process_video_text(file_path):
    audiopath=process_video_audio(file_path)
    textpath=process_audio_text(audiopath)
    return textpath
#speechToText ::
def process_audio_text(file_path):
    # Load audio from file

    r = sr.Recognizer()
    AudioTime = mp.AudioFileClip(file_path).duration
    print(AudioTime)
    offset = 0.0
    iterations = 1
    while offset < int(AudioTime) :
        with sr.AudioFile(file_path) as source:
            audio = r.record(source,offset=offset)  # Read the entire audio file

        # Transcribe audio
        text = r.recognize_google(audio)  # Replace with your model

        timestamp = offset
        
        # Write to text file
        with open(os.path.join(PROCESSED_FOLDER,"sub.txt"), "a") as file:
            file.write(f"{text}\n")
            
        iterations = iterations + 1
        offset = offset + 15
        print("Iterations :: ",iterations)
        
    # subText = aud.write_audiofile(os.path.join(PROCESSED_FOLDER, "sub.txt"))
    return os.path.join(PROCESSED_FOLDER,"sub.txt")
def process_video_subvideo(file_path):

    def read_subtitles_from_file(file_path):
        with open(file_path, 'r') as file:
            subtitle_list = [line.strip() for line in file.readlines()]
        return subtitle_list

    def add_subtitles(video_path, subtitle_file_path, output_path, duration_per_subtitle=3):
        # Read subtitles from the text file
        subtitle_list = read_subtitles_from_file(subtitle_file_path)

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Open the audio file
        audio = AudioSegment.from_file(video_path)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Define font and other text properties
        font = ImageFont.load_default()

        # Initialize frame index
        frame_index = 0

        # Iterate through each subtitle
        for subtitle in subtitle_list:
            # Read the next frame from the original video
            ret, frame = cap.read()
            if not ret:
                break

            # Create a blank image with text
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img)
            text_bbox = draw.textbbox((0, 0), subtitle, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
            draw.text(((width - text_width) // 2, height - text_height - 10), subtitle, font=font, fill='white')

            # Convert PIL image to OpenCV format
            cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Write the frame with subtitles
            out.write(cv2_img)

            # Write the same frame for the specified duration
            for _ in range(int(fps * 15)):
                out.write(cv2_img)
                frame_index += 1

        # Continue writing the remaining frames from the original video
        while frame_index < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_index += 1

        # Release video capture and writer objects
        cap.release()
        out.release()

        # Save the integrated audio
        out_audio_path = output_path.replace('.mp4', '_audio.aac')
        audio.export(out_audio_path, format='mp4') # Changed from 'mp3' to 'mp4'

        # Merge video and audio using FFmpeg
        final_output_path = output_path.replace('.mp4', '_with_audio.mp4')
        ffmpeg_command = f'ffmpeg -i {output_path} -i {out_audio_path} -c:v copy -c:a aac -strict experimental -shortest {final_output_path}'
        subprocess.call(ffmpeg_command, shell=True)
        return final_output_path
    video_path=file_path
    subtitle_file_path=process_video_text(file_path)
    output_path=os.path.join(PROCESSED_FOLDER,"video_with_subtitles.mp4")
    final_output_path=add_subtitles(video_path, subtitle_file_path, output_path)
    return final_output_path
def process_video_transvideo(file_path):
    def translate(video_path, output_path, translated_audio):

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Open the audio file
        audio = AudioSegment.from_file(translated_audio)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # Define font and other text properties
        font = ImageFont.load_default()

        # Initialize frame index
        frame_index = 0

        while frame_index < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            frame_index += 1

        # Release video capture and writer objects
        cap.release()
        out.release()

        # Save the integrated audio
        out_audio_path = output_path.replace('.mp4', '_audio.aac')
        audio.export(out_audio_path, format='mp4')  # Changed from 'mp3' to 'mp4'

        # Merge video and audio using FFmpeg
        final_output_path = output_path.replace('.mp4', '_with_audio.mp4')
        ffmpeg_command = f'ffmpeg -i {output_path} -i {out_audio_path} -c:v copy -c:a aac -strict experimental -shortest {final_output_path}'
        subprocess.call(ffmpeg_command, shell=True)
        return final_output_path
    video_path=file_path
    subtitle_file_path=process_video_text(video_path)
    output_path=os.path.join(PROCESSED_FOLDER,"video_with_subtitles.mp4")
    file_path_trans=os.path.join(PROCESSED_FOLDER,"sub_trans.txt")
    subtitle_file_path_trans=texttranslate.translate_text_file(subtitle_file_path,file_path_trans)
    trans_audio_path=os.path.join(PROCESSED_FOLDER,"trans_audio.mp3")
    trans_audio=text_to_audio.convertToaudio(subtitle_file_path_trans,trans_audio_path)
    final_output_path=translate(video_path, output_path,trans_audio)
    return final_output_path

