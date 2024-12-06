from re import split, sub

from prlps_translit.mapping import TranslitSchema, cyr_to_lat


def transliterate(cyrillic_source_text: str) -> str:
    """
    функция для транслитерации русского текста на латиницу
    :param cyrillic_source_text: текст для транслитерации
    :return: транслитерированный текст
    """

    def _split_sentence(source: str):
        return (word for word in split(r'\b', source) if word)

    def _split_word(word: str):
        ending_length = 2
        if len(word) > ending_length:
            return word[:-ending_length], word[-ending_length:]
        return word, ''

    def _letter_reader(stem: str):
        prev, curr = '', ''
        for idx in range(len(stem)):
            next_ = stem[idx + 1] if idx < len(stem) - 1 else ''
            yield prev, curr or stem[idx], next_
            prev, curr = curr or stem[idx], next_

    def _translate_letters(word: str, schema: TranslitSchema):
        return [schema.get_translation(prev, curr, next_) for prev, curr, next_ in _letter_reader(word)]

    def _translate_word(word: str, schema: TranslitSchema):
        stem, ending = _split_word(word)
        translated_ending = schema.get_ending_translation(ending) if ending else None
        if translated_ending:
            translated = _translate_letters(stem, schema) + [translated_ending]
        else:
            translated = _translate_letters(word, schema)
        return ''.join(translated)

    return ''.join(_translate_word(word, cyr_to_lat) for word in _split_sentence(cyrillic_source_text))


def translate_to_url(cyrillic_string: str, divider: str = '-') -> str:
    """
    функция для транслитерации русского текста на латиницу для человекопонятных ссылок
    :param cyrillic_string: текст для транслитерации
    :param divider: разделитель
    :return: транслитерированный текст
    """
    cyrillic_string = transliterate(cyrillic_string).replace(' ', divider).lower()
    return sub(rf'[^0-9a-z{divider}]', '', cyrillic_string)


