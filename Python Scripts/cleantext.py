import re
def Cleaning_twitter_data(text_string):
    try:
        # remove patterns matching url format
        url = r'((http|ftp|https):\/\/)?[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&amp;:/\+#]*[\w\-\@?^=%&amp;/\+#])?'
        text_string = re.sub(url_pattern, ' ', text_string)

        # remove new line and digits with regular expression
        text_string = text_string.replace(r"\n", " ")

        # remove emojis from the tweets
        emojis = r'\\u[\da-z]+'
        text_string = re.sub(emojis, '', text_string)

        # reomve the RT from the tweets
        text_string = text_string.replace(r"RT", " ")

        # remove white space
        front_trailing_spaces = r"^\s|\s$"
        text_string = re.sub(front_trailing_spaces, "", text_string)

        # remove special characters
        special_char = r'[^A-Za-z0-9 ]+'
        text_string = re.sub(special_char, '', text_string)

        # standardize white space
        white_space = r'\s+'
        text_string = re.sub(white_space, ' ', text)
    except:
        pass
    return text_string