#!/usr/bin/env python

from flask import Flask, render_template, request
import pandas as pd


class Words(object):
    """
    Register what words are correct and what words you got wrong.
    Also count the amount of correct and incorrect answers.
    """

    def __init__(self) -> None:
        self.word_df = pd.DataFrame()
        self.answered_words_df = pd.DataFrame()
        self.correct_answers = set()
        self.num_correct_answers = 0
        self.incorrecnt_answers = set()
        self.num_incorrect_answers = 0

    def increase_correct_score(self):
        self.num_correct_answers += 1

    def increase_incorrect_score(self):
        self.num_incorrect_answers += 1

    def add_correct_words(self, word):
        self.correct_answers.add(word)

    def add_incorrect_words(self, word):
        self.incorrecnt_answers.add(word)

    def create_answered_df(self):
        self.answered_words_df = self.word_df[""]

    def create_answered_df(self):
        self.answered_words_df = pd.DataFrame(
            0,
            index=range(self.word_df.shape[0]),
            columns=["Japanese", "Correct", "Incorrect", "count"],
        )
        self.answered_words_df["Japanese"] = self.word_df["Japanese"]

    def put_in_answered_df(self, word, is_correct):
        self.answered_words_df.loc[
            self.answered_words_df["Japanese"] == word, "count"
        ] += 1
        if is_correct:
            self.answered_words_df.loc[
                self.answered_words_df["Japanese"] == word, "Correct"
            ] += 1
        else:
            self.answered_words_df.loc[
                self.answered_words_df["Japanese"] == word, "Incorrect"
            ] += 1

    def get_random_word(self):
        return self.word_df.sample()["Japanese"].values[0]

    def check_answer(self, word, answer):
        correct_answer = self.word_df[self.word_df["Japanese"] == word]["Dutch"].values[
            0
        ]
        return correct_answer == answer, correct_answer

    def get_score(self):
        return {
            "correct": self.num_correct_answers,
            "incorrect": self.num_incorrect_answers,
        }


app = Flask(__name__)
score_keepers = Words()
score_keepers.word_df = pd.read_excel("data/Words.xlsx", "HFST. 1 words")
score_keepers.create_answered_df()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    global word
    is_correct = None
    correct_answer = None
    if request.method == "POST":
        answer = request.form["answer"]  # Get the answer submitted by the user
        # Validate the answer and provide feedback (you can customize this logic)
        is_correct, correct_answer = score_keepers.check_answer(word, answer)
        if is_correct:
            score_keepers.increase_correct_score()
        else:
            score_keepers.increase_incorrect_score()
        score_keepers.put_in_answered_df(word, is_correct)

    word = score_keepers.get_random_word()
    return render_template(
        "index.html",
        is_correct=is_correct,
        correct_answer=correct_answer,
        word=word,
        score=score_keepers.get_score(),
        answered_df=[
            score_keepers.answered_words_df.to_html(
                index=False, classes=["data", "sortable"], table_id="answered"
            )
        ],
    )


@app.route("/list", methods=["GET", "POST"])
def list_words():
    global word
    is_correct = None
    correct_answer = None
    if request.method == "POST":
        answer = request.form["answer"]  # Get the answer submitted by the user
        # Validate the answer and provide feedback (you can customize this logic)
        is_correct, correct_answer = score_keepers.check_answer(word, answer)
        if is_correct:
            score_keepers.increase_correct_score()
        else:
            score_keepers.increase_incorrect_score()
        score_keepers.put_in_answered_df(word, is_correct)

    word = score_keepers.get_random_word()
    return render_template(
        "list_words.html",
        is_correct=is_correct,
        correct_answer=correct_answer,
        word=word,
        score=score_keepers.get_score(),
        answered_df=[
            score_keepers.answered_words_df.to_html(
                index=False, classes=["data", "sortable"], table_id="answered"
            )
        ],
    )


if __name__ == "__main__":
    app.run(debug=True)
