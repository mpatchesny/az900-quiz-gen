import sys
import random

if __name__ == "__main__":
    path = sys.argv[1]
    random_questions = False
    if len(sys.argv) == 3:
        random_questions = bool(sys.argv[2])

    with open(path, "r", encoding="utf-8") as f:
        content = f.readlines()

    all_questions = []
    for i in range(0, len(content)):
        if content[i].startswith("###"):
            question = content[i][4:-1]
            answers = []
            good_answers = []

            i += 2
            while content[i].startswith("- "):
                answers.append(content[i])
                if answers[-1].startswith("- [x]"):
                    good_answers.append(answers[-1])
                i += 1

            answers = [ x[5:-1] for x in answers ]
            good_answers = [ x[5:-1] for x in good_answers ]
            all_questions.append({"question": question, "answers": answers, "good_answers": good_answers})

    questions_answered = []
    ok_answers_count = 0
    question_no = 0

    while True:
        if random_questions:
            not_answered_questions = [ x for x in all_questions if x not in questions_answered ]
            question = random.choice(not_answered_questions)
            if len(not_answered_questions) == 0:
                print("All quesiton answered!")
                break
        else:
            if question_no >= len(all_questions):
                print("All quesiton answered!")
                break
            question = all_questions[question_no]

        single_multiple_choice = "[single choice]" if len(question["good_answers"]) == 1 else "[multiple choice]"
        summary = f"[{ok_answers_count} OK, {question_no-ok_answers_count} BAD]"

        print("")
        print(f"{question_no+1}/{len(all_questions)}", summary, single_multiple_choice, question["question"], "[q to exit]")
        for i in range(0, len(question["answers"])):
            print(f"{i+1}." + question["answers"][i])

        user_answer = input("Answer: ")
        if user_answer == "q": 
            break

        user_answers_num = str(user_answer).split(",")
        user_answers_num = [int(x)-1 for x in [x.strip() for x in user_answers_num] if x.isdigit()]
        user_answers = []
        for num in user_answers_num:
            if num < len(question["answers"]):
                user_answers.append(question["answers"][num])

        bad_answer = False
        for answer in user_answers:
            if not answer in question["good_answers"]:
                bad_answer = True
                break
        
        if not bad_answer:
            print("Correct")
            ok_answers_count += 1
        else:
            print("Wrong! Proper answer(s): " + ", ".join(question["good_answers"]))

        questions_answered.append(question)
        question_no += 1

    print(f"{len(questions_answered)} questions answered, {ok_answers_count} answers correct, {len(questions_answered) - ok_answers_count} answers wrong")