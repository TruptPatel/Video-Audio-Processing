from googletrans import Translator

def translate_text_file(input_file,output_file,target_language='ru'):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as file:
        source_text = file.read()

    translated_text = translator.translate(source_text, dest=target_language).text

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(translated_text)
    print(f"Translation complete. Check {output_file} for the translated text.")
    return output_file


    
