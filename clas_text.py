import asyncio


class Text(str):
    def __init__(self, text):
        self.text = text


    def check_words_in_text(self, word_list):
        if isinstance(word_list, str):
            word_list = [word_list]
        item_word_list = set(word_list)
        return any(i.lower() in self.lower() for i in item_word_list)

    def replace_all(self, word_list):
        new_text = self
        for i in word_list:
            new_text = new_text.replace(i, '')
        return Text(new_text)


# Пример использования метода экземпляра объекта
word_list = ['🛩', '#авиа', 'orange']
text = Text('🛩 #авиа 🪢ПАССАЖИРОПОТОК АВИАКОМПАНИЙ РФ В ИЮЛЕ ВЫРОС НА 4%, ДО 12 МЛН ЧЕЛОВЕК - РОСАВИАЦИЯ 🅾️ The Trading Times')

# result = text.check_words_in_text(word_list)
# print(result)

# Пример использования класса

# word_list = ['apple', 'banana', 'orange']
# text = 'I like to eat apples and bananas.'


print(text.replace_all(word_list))