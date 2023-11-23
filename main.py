from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file("sure.kv")
class LoginPage(Screen):
    def show_call_instructor_popup(self):
        popup = Popup(
            title='       Call Mrs Okudo for assistance        ',
            content=Label(text="+234 703 344 2471"),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
class HomePage(Screen):
    def start_quiz(self):
        self.manager.current = "quiz"

    def reset_inputs(self):
        pass

    def logout(self):
        login_page = self.manager.get_screen("login")
        password_input = login_page.ids.passw

        # Reset the text in the password TextInput widget
        password_input.text = ""

        self.manager.current = "login"

    def start_quiz2(self):
        quiz_screen2 = self.manager.get_screen("quiz2")
        quiz_screen2.current_question = 0
        quiz_screen2.score = 0
        quiz_screen2.load_question()
        quiz_screen2.clear_buttons()
        self.manager.current = "quiz2"
class ResultScreen(Screen):
    pass

class ResultScreen2(Screen):
    pass
class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginPage())
        sm.add_widget(HomePage())
        sm.add_widget(ResultScreen())
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(QuizScreen2(name="quiz2"))

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"

        sm.current = "login"

        return sm

    def reset_quiz_and_go_home(self):
        screen_manager = self.root
        quiz_screen = screen_manager.get_screen("quiz")
        home_screen = screen_manager.get_screen("home")

        quiz_screen.reset_quiz_state()
        screen_manager.transition.direction = "right"
        home_screen.manager.current = "home"

    def set_username(self, username):
        self.username = username
class QuizScreen(Screen):
    current_question = 0
    score = 0

    questions = [
        {"question": "1. The number that comes\n before 1000 is?",
         "options": ["999", "199", "099"], "correct_answer": 0},
        {"question": "2. Three thousand and seventy can be\n written as.", "options": ["30076", "300076", "3070",],
         "correct_answer": 2},
        {"question": "3. in 4928, 2 stands for ......",
         "options": ["units", "thousand", "tens"], "correct_answer": 2},
        {"question": "4. Find the total of 124 and 35",
         "options": ["159", "179", "158"], "correct_answer": 0},
        {"question": "5. what is the next segment?\n 10, 15, 20, 25.",
         "options": ["40", "35", "30"], "correct_answer": 2},
        {"question": "6. What is the missing number\n109 --- 111?",
         "options": ["171", "110", "101"], "correct_answer": 1},
        {"question": "7. When the long hand of a clock \nis pointing at 12 and the short hand\n at 9, it is what time?",
         "options": ["12 O'clock", "7 O'clock ", "9 O'clock"],
         "correct_answer": 2},
        {"question": "8. There are ........ calender months",
         "options": ["12", "13", "14",], "correct_answer": 0},
        {"question": "9. A millenium is how many years?",
         "options": ["100", "1000", "10"], "correct_answer": 1},
        {"question": "10. PM means........",
         "options": ["medium", "meridian", "marvel"], "correct_answer": 1},
        {"question": "11. There are ..... days in a week.",
         "options": ["9", "6", "7"],
         "correct_answer": 2},
        {
            "question": "12. One of the properties of a triangle\n is that it is round in shape.",
            "options": ["True", "False"], "correct_answer": 1},
        {
            "question": "13. A square has four equal sizes",
            "options": ["True", "False", "", ""],
            "correct_answer": 0},
        {"question": "14. A rectangle has four equal sides",
         "options": ["True", "False",]
        , "correct_answer": 1},
        {"question": "15. 'How many days are in a leap year?",
         "options": ["355", "366",
                     "365"], "correct_answer": 1},
        {"question": " 16. 604 oranges plus 207 bananas.\n How many fruit are there altogether?",
         "options": ["613", "811", "608"], "correct_answer": 1},
        {"question": "17. Take 39 erasers from\n50 erasers in a box.\n how many will be left?", "options": ["10", "12", "11"],
         "correct_answer": 2},
        {"question": "18. 21 x 3 = ?.", "options": ["65", "64", "63"],
         "correct_answer": 2},
        {"question": "19. Divide 24 by 6.",
         "options": ["4", "3", "5"], "correct_answer": 0},
        {"question": "20. The number that comes after 150.",
         "options": ["151", "149", "148"], "correct_answer": 0},
    ]
    def on_pre_enter(self):
        self.load_question()
    def load_question(self):
        question = self.questions[self.current_question]
        self.ids.question_label.text = question["question"]
        for i, option in enumerate(question["options"]):
            self.ids[f'option_{i + 1}'].text = option

    def check_answer(self, selected_option):
        correct_answer = self.questions[self.current_question]["correct_answer"]

        if selected_option == correct_answer:
            self.ids[f'option_{selected_option + 1}'].background_color = (0, 1, 0, 1)  # Green for correct
            self.score += 1
        else:
            self.ids[f'option_{selected_option + 1}'].background_color = (1, 0, 0, 1)  # Red for incorrect

        # Disable buttons after an option is selected
        for i in range(4):
            self.ids[f'option_{i + 1}'].disabled = False

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.load_question()
            self.clear_buttons()
        else:
            self.manager.transition.direction = "up"  # Set transition direction
            self.show_result()
    def clear_buttons(self):
        for i in range(4):
            self.ids[f'option_{i + 1}'].background_color = (1, 1, 1, 1)  # Reset button color
            self.ids[f'option_{i + 1}'].disabled = False
    def show_result(self):
        result_label = self.manager.get_screen("result_screen").ids.result_label
        result_label.text = f"Result: {self.score}/20"
        self.manager.current = "result_screen"
    def reset_quiz_state(self):
        self.current_question = 0
        self.score = 0
        self.load_question()
        self.clear_buttons()

