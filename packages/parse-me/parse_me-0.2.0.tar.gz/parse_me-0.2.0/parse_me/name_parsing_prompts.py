"""
This file contains prompts for name parsing in different languages and cultures.
"""

BASIC_NAME_PARTS = (['primary-name', 'given-name','alternative-name', 'middle-name','maiden-surname', 'surname',
                     'patronymic', 'matronymic', 'honorific', 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation',
                     'salutation'],
                    '*given-name*: e.g. "Moses, John, Muhammad". If an initial is used, e.g. the M. in "M. Smith" then you can just use the initial.' \
                    '*alternative-name*: For example, "ציפי" in "ציפי (ציפורה) שביט" or "the rock" in "Chris the rock Johnson."' \
                    '*middle-name e.g. "Hillel" in the name "Haim Hillel Ben-Sasson" Here as well, there may be only an initial. ' \
                    '*maiden-surname* e.g. Goldstein ' \
                    'in the name "Sara Karp (nee Goldstein)" or "Sara Karp (geb. Goldstein)" or "גולדשטיין" in "לילך גולדשטיין-בר". ' \
                    '*surname* e.g. Shalit in the name "Gilad Shalit". *patronymic* e.g. Ben-Moshe, Ibn-Musa, Vladimirovich. ' \
                    'In case of avonymics a patronym can also include names of forefathers: e.g. "ibn Ḥasan ibn Ifrāʾīm ibn Yaʿqūb ibn Ismāʿīl ibn Jumayʿ in the case of ' \
                    'Ibn Jamīʿ, Al-Shaykh al-Muwaffaq Shams al-Riyāsah Abū l-ʿAshāʾir Hibat Allāh ibn Zayn ibn Ḥasan ibn Ifrāʾīm ibn Yaʿqūb ibn Ismāʿīl ibn Jumayʿ al-Isrāʾīlī.' \
                    ' *matronymic* e.g. Bat-Miriam, ابن ناعمة ' \
                    '*honorific* e.g. the honorable, al-Muwaffaq, his highness, מורנו הרב' \
                    ' *acronym* e.g. "רמב״ם". *teknonym*e.g. "Abu-Ibrahim". *professional-name* e.g. Al-Tabib. ' \
                    'Use only when the name is used as an actual designation of the profession of the individual, ' \
                    'and not when it is a surname like "Thatcher" in "Margeret Thatcher" (even if it might refer to ' \
                    'the profession in previous generations). *nisba* representing the regional origin of a person ' \
                    'or their family e.g. al-Isrāʾīlī in the example above. *qualifier* e.g. "jr." or "the third". ' \
                    '*appellation* E.g. "Lord", "Ha-Cohen". Use only when the name is used as a designation of an ' \
                    'actual status, not when merely a surname like in "Jaacov Cohen". *sallutation* e.g. Dr., Prof., Bei.')

ARABIC_NAME_PARTS = (['primary-name', 'given-name', 'middle-name', 'surname', 'patronymic', 'matronymic', 'honorific'
                         , 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation',
                      'salutation']
                     , """**ARABIC_NAME_PARTS:**
*primary-name*: For example, \"ابن جمايع\", \"الرازي\". This is a common way of referring to a person and may not necessarily conform to other name fields.
*given-name*: For example, \"محمد\", \"علي\", \"فاطمة\".
*alterantive-name*: For example, \"تسيبي\" in \"تسيبي (تسيبورا) شافيت\" this field can also be used as a nickname.
*middle-name*: For example, \"هلال\" in the name \"خالد هلال بن سعيد\".
*surname*: For example, \"شلبي\" in \"جميل شلبي\".
*patronymic*: For example, \"ابن موسى\", \"بن يوسف\". May also include avonymic names of forefathers, such as \"ابن حسن بن إبراهيم بن إسماعيل\".
*matronymic*: For example, \"ابن ناعمة\".
*honorific*: For example, \"الموفق\", \"فضيلة الشيخ\".
*acronym*: For example, \"رمسيس\".
*teknonym*: For example, \"أبو إبراهيم\".
*professional-name*: For example, \"الطبيب\" when referring to a specific profession.
*nisba*: Referring to regional origin, such as \"المصري\" or \"الإسرائيلي\".
*qualifier*: For example, \"الثاني\".
*appellation*: For example, \"الأمير\", \"الحاخام\".
*salutation*: For example, \"دكتور\", \"أستاذ\".""")

