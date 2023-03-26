import random
from enum import Enum


class Alphabet(Enum):

    CYRILIC = 0
    LATIN = 1


class Vocabulary_machine:

    def __init__(self):

        self.__not_learned_words = list()
        self.__learned_words = list()
        self.__current_word = None
        self.__is_answer_correct = None
        self.__current_alphabet = Alphabet.CYRILIC


    def Load_words(self, list_words):
        """Loading words of module from database"""

        for i in range(0, len(list_words)):

            if list_words[i][5] == "L":
                self.__learned_words.append(list_words[i])

            else:
                self.__not_learned_words.append(list_words[i])


    @property
    def Alphabet(self):
        return self.__current_alphabet


    @Alphabet.setter
    def Alphabet(self, alphabet_name: str):

        if alphabet_name == "CYRILIC":
            self.__current_alphabet = Alphabet.CYRILIC
        elif alphabet_name == "LATIN":
            self.__current_alphabet = Alphabet.LATIN
        else:
            print("Wrong Alphabet setting")


    def Check_answer(self, answer: str) -> bool:

        answer = self.__remove_odd_spaces(answer).lower()

        if self.Alphabet.name == "CYRILIC":
            check_word = self.__current_word[1].lower()

        else:
            check_word = self.__current_word[2].lower()

        self.__is_answer_correct = answer == check_word

        return self.__is_answer_correct


    def Judge_answer(self, entered_word: str) -> bool:

        is_correct = self.Check_answer(entered_word)

        if is_correct:

            if self.__current_word[5] == "U":

                self.__Change_state_of_word(self.__current_word, "K")

                self.__is_answer_correct = True

            if self.__current_word[5] == "K":

                if int(self.__current_word[6]) == 0:
                    self.__Change_state_of_word(self.__current_word, "L")

                else:
                    self.__Inc_Dec_Mistake(self.__current_word, "-")

            self.__is_answer_correct = True

        else:

            if self.__current_word[5] == "K":

                self.__Inc_Dec_Mistake(self.__current_word, "+")

            self.__is_answer_correct = False

        return self.__is_answer_correct



    def Is_answer_was_correct(self):

        return self.__is_answer_correct



    def __Change_state_of_word(self, current_word: tuple, new_state: str):

        updated_word = list()

        for i in range(len(current_word)):

            if i == 5:
                updated_word.append(new_state)
            else:
                updated_word.append(current_word[i])

        if new_state == "U":    # if L -> U (reset)
            self.__learned_words.remove(current_word)
            self.__not_learned_words.append(updated_word)
        else:
            self.__not_learned_words.remove(current_word)


        if new_state == "K":    # if U -> K
            self.__not_learned_words.append(updated_word)

        if new_state == "L":    # if K -> L
            self.__learned_words.append(updated_word)


    def __Inc_Dec_Mistake(self, current_word: tuple, fine: str):
        """Increments mistake fine of word if the answer was incorrect
        fine has to be equals "+"
        Decrements mistake fine of word if the answer was correct
        fine has to be equals "-"
        """

        mistake_rate = int(current_word[6])

        if fine == "+":
            mistake_rate += 1
        else:
            mistake_rate -= 1

        updated_word = list()

        for i in range(6):
            updated_word.append(current_word[i])

        updated_word.append(str(mistake_rate))

        self.__not_learned_words.remove(current_word)
        self.__not_learned_words.append(updated_word)



    def Get_choosed_word(self):
        """Returns the current word to display
        (only cyrilic, latin and translation)"""

        return [self.__current_word[1], self.__current_word[2], self.__current_word[3]]


    def Get_current_word(self):

        return self.__current_word


    def Get_3_random_words(self) -> list:
        """select 3 random words from other words
        of module for display variants on choose_word page """

        random_words = list()
        indexes = list()
        all_words = self.__learned_words + self.__not_learned_words

        #____________ In case when the number of words in module is extremely few (<4) _________
        if len(all_words) < 4:
            k = 0

            for i in range(3):

                if k == len(all_words):
                    k = 0

                chosen_word = [all_words[k][1], all_words[k][2]]
                random_words.append(chosen_word)
                k += 1

            return random_words

        # ____________ In case when the number of words in module is normal (>4) _________
        while len(random_words) < 3:

            random_word_index = random.randint(0, len(all_words) - 1)

            if all_words[random_word_index][0] != self.__current_word[0]:

                if len(random_words) < 1 or self.__Is_index_differet(indexes, random_word_index):

                    chosen_word = [all_words[random_word_index][1], all_words[random_word_index][2]]
                    random_words.append(chosen_word)
                    indexes.append(random_word_index)

        return random_words


    def __Is_index_differet(self, indexes: list, random_index: int) -> bool:
        """checks if index is different from other indexes in list
           indexes have to be different, because words have to be different
           on choose_word page"""

        for i in range(len(indexes)):

            if random_index == indexes[i]:
                return False

        return True


    def Is_module_learnt(self) -> bool:
        """Checks if all words in module are learnt returns true, if not - false"""

        if len(self.__not_learned_words) == 0:
            return True
        else:
            return False


    def Next_page(self) -> str:
        """"""

        self.__Choose_random_word()
        return self.__current_word[5]


    def __Choose_random_word(self):

        random_word_index = random.randint(0, len(self.__not_learned_words) - 1)
        self.__current_word = self.__not_learned_words[random_word_index]


    def Unload_words(self):
        """Loading words (saving) words to database"""

        return self.__not_learned_words + self.__learned_words


    def Progress_rate(self, module_words: list) -> int:
        """Calculating the progress of learning words in module in %"""

        all_words = len(module_words)

        if all_words == 0:
            return 0

        learned_words = 0
        for i in range(0, all_words):

            if module_words[i][5] == "L":
                learned_words += 1

        return int((learned_words / all_words) * 100)


    def Calculate_words_states(self):
        """Calculates the sum of Unknown words, Known words and Learned words"""

        sum_unknown_words = 0
        sum_known_words = 0
        sum_learned_words = len(self.__learned_words)

        for i in range(len(self.__not_learned_words)):

            if self.__not_learned_words[i][5] == "U":

                sum_unknown_words += 1

            else:

                sum_known_words += 1

        return sum_unknown_words, sum_known_words, sum_learned_words


    def Reset_learning_progress(self):

        if self.Is_module_learnt():

            length = len(self.__learned_words)

            while length > 0:

                word = self.__learned_words[length - 1]
                self.__Change_state_of_word(word, "U")
                length = length - 1

        else:

            print("Module has still not learnt words")


    def __remove_odd_spaces(self, dirty_word):
        """Removes odd spaces of entered word"""
        clean_word = list()
        dirty_word = str.strip(dirty_word)

        i = 0
        while i < len(dirty_word):

            if dirty_word[i] == " " and dirty_word[i + 1] == " ":
                i += 1

            else:
                clean_word.append(dirty_word[i])
                i += 1

        return ''.join(clean_word)





    #=========== FOR TEST ===========================
    def Log_words(self):

        self.Get_Unlearned_Words()
        self.Get_Known_Words()
        self.Get_Learned_Words()


    def Get_Unlearned_Words(self):

        print("====================================================================")

        not_learned_words = self.__not_learned_words

        result_words = list()

        for i in range(len(not_learned_words)):

            if not_learned_words[i][5] == "U":

                result_words.append(not_learned_words[i][1])

        print("--------- UNLEARNED ----------")
        for i in range(len(result_words)):

            print(result_words[i])


    def Get_Known_Words(self):

        known_words = self.__not_learned_words

        result_words = list()

        for i in range(len(known_words)):

            if known_words[i][5] == "K":
                result_words.append(known_words[i][1])

        print("--------- KNOWN ----------")
        for i in range(len(result_words)):
            print(result_words[i])

    def Get_Learned_Words(self):

        learned_words = self.__learned_words
        print("--------- LEARNED ----------")

        for i in range(len(learned_words)):

            print(learned_words[i][1])

















