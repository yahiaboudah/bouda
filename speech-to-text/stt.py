
def speech_to_text(pp, lan):

    from speech_recognition import Recognizer, AudioFile
    from pydub import AudioSegment
    import os
    newpp = pp
    nflac = False

    # if not flac, convert:
    dirname = os.path.dirname(pp)
    filename, fileext = os.path.split(pp)[1].split('.')
    
    if(fileext != 'flac'):
        nflac = True
        newpp = (os.path.join(dirname, filename + '.flac'))
        sound = AudioSegment.from_file(pp)
        sound.export(newpp, format="flac")
    

    r = Recognizer()
    with AudioFile(newpp) as source:              
        audio = r.record(source)

    try:
        txt = r.recognize_google(audio,language = lan)
    except:
        return 'Python Error'
    #clean up the flac file:
    if(nflac): os.remove(newpp)

    return txt