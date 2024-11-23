import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from time import sleep
import time, csv, random, json

from data_preprocess import *
from initialize_set import ask_questions

time_repeat, time_quest, time_robot = ask_questions()

command = [
  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
  '--remote-debugging-port=1005',
  '--user-data-dir=C:\\chrome\\1005'
]
subprocess.Popen(command)

time.sleep(1)

chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:1005"
chrome_options.add_argument('--log-level=3')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


if __name__ == "__main__":
  
  input_url = 'https://chatgpt.com'
  # input_url = 'https://auth.openai.com/authorize?client_id=TdJIcbe16WoTHtN95nyywh5E4yOo6ItG&scope=openid%20email%20profile%20offline_access%20model.request%20model.read%20organization.read%20organization.write&response_type=code&redirect_uri=https%3A%2F%2Fchatgpt.com%2Fapi%2Fauth%2Fcallback%2Flogin-web&audience=https%3A%2F%2Fapi.openai.com%2Fv1&device_id=5b09da28-5618-4a34-b120-37504269c4f2&prompt=login&screen_hint=login&ext-oai-did=5b09da28-5618-4a34-b120-37504269c4f2&ext-login-allow-phone=true&country_code=US&state=MNUHp9hgh4clNWUqawHtnGe1ox-phMzNdQbQ6BWDDwE&code_challenge=qpKr1aVQn_DrDp7kcxOnpb_iXg584lFX-pFZCoQsVWc&code_challenge_method=S256'
  driver.get(input_url)
  sleep(1)
  
  try:
    button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search the web"]')
    button.click()
    print("Button with 'Search the web' clicked.")
  except NoSuchElementException:
    print("Button with 'Search the web' clicked.")

  robot_list = read_file_and_return_lines("robot list.txt")
  query_list = read_file_and_return_lines("query list.txt")
  query_list = clean_text_list(query_list, time_repeat)

  for robot_id, robot in enumerate(robot_list):
    robot_query = [robot] + query_list
    # file_buffer = []
    value_buffer = []
    query_buffer = []

    for query_id, query in enumerate(robot_query):
      textbox = driver.find_element(By.ID, 'prompt-textarea')

      if query_id == 0:
        # file_buffer.append(query)
        textbox.send_keys(query)
        textbox.send_keys(Keys.SHIFT, Keys.ENTER)
      elif query != ' ':
        # file_buffer.append(query + "\n" if query_id < 2 else " - " + query)
        query_buffer.append(query)
        textbox.send_keys('- ' + query)
        textbox.send_keys(Keys.SHIFT, Keys.ENTER)
      else:
        pass

      sleep(1)

      if query_id % time_repeat == 1:
        # btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="send-button"]')
        # btn.click()
        textbox.send_keys(Keys.ENTER)
        sleep(time_quest)

        answer = driver.find_elements(By.CLASS_NAME, 'markdown')[int(query_id/5)].text
        print(f'[ANSWER {int(query_id/5) + 1}]:\n{answer}')

        value_buffer.append({
          "query": query_buffer,
          "answer": answer
        })

        query_buffer = []

        sleep(10)
    
    save_list_to_txt(file_buffer, robot + '.txt')
    sleep(time_robot)
