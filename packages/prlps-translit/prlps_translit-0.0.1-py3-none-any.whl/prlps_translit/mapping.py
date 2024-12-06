class TranslitSchema:
    """
    класс для маппинга транслитерации на основе словаря
    """

    def __init__(self, mapping: dict, prev_mapping: dict = None, next_mapping: dict = None, ending_mapping: dict = None):
        self.map = self._create_map(mapping)
        self.prev_map = self._create_special_map(prev_mapping or {}, capitalize=False, upper=False)
        self.next_map = self._create_special_map(next_mapping or {}, capitalize=True, upper=True)
        self.ending_map = self._create_special_map(ending_mapping or {}, capitalize=False, upper=True)

    @staticmethod
    def _create_map(mapping: dict):
        upper_map = {key.capitalize(): value.capitalize() for key, value in mapping.items()}
        mapping.update(upper_map)
        return mapping

    @staticmethod
    def _create_special_map(mapping: dict, capitalize: bool, upper: bool):
        result = {}
        for key, value in mapping.items():
            if capitalize:
                result[key.capitalize()] = value.capitalize()
            if upper:
                result[key.upper()] = value.upper()
            result[key] = value
        return result

    def get_translation(self, prev: str, curr: str, next_: str) -> str:
        return self.prev_map.get(prev + curr) or self.next_map.get(curr + next_) or self.map.get(curr, curr)

    def get_ending_translation(self, ending: str) -> str:
        return self.ending_map.get(ending)


cyr_to_lat = TranslitSchema(
    mapping={
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    },
    prev_mapping={
        'е': 'ye', 'ае': 'ye', 'ие': 'ye', 'ое': 'ye', 'уе': 'ye', 'эе': 'ye', 'юе': 'ye', 'яе': 'ye', 'ье': 'ye', 'ъе': 'ye'
    },
    next_mapping={
        'ъа': 'y', 'ъи': 'y', 'ъо': 'y', 'ъу': 'y', 'ъы': 'y', 'ъэ': 'y', 'ьа': 'y', 'ьи': 'y', 'ьо': 'y', 'ьу': 'y', 'ьы': 'y', 'ьэ': 'y'
    },
    ending_mapping={
        'ий': 'y', 'ый': 'y'
    }
)
