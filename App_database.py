import sqlite3

class App_database:

    def __init__(self):
        """Initialization of database"""

        self.__connection = sqlite3.connect('srpski_database.db')
        self.__cursor = self.__connection.cursor()

        """______ Creating the table of modules ______"""

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS modules(
            moduleid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            author TEXT);
        """)

        self.__connection.commit()

        """______ Creating the table of words ______"""

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS words(
            wordid INTEGER PRIMARY KEY AUTOINCREMENT,
            cyrilic TEXT,
            latin TEXT,
            translation TEXT,
            moduleid TEXT,
            status TEXT,
            mistakes INTEGER);
        """)

        self.__connection.commit()

        self.current_module_id = None
        self.current_word_id = None


    def Add_word(self, cyrilic_word: str, latin_word: str, translation: str, moduleid: int):
        """Add word into database"""

        word = (cyrilic_word, latin_word, translation, moduleid, "U", 0)
        self.__cursor.execute("INSERT INTO words (cyrilic, latin, translation, moduleid, status, mistakes) VALUES(?,?,?,?,?,?);", word)
        self.__connection.commit()


    def Add_module(self, name: str, description: str, author: str):
        """Add module into database"""

        module = (name, description, author)
        self.__cursor.execute("INSERT INTO modules (name, description, author) VALUES(?, ?, ?);", module)
        self.__connection.commit()


    def Delete_module(self, idmodule: int):
        """Delete all module with words"""

        words = self.Get_all_words_of_module(idmodule)

        for i in range(0, len(words)):
            self.Delete_word(words[i][0])
        self.__connection.commit()

        self.__cursor.execute("DELETE FROM modules WHERE moduleid = ?", (idmodule,))
        self.__connection.commit()


    def Delete_word(self, idword: int):
       """Delete word from database"""

       self.__cursor.execute("DELETE FROM words WHERE wordid = ?", (idword,))
       self.__connection.commit()


    def Get_all_words_of_module(self, idmodule: int) -> list:
        """Select and return all words from module"""

        self.__cursor.execute("SELECT * FROM words WHERE moduleid = ?", (idmodule,))
        words = self.__cursor.fetchall()
        self.__connection.commit()

        return words


    def Save_learning_progress_of_module(self, module_words: list):
        """Saves into database all learning states of words, mistakes (fine rates) of words in module"""

        for i in range(len(module_words)):

            wordid = module_words[i][0]
            new_state = module_words[i][5]
            new_mistakes = module_words[i][6]
            new_word = (new_state, new_mistakes, wordid)
            self.__cursor.execute("UPDATE words SET status = ?, mistakes = ? WHERE wordid = ?", new_word)
            self.__connection.commit()


    def Edit_word(self, wordid: int, cyrilic_word: str, latin_word: str, translation: str):
        """Changing data in word"""

        new_word = (cyrilic_word, latin_word, translation, wordid)
        self.__cursor.execute("UPDATE words SET cyrilic = ?, latin = ?, translation = ? WHERE wordid = ?", new_word)
        self.__connection.commit()


    def Edit_module(self, moduleid: int, name: str, description: str, author: str):
        """Changing data in module"""

        new_module = (name, description, author, moduleid)
        self.__cursor.execute("UPDATE modules SET name = ?, description = ?, author = ? WHERE moduleid = ?", new_module)
        self.__connection.commit()


    def Get_module(self, moduleid: int) -> tuple:
        """Return module according to module index"""

        self.__cursor.execute("SELECT * FROM modules WHERE moduleid = ?", (moduleid,))
        module = self.__cursor.fetchall()
        self.__connection.commit()

        return module


    def Get_all_modules(self) -> list:
        """Return all modules of database"""

        self.__cursor.execute("SELECT * FROM modules")
        modules = self.__cursor.fetchall()
        self.__connection.commit()

        return modules


    def Get_word(self, wordid: int) -> tuple:
        """Get word from database according to id"""

        self.__cursor.execute("SELECT * FROM words WHERE wordid = ?", (wordid,))
        word = self.__cursor.fetchall()
        self.__connection.commit()

        return word


    def Show_modules(self):
        """Display all modules in database"""

        print("======== MODULES ========")
        self.__cursor.execute("SELECT * FROM modules;")
        modules = self.__cursor.fetchall()
        print(modules)


    def Show_words(self):
        """Display all words in database"""

        print("======== WORDS ========")
        self.__cursor.execute("SELECT * FROM words;")
        words = self.__cursor.fetchall()
        print(words)



