ARABIC_NAME_PARTS_LATIN = (
['primary-name', 'given-name', 'middle-name', 'surname', 'patronymic', 'matronymic', 'honorific'
    , 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation', 'salutation'],
"""**ARABIC_NAME_PARTS (Latin script):**
*primary-name*: For example, \"Ibn Jamīʿ\", \"Al-Razi\". A name commonly used to refer to a person, independent of other name components.
*given-name*: For example, \"Muhammad\", \"Ali\", \"Fatimah\".
*middle-name*: For example, \"Hilal\" in the name \"Khalid Hilal bin Said\".
*surname*: For example, \"Shalabi\" in \"Jamil Shalabi\".
*patronymic*: For example, \"ibn Musa\", \"bin Yusuf\". May also include avonymic names of forefathers, such as \"ibn Hasan ibn Ibrahim ibn Isma'il\".
*matronymic*: For example, \"ibn Na'ima\".
*honorific*: For example, \"al-Muwaffaq\", \"Fadhilat al-Shaykh\".
*acronym*: For example, \"Ramsis\".
*teknonym*: For example, \"Abu Ibrahim\".
*professional-name*: For example, \"al-Tabib\" when referring to a specific profession.
*nisba*: Referring to regional origin, such as \"al-Misri\" or \"al-Isra'ili\".
*qualifier*: For example, \"al-Thani\" (the second).
*appellation*: For example, \"al-Amir\", \"al-Hakham\".
*salutation*: For example, \"Dr.\", \"Ustadh\".""")

HEBREW_NAME_PARTS_LATIN = (
['primary-name', 'given-name', 'middle-name', 'surname', 'patronymic', 'matronymic', 'honorific'
    , 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation', 'salutation'],
"""**HEBREW_NAME_PARTS (Latin script):**
*primary-name*: For example, \"Ibn-Gvirol\", \"Maimonides\". A name commonly used to refer to a person, independent of other name components.
*given-name*: For example, \"Moses\", \"Shlomo\", \"Lea\" .
*alternative-name*: For example, \"Tzipi\" in \"Tzipi (Tzipora) Shavit\".
*middle-name*: For example, \"Hillel\" in the name \"Yitzhak Hillel Ben-Sasson\".
*surname*: For example, \"Shalit\" in \"Gilad Shalit\".
*patronymic*: For example, \"Ben-Moshe\", \"Ben-Yitzhak\". Can also include forefathers' names, such as \"Ben-Eliyahu Ben-Yosef\".
*matronymic*: For example, \"Bat-Miriam\".
*honorific*: For example, \"Moreinu\", \"Harav\".
*acronym*: For example, \"Rambam\" (רמב\"ם).
*teknonym*: For example, \"Abba-Yosef\".
*professional-name*: For example, \"Ha-Dayan\" when used to indicate a professional role.
*qualifier*: For example, \"ha-sheni\" (the second).
*appellation*: For example, \"HaCohen\", \"HaLevi\".
*salutation*: For example, \"Dr.\", \"Rav\".""")

MODERN_HEBREW_NAME_PARTS_LATIN = (
['primary-name', 'given-name', 'middle-name', 'surname', 'patronymic', 'matronymic', 'honorific'
    , 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation', 'salutation'],
"""**HEBREW_NAME_PARTS (Latin script):**
*primary-name*: For example, \"Ibn-Gvirol\", \"Maimonides\". A name commonly used to refer to a person, independent of other name components.
*given-name*: For example, \"Moses\", \"Shlomo\", \"Lea\" .
*alternative-name*: For example, \"Tzipi\" in \"Tzipi (Tzipora) Shavit\".
*middle-name*: For example, \"Hillel\" in the name \"Yitzhak Hillel Ben-Sasson\".
*surname*: For example, \"Shalit\" in \"Gilad Shalit\".
*patronymic*: For example, \"Ben-Moshe\", \"Ben-Yitzhak\". Can also include forefathers' names, such as \"Ben-Eliyahu Ben-Yosef\".
*matronymic*: For example, \"Bat-Miriam\".
*honorific*: For example, \"Moreinu\", \"Harav\".
*acronym*: For example, \"Rambam\" (רמב\"ם).
*teknonym*: For example, \"Abba-Yosef\".
*professional-name*: For example, \"Ha-Dayan\" when used to indicate a professional role.
*nisba*: Referring to regional or familial origin, such as \"Of Prague\" or \"HaTishbi\".
*qualifier*: For example, \"ha-sheni\" (the second).
*appellation*: For example, \"HaCohen\", \"HaRav\".
*salutation*: For example, \"Dr.\", \"Rav\".""")

HEBREW_NAME_PARTS_HEBREW = (
['primary-name', 'given-name', 'alternative-name',  'middle-name', 'surname', 'patronymic', 'matronymic', 'honorific'
    , 'acronym', 'teknonym', 'professional-name', 'nisba', 'qualifier', 'appellation', 'salutation'],
"""**HEBREW_NAME_PARTS (Hebrew script):**
*primary-name*: For example, \"אבן גבירול\", \"הרמב\"ם\". A commonly recognized name for a person.
*given-name*: For example, \"משה\", \"שלמה\", \"לאה\".
*alternative-name*: For example, \"ציפי\" in \" ציפי (ציפורה) שביט\".
*middle-name*: For example, \"הלל\" in \"יצחק הלל בן ששון\".
*surname*: For example, \"שליט\" in \"גלעד שליט\".
*patronymic*: For example, \"בן משה\", \"בן יצחק\". May include multiple forefather names, like \"בן אליהו בן יוסף\".
*matronymic*: For example, \"בת מרים\".
*honorific*: For example, \"מורנו\", \"הרב\".
*acronym*: For example, \"רמב\"ם\".
*teknonym*: For example, \"אבא יוסף\".
*professional-name*: For example, \"הדיין\" used in professional context.
*nisba*: For regional or familial origin, such as \"מפראג\" or \"הגלעדי\".
*qualifier*: For example, \"השני\" (the second).
*appellation*: For example, \"הכהן\", \"הרב\".
*salutation*: For example, \"ד\"ר\", \"רב\".""")

GERMAN_NAME_PARTS = (['primary-name', 'given-name', 'surname', 'honorific', 'salutation'], """**GERMAN_NAME_PARTS:**
*primary-name*: For example, \"Goethe\", \"Beethoven\". A commonly recognized way of referring to a person.
*given-name*: For example, \"Johann\", \"Heinrich\", \"Anna\".
*alternative-name*: For example, \"Tzipi\" in \"Tzipi (Tzipora) Shavit\".
*surname*: For example, \"Schneider\" in \"Paul Schneider\".
*honorific*: For example, \"Herr\", \"Frau\".
*salutation*: For example, \"Dr.\", \"Prof.\".""")

BASIC_PROMPT =  'Act as an expert linguist and historian versed in the {language} language and culture. Given a ' \
                'name try to parse it into its basic parts. Return a dictionary with one or more of ' \
                'the following keys: {name_parts}. Here is an example: {example}. ' \
                'Review your work and make sure the name parts specified appear in the list given. ' \
                'Make sure to return the name parts in the same language and script as the input name.'
INSTRUCTIONS = 'The name is "{name}". Here is some background information about this person: {background}.'
EXAMPLE_HE = {'name': 'רבי ישראל בן אליעזר הבעש"ט', 'language': 'he', 'name_parts': HEBREW_NAME_PARTS_HEBREW,
              'background': 'A Jewish Rabbi and spiritual leader from the 18th century',
              'parts': {"given": "ישראל", "patronymic": "בן אליעזר", "acronym": "הבעש\"ט", "primary-name": "הבעש\"ט"}}
EXAMPLE_HE_L = {'name': 'Rabbi Yisrael ben Eliezr HaBa\'al Shem Tov', 'language': 'heL', 'name_parts': HEBREW_NAME_PARTS_LATIN,
                'background': 'A Jewish Rabbi and spiritual leader from the 18th century',
                'parts': {"given": "Yisrael", "patronymic": "ben Eliezr", "primary-name": "HaBa'al Shem Tov"}}

EXAMPLE_HE_L_M = {'name': 'Rabbi Yisrael ben Eliezr HaBa\'al Shem Tov', 'language': 'heL', 'name_parts': HEBREW_NAME_PARTS_LATIN,
                'background': 'A Jewish Rabbi and spiritual leader from the 18th century',
                'parts': {"given": "Yisrael", "patronymic": "ben Eliezr", "primary-name": "HaBa'al Shem Tov"}}

EXAMPLE_AR = {'name': 'عبد المسيح بن عبد الله ابن ناعمة الحمصي', 'language': 'ar', 'name_parts': ARABIC_NAME_PARTS,
              'background': 'None',
              'parts': {"given": "عبد المسيح", "patronymic": "بن عبد الله", "matronymic": "ابن ناعمة",
                        "nisba": "الحمصي"}}
EXAMPLE_ARL = {'name': 'ʿAbd al-Masīḥ bin ʿAbd Allāh ibn Nāʿima al-Ḥimṣī', 'language': 'arL',
               'name_parts': ARABIC_NAME_PARTS_LATIN,
               'background': 'Abd al-Masih b. Naʿima of Homs',
               'parts': {"given": "ʿAbd al-Masīḥ", "patronymic": "bin ʿAbd Allāh", "matronymic": "ibn Nāʿima",
                         "nisba": "al-Ḥimṣī"}}
EXAMPLE_GE = ''
EXAMPLE_EN = {'name': 'Lord Jeffrey Earl Chaucer the third of Yorkshire', 'language': 'en',
              'name_parts': BASIC_NAME_PARTS,
              'background': 'A British Lord and poet from the 14th century',
              'parts': {"given": "Jeffrey", "middle-name": "Earl", "surname": "Chaucer", "qualifier": "the third"
                  , "appellation": "Lord", "nisba": "of Yorkshire"}}

# Here we can create specific prompts for different languages or cultures
LANGS = {'he': {'language': 'Hebrew', 'parts': HEBREW_NAME_PARTS_HEBREW, 'example': EXAMPLE_HE,
                'description': 'Hebrew name in Hebrew scipt'},
         'heL': {'language': 'Hebrew', 'parts': HEBREW_NAME_PARTS_LATIN, 'example': EXAMPLE_HE_L,
                 'description': 'Hebrew name in Latin script from medieval or earlier periods'},
         'heLM': {'language': 'Hebrew', 'parts': MODERN_HEBREW_NAME_PARTS_LATIN, 'example': EXAMPLE_HE_L_M,
                  'description': 'Hebrew name in Latin script from modern times'},
         'ar': {'language': 'Arabic', 'parts': ARABIC_NAME_PARTS, 'example': EXAMPLE_AR,
                'description': 'Arabic name in Arabic script'},
         'arL': {'language': 'Arabic', 'parts': ARABIC_NAME_PARTS_LATIN, 'example': EXAMPLE_ARL,
                 'description': 'Arabic name in Arabic script'},
         'de': {'language': 'German', 'parts': GERMAN_NAME_PARTS, 'example': EXAMPLE_GE,
                'description': 'German name in German script'},
         'en': {'language': 'English', 'parts': BASIC_NAME_PARTS, 'example': EXAMPLE_EN,
                'description': 'Name in English or an unknown language in English script'}}
