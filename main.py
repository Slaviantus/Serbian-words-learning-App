from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from App_database import App_database
from kivy. uix. button import Button
from kivy. uix. label import Label
from Vocabulary_machine import Vocabulary_machine
from File_module_manager import File_module_manager
from kivy.core.window import Window
from kivy.clock import Clock
import random

Config.set('kivy', 'exit_on_escape', '0')


from kivy.lang import Builder

database = None
vocabulary_machine = None
file_module_manager = None


class StartWindow(Screen):
    pass



class ModulesViewWindow(Screen):


    def __init__(self, **kwargs):
        """Bind escape key for going to the start page
        works in all pages of application"""

        super(ModulesViewWindow, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back_click)


    def on_open_window(self):

        self.modules = database.Get_all_modules()

        button_height = self.height * 0.07
        self.modules_list.size_hint_y = button_height * len(self.modules) / 200


        for i in range(len(self.modules)):

            item = Module_Button(text = str(self.modules[i][1]),
                                 on_press = self.choose_module,
                                 font_name= 'clacon2.ttf',
                                 color = (0.549, 0.941, 0.627, 1),
                                 background_color = (0, 0, 0, 0),
                                 font_size = 0.04 * self.height,
                                 halign = 'left',
                                 )
            item.Button_index = str(i)

            separator = Label(text="----------------------------------",
                              color=(0.549, 0.941, 0.627, 1))

            self.modules_list.add_widget(item)
            self.modules_list.add_widget(separator)


    def choose_module(self, module):

        database.current_module_id = self.modules[int(module.Button_index)][0]
        self.manager.current = 'edit_module'


    def on_close_window(self):

        self.modules_list.clear_widgets()


    def Android_back_click(self, window, key, *largs):

        if key == 27: # 27 - escape key
            self.manager.current = 'start'




class Module_Button(Button):

    def __init__(self, **kwargs):
        super(Module_Button, self).__init__(**kwargs)

        self.__button_index = 0


    @property
    def Button_index(self):

        return self.__button_index


    @Button_index.setter
    def Button_index(self, value: int):

        self.__button_index = value





class EditModuleWindow(Screen):

    def on_open_window(self):

        self.is_module_edited = False

        self.module = database.Get_module(database.current_module_id)
        self.words = database.Get_all_words_of_module(database.current_module_id)

        button_height = self.height * 0.07
        self.words_list.size_hint_y = button_height * len(self.words) / 100


        self.name_display.text = self.module[0][1]
        self.description_display.text = self.module[0][2]
        self.author_display.text = "by " + self.module[0][3]
        self.total_words.text = "WORDS=" + str(len(self.words))

        for i in range(0, len(self.words)):

            button_text = str(self.words[i][1]) + "\n" + str(self.words[i][2]) + "\n" + str(self.words[i][3])

            print(button_text)

            item = Module_Button(text = button_text,
                                 width = self.width - 80,
                                 halign = "left",
                                 background_color = (0, 0, 0, 0),
                                 color = (0.549, 0.941, 0.627, 1),
                                 font_size = 20,
                                 font_name='clacon2.ttf',
                                 on_press = self.choose_word)
            item.Button_index = i

            separator = Label(text="----------------------------------", color=(0.549, 0.941, 0.627, 1))

            self.words_list.add_widget(item)
            self.words_list.add_widget(separator)


    def choose_word(self, word):

        database.current_word_id = self.words[int(word.Button_index)][0]
        self.manager.current = 'edit_word'


    def on_edit_button_clicked(self):

        self.name_display.readonly = False
        self.description_display.readonly = False
        self.author_display.readonly = False
        self.is_module_edited = True


    def on_back_button_clicked(self):

        if self.is_module_edited:

            id = database.current_module_id
            new_name = self.name_display.text
            new_description = self.description_display.text
            new_author = self.author_display.text

            database.Edit_module(id, new_name, new_description, new_author)


    def on_close_window(self):

        self.words_list.clear_widgets()


class EditWordWindow(Screen):

    def on_open_window(self):

        self.word = database.Get_word(database.current_word_id)

        self.edit_cyrilic.text = str(self.word[0][1])
        self.edit_latin.text = str(self.word[0][2])
        self.edit_translation.text = str(self.word[0][3])


    def on_delete_button_clicked(self):

        id = database.current_word_id
        database.Delete_word(id)


    def on_close_window(self):

        id = database.current_word_id
        new_cyrilic = self.edit_cyrilic.text
        new_latin = self.edit_latin.text
        new_translation = self.edit_translation.text

        database.Edit_word(id, new_cyrilic, new_latin, new_translation)



