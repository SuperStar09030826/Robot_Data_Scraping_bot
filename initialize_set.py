import os
from data_preprocess import read_file_and_return_lines
from data_preprocess import save_list_to_txt

def check_file_exists(filename="initial.txt"):
    return os.path.isfile(filename)

def ask_questions():
    # Initialize a list to store answers
    answers = []

    questions = [
      "How many questions do you want to ask at once? (3~10)\n",
      "How many seconds later do you want to ask again? (20+ seconds)\n",
      "How many seconds(1hr = 3600s, 1 day = 86400s) later do you want to ask about next robot again? (100+ seconds)\n",
    ]

    if os.path.isfile("initial.txt"):
        list_answer = list(map(int, read_file_and_return_lines("initial.txt")))
        if len(list_answer) < 3:
          print("Not correct setting. Please set your options.")
        else:
          return list_answer
    else:
        print("There isn't previous setting. Please set your options.")
    
    for question in questions:
      answer = input(question)
      answers.append(answer)

    save_list_to_txt(answers, "initial.txt")
    return list(map(int, answers))

# Call the function to execute
if __name__ == "__main__":
  time_repeat, time_quest, time_robot = ask_questions()
  print("***************\n\n", time_repeat, time_quest, time_robot)