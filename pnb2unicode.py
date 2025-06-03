# pnb2unicode.py
#

import re

# my mappings for Punjabi to Unicode characters.
punjabi_to_unicode_mappings = [
    {
        # Punjabi to Unicode mapping for Gurmukhi script
        # This mapping is based on the PSEB 10th and 12th results the font name is PNB
        '§': 'ਓ', '¤': 'ਅ', 'Ó': 'ਸ', 'Õ': 'ਹ', 
        # k
        '¨': 'ਕ', 'ª': 'ਖ', '\u00ab' : 'ਖ਼', '¬': 'ਗ', '®': 'ਘ', '°': 'ਙ',
        # ch
        '°': 'ਚ', '±': 'ਛ', '²': 'ਜ', '\u00b3' : 'ਜ਼', '¯': 'ਝ', 
        # t
        '¶': 'ਟ', '·': 'ਠ', '¸': 'ਡ', '¹': 'ਢ', '»': 'ਣ', 
        # T
        '¼': 'ਤ', 'Á': 'ਥ', 'Â': 'ਦ', 'Ä': 'ਧ', 'Å': 'ਨ',
        # p
        'Æ': 'ਪ', 'Ç': 'ਫ', 'É': 'ਬ', 'Ê': 'ਭ', 'Ì': 'ਮ',
        # y
        'Í': 'ਯ', 
        'Î': 'ਯ', 'Ï': 'ਰ', 'Ð': 'ਲ', 'Ò': 'ਵ', 'µ': 'ਵ',
        # sh
        'Ô': 'ਸ਼', 
        # others
        '\u00d1' : 'ਲ਼',
        '\u00b9' : 'ਡ੍ਰ',
        '\u00dc' : 'ੀਂ',
        '\u00f0' : '੍ਹ',
        '\u00f2' : '੍ਵ',
        '\u00c8' : 'ਫ਼',
        '\u00f3' : 'ੱ',
        '\u00f4' : 'ੱ',
        '\u00f5' : 'ੱ',
        'ó': 'ੱ',
        # vowels
        'â': 'ੰ', 'Þ': 'ੂ', 'Û': 'ੀ', 'ï': 'ੌ', 
        'ë': 'ੋ', 'Ú': 'ਿ', 'Ý': 'ੁ', 'ã': 'ੇ', 'ñ': '੍ਰ',
        'è': 'ੈ', 'Ù': 'ਾਂ', 'Ø': 'ਾ', 'Ö': '़',
        '×': 'ਂ'
    },

    # special groups of letters
    {
        'ÓÖ': 'ਸ਼', 'ªÖ': 'ਖ਼', '¬Ö': 'ਗ਼', '³Ö': 'ਜ਼', 'ÆÖ': 'ਫ਼', 'ÐÖ': 'ਲ਼',
        '¦Ý': 'ਉ', '¦Þ': 'ਊ', 'Óè': 'ਐ', '¥ã': 'ਏ', 
        '©': 'ਕ੍ਰ',
        'f(.)': '\\1f',
        'Ú¥': 'ਇ', '¥Û': 'ਈ', 'Ú(.)': '\\1Ú', '¤Ø': 'ਆ', 
        '¤è': 'ਐ', 
        '¤ï': 'ਔ', 
        '²Ö' : 'ਜ਼',
        'ÞÝ' : 'Þ',
        'ÝÞ' : 'Ý',
        # miscellaneous corrections
        'âÞ': 'Þâ', 'óÝ': 'Ýó'
    }
]

multiples_for_cleanup = [
    '\u00dc',
    '\u00f0',
    '\u00f2',
    '\u00c8',
    '\u00f3',
    '\u00f4',
    '\u00f5',
    'ó',
    # vowels
    'â', 'Þ', 'Û', 'ï', 'ë', 'Ú', # 'Ý', 
    'ã', 'ñ',
    'è', 'Ù', 'Ø', 'Ö',
    '×']


def to_unicode(text):
    """
    Converts text in PNB font to equivalent unicode standard

    Args:
        text (str): The input text string (in PNB font) to be transliterated.

    Returns:
        str: The transliterated text string.
    """
    letter_mappings = punjabi_to_unicode_mappings[0]
    letters_group_mappings = punjabi_to_unicode_mappings[1]

    # transliterate as:

    # clean up multiples
    for letter in multiples_for_cleanup:
        text = re.sub(letter + '+', letter, text)

    # special group of characters
    for key in letters_group_mappings:
        text = re.sub(key, letters_group_mappings[key], text)


    # individual letters
    transliterated_text = ""
    for char in text:
        if char in letter_mappings:
            transliterated_text += letter_mappings[char]
        else:
            transliterated_text += char
    return transliterated_text


if __name__ == '__main__':
    print("pnb2unicode.py -- code to convert PSEB site font to unicode standard")

