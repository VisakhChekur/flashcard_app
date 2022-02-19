from tkinter import *
import pandas as pd
import random
# from btn_functions import ButtonFunctions


# ----------------------------- CONSTANTS AND DATA ------------------- #
BACKGROUND_COLOR = "#B1DDC6"
language_font = ("Arial", 40, 'italic')
word_font = ("Arial", 60, "bold")
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=30, pady=30)
# ----------------------------- BUTTON FUNCTIONS --------------------- #


class ButtonFunctions():

    def __init__(self):
        self.all_words_df = pd.read_csv("data/french_words.csv")
        self.all_words = {row.French: row.English for i,
                          row in self.all_words_df.iterrows()}

        self.testing_words_df = pd.read_csv("data/words_to_test.csv")
        self.testing_words_list = self.testing_words_df["French"].tolist()
        self.testing_words_dict = {
            word: self.all_words[word] for word in self.testing_words_list}
        self.language = "French"
        self.french_word = random.choice(self.testing_words_list)
        self.english_word = self.testing_words_dict[self.french_word]
        self.front_img = PhotoImage(file="images/card_front_2.png")
        self.back_img = PhotoImage(file="images/card_back_2.png")

    def flip_card(self):
        self.language = canvas.itemcget(language_text, "text")
        if self.language == "English":
            self.language = "French"
            canvas.itemconfig(word_text, text=self.french_word)
            canvas.itemconfig(current_image, image=self.front_img)
        else:
            self.language = "English"
            canvas.itemconfig(word_text, text=self.english_word)
            canvas.itemconfig(current_image, image=self.back_img)
        canvas.itemconfig(language_text, text=self.language)

    # TODO: 7. create correct() function
    def correct(self):
        del self.testing_words_dict[self.french_word]
        if self.testing_words_dict:
            self.french_word = random.choice(
                list(self.testing_words_dict.keys()))
            self.english_word = self.testing_words_dict[self.french_word]
            self.language = "French"
            canvas.itemconfig(current_image, image=self.front_img)
            canvas.itemconfig(language_text, text=self.language)
            canvas.itemconfig(word_text, text=self.french_word)
            cards_left_label.config(
                text=f"Number of cards left = {len(self.testing_words_dict)}")
        else:
            canvas.itemconfig(
                language_text, text="You finished the deck.\nRepopulating the deck.")
            canvas.itemconfig(word_text, text="")
            window.after(3000, btn_fun.repopulate_deck)

    # TODO: 8. create wrong() function
    def wrong(self):
        self.french_word = random.choice(list(self.testing_words_dict.keys()))
        self.english_word = self.testing_words_dict[self.french_word]
        self.language = "French"
        canvas.itemconfig(current_image, image=self.front_img)
        canvas.itemconfig(language_text, text=self.language)
        canvas.itemconfig(word_text, text=self.french_word)

    def save(self):
        self.testing_words_list = list(self.testing_words_dict.keys())
        self.testing_words_dict = {'French': self.testing_words_list}
        self.testing_words_df = pd.DataFrame.from_dict(self.testing_words_dict)
        self.testing_words_df.to_csv("data/words_to_test.csv")
        canvas.itemconfig(language_text, text="Saved successfully!")
        canvas.itemconfig(word_text, text="Save Progress")
        window.after(2000, btn_fun.display_save)

    def display_save(self):
        canvas.itemconfig(language_text, text=self.language)
        if self.language == "French":
            canvas.itemconfig(word_text, text=self.french_word)
        else:
            canvas.itemconfig(word_text, text=self.english_word)

    def repopulate_deck(self):
        self.all_words_df = pd.read_csv("data/french_words.csv")
        self.all_words = {row.French: row.English for i,
                          row in self.all_words_df.iterrows()}
        self.testing_words_dict = {
            f_word: e_word for f_word, e_word in self.all_words.items()}

        self.french_word = random.choice(list(self.testing_words_dict.keys()))
        self.english_word = self.testing_words_dict[self.french_word]
        self.language = "French"
        canvas.itemconfig(language_text, text=self.language)
        canvas.itemconfig(word_text, text=self.french_word)
        cards_left_label.config(
            text=f"Number of cards left = {len(self.testing_words_dict)}")

# ----------------------------- UI SETUP ----------------------------- #


btn_fun = ButtonFunctions()

# Label (no of cards left)
cards_left_label = Label(
    text=f"Number of cards left = {len(btn_fun.testing_words_dict)}")
cards_left_label.config(font=("Arial", 15, "italic"), bg=BACKGROUND_COLOR)
cards_left_label.grid(row=0, column=1, columnspan=2, sticky=E)

# Canvas
canvas = Canvas(height=400, width=608)
current_image = canvas.create_image(
    304, 200, image=btn_fun.front_img, anchor=CENTER)
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(row=1, column=0, columnspan=3)

# TODO: 4. Create Texts (language, word)
language_text = canvas.create_text(
    304, 100, text=btn_fun.language, font=language_font)
word_text = canvas.create_text(
    304, 260, text=btn_fun.french_word, font=word_font)
# TODO: 5. Create Buttons (correct, wrong, quit)

correct_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")
flip_img = PhotoImage(file="images/flip_1.png")
save_img = PhotoImage(file="images/save_correct.png")

correct_btn = Button(image=correct_img, command=btn_fun.correct)
correct_btn.grid(row=2, column=2)
correct_btn.config(highlightthickness=0, bd=0)

wrong_btn = Button(image=wrong_img, command=btn_fun.wrong)
wrong_btn.grid(row=2, column=0)
wrong_btn.config(highlightthickness=0, bd=0)

flip_btn = Button(image=flip_img, command=btn_fun.flip_card)
flip_btn.grid(row=2, column=1)
flip_btn.config(highlightthickness=0, bd=0, bg=BACKGROUND_COLOR,
                activebackground=BACKGROUND_COLOR)

save_btn = Button(image=save_img, command=btn_fun.save)
save_btn.grid(row=0, column=0)
save_btn.config(highlightthickness=0, bd=0, bg=BACKGROUND_COLOR,
                activebackground=BACKGROUND_COLOR)

window.mainloop()