class AddModuleWindow(Screen):

    def on_add_module_clicked(self):

        database.Add_module(self.enter_name.text, self.enter_description.text, self.enter_author.text)



class ModuleDeleteWindow(Screen):

    def on_open_window(self):

        id = database.current_module_id
        module = database.Get_module(id)
        self.module_name.text = "ARE YOU SURE YOU WANT TO DELETE MODULE " + str(module[0][1]) + "?"


    def on_Yes_button_clicked(self):

        id = database.current_module_id
        database.Delete_module(id)



class AddWordWindow(Screen):

    def on_open_window(self):

        self.enter_cyrilic.text = ''
        self.enter_latin.text = ''
        self.enter_translation.text = ''

    def on_add_word_clicked(self):

        id = database.current_module_id
        database.Add_word(self.enter_cyrilic.text, self.enter_latin.text, self.enter_translation.text, id)



class ModulesListWindow(Screen):


    def on_open_window(self):

        self.modules = database.Get_all_modules()

        button_height = self.height * 0.07
        self.modules_list.size_hint_y = button_height * len(self.modules) / 200

        for i in range(0, len(self.modules)):

            sum_module_words = len(database.Get_all_words_of_module(self.modules[i][0]))

            left_column = self.__display_module(i, sum_module_words)
            right_column = self.__display_module_progress(i)

            left_separator = Label(text="----------------------------------", color=(0.549, 0.941, 0.627, 1))
            right_separator = Label(text="----------------------------------", color=(0.549, 0.941, 0.627, 1))

            self.modules_list.add_widget(left_column)
            self.modules_list.add_widget(right_column)

            self.modules_list.add_widget(left_separator)
            self.modules_list.add_widget(right_separator)


    def open_module(self, module):

        database.current_module_id = self.modules[int(module.Button_index)][0]
        self.modules_list.clear_widgets()
        self.manager.current = 'introduction_module'


    def __display_module(self, module_index: int, sum_words: int):

        module_name = "[ " + str(self.modules[module_index][1]) + " ]"
        empty_module_information = "[ " + str(self.modules[module_index][1]) + " (NO WORDS)" + " ]"

        left_column = Module_Button(text=module_name if sum_words != 0 else empty_module_information,
                                    height=60,
                                    width=self.width - 80,
                                    halign="left",
                                    background_color=(0, 0, 0, 0),
                                    color=(0.549, 0.941, 0.627, 1),
                                    disabled_color=(0.549, 0.941, 0.627, 1),
                                    font_size=20,
                                    font_name='clacon2.ttf',
                                    size_hint_y=None,
                                    on_press=self.open_module,
                                    disabled=True if sum_words == 0 else False)
        left_column.Button_index = module_index

        return left_column


    def __display_module_progress(self, module_index: int):

        module_progress = str(vocabulary_machine.Progress_rate(database.Get_all_words_of_module(self.modules[module_index][0]))) + "%"

        right_column = Label(text=module_progress,
                             background_color=(0, 0, 0, 0),
                             color=(0.549, 0.941, 0.627, 1),
                             height=60,
                             width=60,
                             font_size=20,
                             font_name='clacon2.ttf',
                             size_hint_y=None)
        return right_column


    def on_close_window(self):

        self.modules_list.clear_widgets()


class IntroductionModuleWindow(Screen):


    def on_open_window(self):

        module_id = database.current_module_id
        module = database.Get_module(module_id)
        words_list = database.Get_all_words_of_module(module_id)
        vocabulary_machine.Load_words(words_list)
        progress = vocabulary_machine.Progress_rate(words_list)

        self.name_display.text = module[0][1]
        self.author_display.text = "by " + module[0][3]
        self.description_display.text = module[0][2]
        self.total_words.text = "WORDS = " + str(len(words_list))
        self.progress_label.text = "PROGRESS = " + str(progress) + "%"
        self.alphabet_label.text = str(vocabulary_machine.Alphabet.name)
        self.__name_alpchabet_label()

        if vocabulary_machine.Is_module_learnt():

            self.learn_button.text = "LEARN AGAIN"

        else:

            self.learn_button.text = "LEARN"


    def on_changing_alphabet(self):

        current_alphabet = vocabulary_machine.Alphabet.name

        if current_alphabet == "CYRILIC":

            vocabulary_machine.Alphabet = "LATIN"
            self.__name_alpchabet_label()

        else:

            vocabulary_machine.Alphabet = "CYRILIC"
            self.__name_alpchabet_label()


    def __name_alpchabet_label(self):

        self.alphabet_label.text = str(vocabulary_machine.Alphabet.name)


    def on_learn_button_clicked(self):

        if vocabulary_machine.Is_module_learnt():
            vocabulary_machine.Reset_learning_progress()

        next_page = vocabulary_machine.Next_page()


        if next_page == "U":

            self.manager.current = 'choose_word'

        else:

            self.manager.current = 'typing_answer'



