from gtts import gTTS
def convertToaudio(file_path,destination_path):
#Read the text from the file
    with open(file_path, 'r') as file:
        text = file.read()

    #Create a text-to-speech object
    tts = gTTS(text=text, lang='ru')  # Specify the language if needed

    #Save the audio file
    tts.save(destination_path)
    return destination_path

