class Question:
    def __init__(self, text, options):
        self.text = text                
        self.options = options          
        self.votes = {option: 0 for option in options}

    def vote(self, option_index):
        if 0 <= option_index < len(self.options):
            option = self.options[option_index]
            self.votes[option] += 1
            return True
        return False

    def get_results(self):
        return self.votes.copy()

    def total_votes(self):
        return sum(self.votes.values())

    def winner(self):
        if not self.votes:
            return None
        max_votes = max(self.votes.values())
        leaders = [opt for opt, cnt in self.votes.items() if cnt == max_votes]
        return leaders[0] if len(leaders) == 1 else None
            
class Participant:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.voted_questions = []

    def has_voted_in(self, question_id):
        return question_id in self.voted_questions
        
    def add_voted_question(self, question_id):
        self.voted_questions.append(question_id)
        
class Poll:
    def __init__(self):
        self.questions = []
        self.participants = []
        self.next_question_id = 0
        
    def add_question(self, question):
        self.questions.append(question)

    def add_participant(self, participant):
        self.participants.append(participant)
    
    def find_participant_by_email(self, email):
        for p in self.participants:
            if p.email == email:
                return p
        return None
        
    def find_question_by_index(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
        
    def cast_vote(self, participant_email: str, question_index: int, option_index: int) -> str:
        participant = self.find_participant_by_email(participant_email)
        if participant is None:
            return "Участник не найден"

        question = self.find_question_by_index(question_index)
        if question is None:
            return "Вопрос не найден"

        if participant.has_voted_in(question_index):
            return "Участник уже голосовал в этом вопросе"

        success = question.vote(option_index)
        if not success:
            return "Неверный вариант ответа"

        participant.add_voted_question(question_index)
        return "Голос принят"

    def get_question_statistics(self, question_index: int) -> str:
        question = self.find_question_by_index(question_index)
        if question is None:
            return "Вопрос не найден"

        results = question.get_results()
        total = question.total_votes()
        winner = question.winner()

        lines = [f"Вопрос: {question.text}"]
        for option, count in results.items():
            vote_word = "голос" if count == 1 else "голоса" if 2 <= count <= 4 else "голосов"
            lines.append(f"{option}: {count} {vote_word}")
        lines.append(f"Всего голосов: {total}")
        lines.append(f"Победитель: {winner if winner else 'Нет однозначного победителя'}")

        return "\n".join(lines)
        
        
# Создаём опросник
poll = Poll()

# Добавляем вопрос
q1 = Question("Какой цвет вам нравится?", ["Красный", "Синий", "Зелёный"])
poll.add_question(q1)

# Добавляем участников
alice = Participant("Алиса", "alice@mail.ru")
bob = Participant("Боб", "bob@mail.ru")
poll.add_participant(alice)
poll.add_participant(bob)

# Голосование
print(poll.cast_vote("alice@mail.ru", 0, 0))   # Алиса голосует за Красный
print(poll.cast_vote("bob@mail.ru", 0, 1))     # Боб за Синий
print(poll.cast_vote("alice@mail.ru", 0, 0))   # повторная попытка — ошибка

# Статистика
print(poll.get_question_statistics(0))        
        

# Тест 1: создание вопроса и подсчёт голосов
q = Question("Тест?", ["A", "B"])
q.vote(0)
q.vote(0)
q.vote(1)
assert q.total_votes() == 3
assert q.winner() == "A"
assert q.get_results() == {"A": 2, "B": 1}
print("Тест 1 пройден")

# Тест 2: некорректное голосование
q2 = Question("Опрос", ["Да", "Нет"])
assert q2.vote(2) == False   # неверный индекс
assert q2.total_votes() == 0
print("Тест 2 пройден")

# Тест 3: участник не может голосовать дважды
poll = Poll()
q3 = Question("Вопрос", ["1", "2"])
poll.add_question(q3)
user = Participant("Иван", "ivan@ya.ru")
poll.add_participant(user)
res1 = poll.cast_vote("ivan@ya.ru", 0, 0)
res2 = poll.cast_vote("ivan@ya.ru", 0, 1)
assert res1 == "Голос принят"
assert "уже голосовал" in res2.lower()
print("Тест 3 пройден")

# Тест 4: поиск победителя при ничьей
q4 = Question("Ничья", ["X", "Y"])
q4.vote(0)
q4.vote(1)
assert q4.winner() is None
print("Тест 4 пройден")