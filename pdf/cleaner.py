import re

def cleaning(text):
    text = text.lower()

    # dígitos
    text = re.sub(r'\d+', '', text)

    # caracteres especiais
    text = re.sub(r'[^a-zA-Z \n]', '', text)

    # links
    text = re.sub(r'https?://\S+', "", text)

    # espacos
    text = re.sub(r' +', ' ', text)

    # quebras de linha
    text = re.sub(r'\n{3,}', '\n\n', text)

    # bordas
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text
