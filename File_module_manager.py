from tkinter import Tk
from tkinter import filedialog

class File_module_manager:
    """This class is responsible for import / export all module with included words,
    If you need to import. You need to create .txt file, that has to be in following format:
    <name>
    <author>
    <description>
    [Cyrilic/Latin/Translation]
    [Cyrilic/Latin/Translation] etc... """


    def load_module_file(self) -> list:
        """Loads module file of txt format from file directory represents by list"""

        Tk().withdraw()
        file_path = filedialog.askopenfilename(title = "Open document", filetypes = (("txt Text notepad document","*.txt"),))

        if (file_path != ''):
            text_file = open(file_path, "r", encoding="utf-8")
            txt_lines = text_file.readlines()

        return txt_lines


    def extract_module(self, txt_lines: list) -> list:
        """Extracts module data from txt file to list"""

        clean_list = list()
        self.__extract_all_properties(txt_lines, clean_list)

        return  self.__extract_all_words(txt_lines, clean_list)


    def __extract_module_property(self, property: str) -> str:

        return property.split('<')[1].split('>')[0]


    def __extract_word(self, word: str) -> tuple:

        splitedword = word.split('/')
        cyrilic = splitedword[0].split('[')[1]
        latin = splitedword[1]
        translation = splitedword[2].split(']')[0]

        return cyrilic, latin, translation


    def __is_line_contains_property(self, line: str) -> bool:

        start_marker = '<'
        end_marker = '>'

        return self.__is_contains_markers(line, start_marker, end_marker)


    def __is_line_contains_word(self, line: str) -> bool:

        start_marker = '['
        end_marker = ']'

        return self.__is_contains_markers(line, start_marker, end_marker)


    def __is_contains_markers(self, line: str, start_marker: str, end_marker: str) -> bool:

        for i in range(0, len(line)):
            if line[i] == start_marker:
                for j in range(i, len(line)):
                    if line[j] == end_marker:
                        return True
        return False


    def __extract_all_properties(self, txt_lines: list, clean_list: list) -> list:

        for i in range(0, len(txt_lines)):
            if self.__is_line_contains_property(txt_lines[i]):
                clean_list.append(self.__extract_module_property(txt_lines[i]))

        return clean_list


    def __extract_all_words(self, txt_lines: list, clean_list: list) -> list:

        for i in range(0, len(txt_lines)):
            if self.__is_line_contains_word(txt_lines[i]):
                clean_list.append(self.__extract_word(txt_lines[i]))

        return clean_list