class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number=None):
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }