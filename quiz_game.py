import json
import os

from quiz import Quiz


class QuizGame:
    STATE_FILE = "state.json"

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_total = 0
        self.load_data()

    def get_default_quizzes(self):
        return [
            Quiz(
                "Python에서 문자열을 저장할 때 사용하는 자료형은?",
                ["int", "str", "bool", "list"],
                2
            ),
            Quiz(
                "조건에 따라 다른 동작을 수행할 때 사용하는 문법은?",
                ["for", "while", "if", "def"],
                3
            ),
            Quiz(
                "반복문 중 횟수가 정해진 경우 자주 사용하는 것은?",
                ["for", "class", "try", "import"],
                1
            ),
            Quiz(
                "함수를 정의할 때 사용하는 키워드는?",
                ["return", "def", "input", "print"],
                2
            ),
            Quiz(
                "리스트를 나타내는 기호는?",
                ["()", "{}", "[]", "<>"],
                3
            )
        ]

    def show_menu(self):
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def read_text(self, prompt):
        while True:
            try:
                value = input(prompt).strip()

                if value == "":
                    print("⚠️ 빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                    continue

                return value

            except KeyboardInterrupt:
                self.safe_exit("\n⚠️ Ctrl+C가 입력되었습니다. 저장 후 종료합니다.")
            except EOFError:
                self.safe_exit("\n⚠️ 입력이 종료되었습니다. 저장 후 종료합니다.")

    def read_int(self, prompt, min_value, max_value):
        while True:
            text = self.read_text(prompt)

            try:
                number = int(text)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if number < min_value or number > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def play_quiz(self):
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다.")
            return

        total = len(self.quizzes)
        correct_count = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for index, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            quiz.display(index)
            print()

            user_answer = self.read_int("정답 입력 (1-4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번입니다.")

        score_percent = int((correct_count / total) * 100)

        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score_percent}점)")
        print("=" * 40)

        if self.best_score is None or correct_count > self.best_score:
            self.best_score = correct_count
            self.best_total = total
            self.save_data()
            print("🎉 새로운 최고 점수입니다!")
        else:
            print("🙂 최고 점수는 갱신되지 않았습니다.")

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = self.read_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.read_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.read_int("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_data()

        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if not self.quizzes:
            print("\n📭 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

        print("-" * 40)

    def show_best_score(self):
        if self.best_score is None:
            print("\n📌 아직 퀴즈를 풀지 않았습니다.")
            return

        score_percent = 0
        if self.best_total > 0:
            score_percent = int((self.best_score / self.best_total) * 100)

        print("\n🏆 최고 점수")
        print(f"- {score_percent}점 ({self.best_total}문제 중 {self.best_score}문제 정답)")

    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total
        }

        try:
            with open(self.STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다.")

    def load_data(self):
        if not os.path.exists(self.STATE_FILE):
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_total = 0
            self.save_data()
            print("📂 state.json 파일이 없어 기본 퀴즈로 시작합니다.")
            return

        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            quiz_data_list = data.get("quizzes", [])
            loaded_quizzes = []

            if not isinstance(quiz_data_list, list):
                raise ValueError("quizzes 형식 오류")

            for item in quiz_data_list:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str):
                    raise ValueError("question 형식 오류")
                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("choices 형식 오류")
                if not isinstance(answer, int) or not (1 <= answer <= 4):
                    raise ValueError("answer 형식 오류")

                loaded_quizzes.append(Quiz(question, choices, answer))

            self.quizzes = loaded_quizzes if loaded_quizzes else self.get_default_quizzes()
            self.best_score = data.get("best_score")
            self.best_total = data.get("best_total", 0)

            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")

        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("⚠️ 데이터 파일이 없거나 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_total = 0
            self.save_data()

    def safe_exit(self, message):
        print(message)
        self.save_data()
        raise SystemExit

    def run(self):
        while True:
            self.show_menu()
            choice = self.read_int("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                print("프로그램을 종료합니다.")
                self.save_data()
                break