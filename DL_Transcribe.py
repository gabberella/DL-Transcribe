#A quick and dirty command line tool to Download the video and create a transcription with a youtube link 


from pytube import YouTube
import wave, math, contextlib
import speech_recognition as sr

from moviepy.editor import AudioFileClip

link = input("Enter the YouTube link:")
yt= YouTube(link)

#Title of video
print("Title:" ,yt.title)
#Number of views of video
print("Number of views:" ,yt.views)
#Length of the video
print("Length of video:",yt.length,"seconds")

ys = yt.streams.get_highest_resolution()


#Starting download
print("Downloading...")
ys.download()
print("Download completed!!")

#Filename to transcribe 

transcribed_audio_file_name = "tr_speech.wav"

vid_file= str(yt.title) + ".mp4"

audioclip= AudioFileClip(vid_file)
audioclip.write_audiofile(transcribed_audio_file_name)

#getting duration for APIs limitations
with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    
total_duration= math.ceil(duration/60)

#speech recognition to .doc file
r= sr.Recognizer()
transcript = str(yt.title) + ".doc"

for i in range(0, total_duration):
    with sr.AudioFile(transcribed_audio_file_name) as source:
        audio = r.record(source, offset=i*60, duration=60)
    f = open(transcript, "a")
    f.write(r.recognize_google(audio))
    f.write(" ")
f.close()
