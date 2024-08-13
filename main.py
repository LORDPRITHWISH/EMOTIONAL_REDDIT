from codes.Analyser import main
# from codes.movie_maker import mkmovie
from codes.story_extract import getstory



LINK='https://www.reddit.com/r/robotics/'
# LINK='https://www.reddit.com/r/RubyRiottHumiliation/'

# SEARCH="https://www.reddit.com/search/.json?q=robotic+technologies&type=sr"

# getstory(LINK)

# while mkmovie() :
    # print('Movie made')
    
# print('No more stories to make movies from')


main(LINK)