class TypingAnswerWindow(Screen):

    def __init__(self, **kwargs):

        super(TypingAnswerWindow, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard_down)


    def on_open_window(self):

        self.answer_text_input.focus = True
        self.__clear_window()

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)

        self.__current_word = vocabulary_machine.Get_choosed_word()
        self.translation_label.text = self.__current_word[2]


    def on_enter_button_clicked(self):

        answer = self.answer_text_input.text
        vocabulary_machine.Judge_answer(answer)

        if vocabulary_machine.Is_module_learnt():
            words_list = vocabulary_machine.Unload_words()
            database.Save_learning_progress_of_module(words_list)
            self.__go_to_congratulation_page()

        else:
            self.__go_to_transition_page()


    def on_back_button_clicked(self):

        module_words = vocabulary_machine.Unload_words()
        database.Save_learning_progress_of_module(module_words)


    def __go_to_transition_page(self):
        self.manager.current = 'transition_page'


    def __go_to_congratulation_page(self):
        self.manager.current = "congratulations"


    def __clear_window(self):

        self.answer_text_input.text = ""


    def set_multiline_true(self):

        text_length = len(self.answer_text_input.text)
        if text_length == 1:
            self.answer_text_input.multiline = True


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])

        if coef == 0:
            coef = 0.001

        self.progress_level.size_hint_x = self.scale.width * coef
        self.empty_progress.size_hint_x = self.scale.width * (1 - coef)


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])


    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.answer_text_input.focus and keycode == 40:  # 40 - Enter key pressed
            self.on_enter_button_clicked()




class TransitionPageWindow(Screen):

    def on_open_window(self):

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)
        self.__save_learning_progress()
        self.__take_decision_from_answer()


    def __go_to_page_with_next_word(self):

        page_type = vocabulary_machine.Next_page()

        if page_type == "U":
            Clock.schedule_once(self.go_to_choose_word_page, 0.5)

        else:
            Clock.schedule_once(self.go_to_typing_answer_page, 0.5)


    def __go_to_correct_mistake(self, current_word):

        if current_word[5] == "K":
            Clock.schedule_once(self.go_to_mistake_correction_page, 0.5)

        else:
            self.__go_to_page_with_next_word()


    def go_to_choose_word_page(self, delay):
        self.manager.current = 'choose_word'


    def go_to_typing_answer_page(self, delay):
        self.manager.current = 'typing_answer'


    def go_to_mistake_correction_page(self, delay):
        self.manager.current = 'mistake_correction'


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])

        if coef == 0:
            coef = 0.001

        self.progress_level.size_hint_x = self.scale.width * coef
        self.empty_progress.size_hint_x = self.scale.width * (1 - coef)


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])


    def __display_verdict(self, is_correct):

        if is_correct:
            self.verdict_label.text = "==========\nCORRECT!\n=========="

        else:
            self.verdict_label.text = "==========\nWRONG!\n=========="


    def __save_learning_progress(self):

        module_words = vocabulary_machine.Unload_words()
        database.Save_learning_progress_of_module(module_words)


    def __take_decision_from_answer(self):

        is_correct = vocabulary_machine.Is_answer_was_correct()
        current_word = vocabulary_machine.Get_current_word()

        self.__display_verdict(is_correct)

        if is_correct:
            self.__go_to_page_with_next_word()

        else:
            self.__go_to_correct_mistake(current_word)



class MistakeCorrectionWindow(Screen):

    def __init__(self, **kwargs):

        super(MistakeCorrectionWindow, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard_down)


    def on_open_window(self):

        self.__clear_window()
        self.answer_text_input.focus = True

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)
        self.__display_correct_answer()


    def __display_correct_answer(self):

        if vocabulary_machine.Alphabet.name == "CYRILIC":
            self.original_word_label.text = vocabulary_machine.Get_current_word()[1]

        else:
            self.original_word_label.text = vocabulary_machine.Get_current_word()[2]


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])


    def __clear_window(self):

        self.answer_text_input.text = ""


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])

        if coef == 0:
            coef = 0.001

        self.progress_level.size_hint_x = self.scale.width * coef
        self.empty_progress.size_hint_x = self.scale.width * (1 - coef)


    def set_multiline_true(self):

        text_length = len(self.answer_text_input.text)
        if text_length == 1:
            self.answer_text_input.multiline = True


    def on_enter_button_clicked(self):

        answer = self.answer_text_input.text
        is_correct = vocabulary_machine.Check_answer(answer)

        if is_correct:
            self.__go_to_transition_page()


    def __go_to_transition_page(self):
        self.manager.current = 'transition_page'


    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.answer_text_input.focus and keycode == 40:  # 40 - Enter key pressed
            self.on_enter_button_clicked()