class QuizScreen2(Screen):
    current_question = 0
    score = 0

    questions = [
        {
            "question": "1. I have  _____ Uncle",
            "options": ["a", "an", "the", ""], "correct_answer": 1},
        {"question": "2. There ______ pencils is in my bag.",
         "options": ["were", "is", "it", ""], "correct_answer": 0},
        {"question": "3. He kept ____ water in his bottle.",
         "options": ["an", "a", "some", ""], "correct_answer": 2},
        {"question": "4. Which spelling is correct", "options": ["bule", "blue", "buel", ""],
         "correct_answer": 1},
        {"question": "5. Which spelling is correct",
         "options": ["borken", "brokne", "broken", ""], "correct_answer": 2},
        {
            "question": "6. The plural of brush is ____",
            "options": ["bushes", "brushs", "brushes", ""], "correct_answer": 2},
        {"question": "7. The plural of sheep is ____",
         "options": ["sheeps", "sheepes", "sheep", ""], "correct_answer": 2},
        {"question": "8. Mary ____ a beautiful toy.", "options": ["but", "buy", "brought", ""],
         "correct_answer": 2},
        {"question": "9. My mother ____ my breakfast this morning.",
         "options": ["cooked", "cook", "cooking", ""], "correct_answer": 0},
        {"question": "10. She _____ a big house",
         "options": ["builted", "built", "build", ""], "correct_answer": 1}]

    def on_pre_enter(self):
        self.load_question()

    def load_question(self):
        question = self.questions[self.current_question]
        self.ids.question_label.text = question["question"]
        for i, option in enumerate(question["options"]):
            self.ids[f'option_{i + 1}'].text = option

    def check_answer(self, selected_option):
        correct_answer = self.questions[self.current_question]["correct_answer"]

        if selected_option == correct_answer:
            self.ids[f'option_{selected_option + 1}'].background_color = (0, 1, 0, 1)  # Green for correct
            self.score += 1
        else:
            self.ids[f'option_{selected_option + 1}'].background_color = (1, 0, 0, 1)  # Red for incorrect

        # Disable buttons after an option is selected
        for i in range(4):
            self.ids[f'option_{i + 1}'].disabled = False

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.load_question()
            self.clear_buttons()
        else:
            self.manager.transition.direction = "up"  # Set transition direction
            self.show_result()
    def clear_buttons(self):
        for i in range(4):
            self.ids[f'option_{i + 1}'].background_color = (1, 1, 1, 1)  # Reset button color
            self.ids[f'option_{i + 1}'].disabled = False
    def show_result(self):
        result_label = self.manager.get_screen("result_screen").ids.result_label
        result_label.text = f"Result: {self.score}/10"
        self.manager.current = "result_screen"
    def reset_quiz_state(self):
        self.current_question = 0
        self.score = 0
        self.load_question()
        self.clear_buttons()
    def try_again(self):
        self.reset_quiz_state()
        self.manager.current = "home"

if __name__ == '__main__':
    MainApp().run()