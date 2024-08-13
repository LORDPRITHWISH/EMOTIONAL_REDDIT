import moviepy.editor as mp
import pyttsx3 as tts
import math
import random
import tqdm
import os
import string
from codes.timefind import findtimearr

vid1='assets/mc1.mp4'
vid2='assets/mc2.mp4'
TAGFONT = 'fonts\\RubikGlitch-Regular.ttf'
MAINFONT= 'fonts\\coolfont.ttf'
COL='white'


def gen_sub(txt,dur) :
    
    txtimg = lambda word,time : mp.TextClip(word, fontsize=70, color=COL,font=MAINFONT).set_duration(time)
    wordlist = findtimearr(txt,dur)
    txtlist=[]
    
    # print(*txtlist,sep='\n')
    
    for i in wordlist:
        text = txtimg(*i)
        txtlist.append(text)
    return mp.concatenate_videoclips(txtlist)



def video_make(words) :
    sound=mp.AudioFileClip('tempo/audio.mp3')

    dur=math.ceil(sound.duration)
    vd=dur+1

    clip1= mp.VideoFileClip(vid1)
    v1l=random.randint(0,math.ceil(clip1.duration)-vd)
    clip2= mp.VideoFileClip(vid2)
    v2l=random.randint(0,math.ceil(clip2.duration)-vd)


    clip1= clip1.subclip(v1l,v1l+vd)
    clip2= clip2.subclip(v2l,v2l+vd)


    com=mp.clips_array([[clip1],[clip2]])


    text = mp.TextClip("@darklord", fontsize=30, color=COL,font=TAGFONT).set_position(("right", "bottom")).set_duration(com.duration)
    border_text = mp.TextClip("@darklord", fontsize=32, color='BLACK',font=TAGFONT).set_position(("right", "bottom")).set_duration(com.duration)

    txt_vid=gen_sub(words,dur).set_position(("center"))    
    
    audio=mp.CompositeAudioClip([sound.set_start(1).volumex(2.0),com.audio.volumex(0.05)])
    com=com.set_audio(audio)


    com=com.crop(x_centered=True,width=810).resize(height=720)
    
    com=mp.CompositeVideoClip([com,txt_vid.set_start(1)])
    com=mp.CompositeVideoClip([com,border_text,text])
    
    i=1
    name='video/story{}.mp4'
    while os.path.exists(name.format(i)) :
        i+=1
    com.write_videofile(name.format(i))


def production(txt) :
    video_make(txt)
    os.remove('tempo/audio.mp3')
    os.remove('tempo/sub.mp3')
    os.system('start story.mp4')