class ImportModuleWindow(Screen):

    def on_open_window(self):
        self.__clear_window()
        self.__enable_import_button()


    def on_import_button_clicked(self):

        txt_file_lines = file_module_manager.load_module_file()
        self.__display_txt_file(txt_file_lines)

        self.__imported_module = file_module_manager.extract_module(txt_file_lines)

        self.__add_module()
        self.__add_words()
        self.__disable_import_button()


    def __add_module(self):

        module_name = self.__imported_module[0]
        module_author = self.__imported_module[1]
        module_description = self.__imported_module[2]

        database.Add_module(module_name, module_description, module_author)


    def __add_words(self):

        module_id = self.__get_last_moduleId()

        for i in range(3, len(self.__imported_module)):

            cyrilic = self.__imported_module[i][0]
            latin = self.__imported_module[i][1]
            translation = self.__imported_module[i][2]

            database.Add_word(cyrilic, latin, translation, module_id)


    def __get_last_moduleId(self) -> int:

        modules = database.Get_all_modules()
        id_list = list()

        for i in range(len(modules)):
            id_list.append(modules[i][0])

        return max(id_list)


    def __display_txt_file(self, txt_file_lines):

        txt_str = ''.join(txt_file_lines)
        self.module_display.text = txt_str


    def __clear_window(self):

        self.module_display.text = ''


    def __disable_import_button(self):

        self.import_button.disabled = True
        self.import_button.text = ''


    def __enable_import_button(self):

        self.import_button.disabled = False
        self.import_button.text = "IMPORT"





class ChooseWordWindow(Screen):


    def on_open_window(self):

        self.__enable_all_buttons()

        words_states = vocabulary_machine.Calculate_words_states()
        self.__update_progress_bar(words_states)
        self.__display_words_states(words_states)

        self.__import_answer_variants()


    def __display_words_variants(self, variants):

        if vocabulary_machine.Alphabet.name == "CYRILIC":
            self.__display_cyrilic_variants(variants)

        else:
            self.__display_latin_variants(variants)


    def __display_cyrilic_variants(self, variants):

        self.variant_1.text = variants[0][0]
        self.variant_2.text = variants[1][0]
        self.variant_3.text = variants[2][0]
        self.variant_4.text = variants[3][0]


    def __display_latin_variants(self, variants):

        self.variant_1.text = variants[0][1]
        self.variant_2.text = variants[1][1]
        self.variant_3.text = variants[2][1]
        self.variant_4.text = variants[3][1]


    def __import_answer_variants(self):

        correct_word = vocabulary_machine.Get_choosed_word()
        self.translation_label.text = correct_word[2]

        answer_variants = vocabulary_machine.Get_3_random_words()
        answer_variants.append([correct_word[0], correct_word[1]])

        random.shuffle(answer_variants)

        self.__display_words_variants(answer_variants)


    def on_variant_word_clicked(self, button, variant: str):

        vocabulary_machine.Judge_answer(variant)
        self.__disable_all_buttons()
        self.__go_to_transition_page()


    def __disable_all_buttons(self):

        self.variant_1.disabled = True
        self.variant_2.disabled = True
        self.variant_3.disabled = True
        self.variant_4.disabled = True


    def __enable_all_buttons(self):

        self.variant_1.disabled = False
        self.variant_2.disabled = False
        self.variant_3.disabled = False
        self.variant_4.disabled = False


    def __update_progress_bar(self, words_states: tuple):

        coef = words_states[2] / (words_states[0] + words_states[1] + words_states[2])

        if coef == 0:
            coef = 0.001

        self.progress_level.size_hint_x = self.scale.width * coef
        self.empty_progress.size_hint_x = self.scale.width * (1 - coef)


    def __display_words_states(self, words_states: tuple):

        self.sum_unknown.text = str(words_states[0])
        self.sum_known.text = str(words_states[1])
        self.sum_learned.text = str(words_states[2])


    def on_back_button_clicked(self):

        module_words = vocabulary_machine.Unload_words()
        database.Save_learning_progress_of_module(module_words)


    def __go_to_transition_page(self):

        self.manager.current = 'transition_page'





class CongratulationsWindow(Screen):

    pass



class WindowManager(ScreenManager):

    def on_open_window(self):

        pass



class SrpskiApp(App):
    def build(self):

        Builder.load_file("srpski.kv")




if __name__ == '__main__':

    database = App_database()
    vocabulary_machine = Vocabulary_machine()
    file_module_manager = File_module_manager()
    SrpskiApp().run()







