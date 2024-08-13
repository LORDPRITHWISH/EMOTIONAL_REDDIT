from codes.movie_processor import production
from codes.recording_booth import record

source='tempo/story.txt'

def mkmovie() :
    with open(source,'r') as re :
        if re.readline() == '' :
            return False
    def restwrite(story) :
        with open(source,'w') as sour :
            sour.write(story)


    with open(source,'r') as sour :
        text=sour.readline()
        restwrite(sour.read())


        
    ind=text.index('#####')

    sub=text[0:ind]
    story=text[ind+5:]


    record(sub,story)

    production(story)
    
    return True
