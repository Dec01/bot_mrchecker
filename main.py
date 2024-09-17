import json

import requests
from selenium.webdriver.common.by import By
from selenium import webdriver


hahaha = ""
authors_list = ['User_1', 'User_2', 'User_3', 'User_4']
lables_list = ['tech', 'feature', 'core']
mr_dict = {
    'User_1': {},
    'User_2': {},
    'User_3': {},
    'User_4': {}
}
authors_task = []
gitlab_url = "https://git.site.ru"

option = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=option)
driver.get('https://git.site.ru/site')
search_username = driver.find_element(By.ID, "username")
search_password = driver.find_element(By.ID, "password")
search_button_div = driver.find_element(By.CLASS_NAME, "submit-container")
search_button = search_button_div.find_element(By.CLASS_NAME, "gl-button")
search_username.send_keys('username')
search_password.send_keys('password')
search_button.click()
driver.get('https://git.site.ru/groups/site/-/merge_requests')


def update_dict(mr_author, mr_task, mr_link, mr_label, mr_likes, mr_comments):
    text = mr_task
    task_name = ''
    word = 'TASK-'
    text = text.split()
    for i in text:
        if word in i:
            task_name = i
    if mr_author in mr_dict:
        if task_name in mr_dict[mr_author]:
            if mr_link in mr_dict[mr_author][task_name]:
                del mr_dict[mr_author][task_name][mr_link]['type:']
                del mr_dict[mr_author][task_name][mr_link]['likes:']
                del mr_dict[mr_author][task_name][mr_link]['comments:']
                mr_dict[mr_author][task_name][mr_link]['type:'] = mr_label
                mr_dict[mr_author][task_name][mr_link]['likes:'] = mr_likes
                mr_dict[mr_author][task_name][mr_link]['comments:'] = mr_comments
            else:
                mr_dict[mr_author][task_name][mr_link] = {}
                mr_dict[mr_author][task_name][mr_link]['type:'] = mr_label
                mr_dict[mr_author][task_name][mr_link]['likes:'] = mr_likes
                mr_dict[mr_author][task_name][mr_link]['comments:'] = mr_comments
        else:
            mr_dict[mr_author][task_name] = {}
            mr_dict[mr_author][task_name][mr_link] = {}
            mr_dict[mr_author][task_name][mr_link]['type:'] = mr_label
            mr_dict[mr_author][task_name][mr_link]['likes:'] = mr_likes
            mr_dict[mr_author][task_name][mr_link]['comments:'] = mr_comments
    else:
        pass

    pass

def status_mr_func(test, mr):
    test2 = dict(test)
    test3 = list(test2.items())
    if (test3[0][1] == "tech") and (test3[1][1] == "1" or test3[1][1] == "2" or test3[1][1] == "3"):
        if test3[2][1] == "0":
            return ":test_tube: Готово к тесту"
        else:
            return status_comment_func(mr)
    elif (test3[0][1] == "feature") and (test3[1][1] == "2" or test3[1][1] == "3"):
        if test3[2][1] == "0":
            return ":test_tube: Готово к тесту"
        else:
            return status_comment_func(mr)
    elif (test3[0][1] == "core") and (test3[1][1] == "2" or test3[1][1] == "3"):
        if test3[2][1] == "0":
            return ":test_tube: Готово к тесту"
        else:
            return status_comment_func(mr)
    elif test3[0][1] == "None":
        return ":o: Нет лейбла!"
    elif test3[1][1] == "None":
        return ":o: Не хватает лайков!"
    else:
        return ":o: Не хватает лайков!"



def status_jira_func(jira_status):
    option = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=option)
    driver.get(jira_status)
    try:
        search_username = driver.find_element(By.ID, "login-form-username")
        search_password = driver.find_element(By.ID, "login-form-password")
        search_button = driver.find_element(By.ID, "login-form-submit")
        search_username.send_keys('username')
        search_password.send_keys('username')
        search_button.click()
    except:
        pass
    driver.get(jira_status)
    try:
        status_jira = driver.find_element(By.ID, "status-val").text
        if status_jira == "НА РЕВЬЮ(BACKEND)":
            status_jira += " :vovka:"
        if status_jira == "В РАБОТЕ(BACKEND)":
            status_jira += " :deployparrot:"
        if status_jira == "ГОТОВО":
            status_jira += " :vanga:"
        if status_jira == "ГОТОВО К ПЕРЕНОСУ(BACKEND)":
            status_jira += " :vanga:"
        if status_jira == "ГОТОВО К ТЕСТУ(BACKEND)":
            status_jira += " :test_tube:"
        if status_jira == "ТЕСТИРОВАНИЕ(BACKEND)":
            status_jira += " :test_tube:"
    except:
        status_jira = 'None'
        pass
    return status_jira

def status_comment_func(test):
    option = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=option)
    driver.get(test)
    try:
        search_username = driver.find_element(By.ID, "username")
        search_password = driver.find_element(By.ID, "password")
        search_button_div = driver.find_element(By.CLASS_NAME, "submit-container")
        search_button = search_button_div.find_element(By.CLASS_NAME, "gl-button")
        search_username.send_keys('username')
        search_password.send_keys('username')
        search_button.click()
    except:
        pass
    driver.get(test)
    print("url: ", test)
    zzz = driver.find_element(By.CLASS_NAME, 'merge-request-tabs-container')
    status_comment = zzz.find_elements(By.TAG_NAME, 'div')
    print("status_comment: ", status_comment)
    try:
        for div in status_comment:
            print("tag_text: ", div.text)
            print("tag_attribute: ", div.get_attribute('class'))
            if div.get_attribute('class') == "d-flex flex-wrap align-items-center justify-content-lg-end":
                test444 = div.find_element(By.CLASS_NAME, "gl-display-flex discussions-counter").text
                print("ИТОГ: ", test444)
                sssss = ":test_tube: Готово к тесту"
                return sssss
            else:
                pass
    except:
        sssss = ":o: Есть незакрытые вопросы"
        return sssss


def send_slack():

    webhook_url = 'url'
    user1_issiu = mr_dict["User_1"].keys()
    user2_issiu = mr_dict["User_2"].keys()
    user3_issiu = mr_dict["User_3"].keys()
    user4_issiu = mr_dict["User_4"].keys()
    slack_data = {"text": ""}
    slack_data["text"] += f"\n#################################################################################\n"
    slack_data["text"] += f"\n*User_1* - активных задач: {len(user1_issiu)}\n\n"
    for key in user1_issiu:
        jira_status = f'https://jira.site.ru/browse/{key}'
        status = status_jira_func(jira_status)
        slack_data["text"] += f"\n> <https://jira.site.ru/browse/{key}|{key}> | {status}"
        for mr in mr_dict["User_1"][key]:
            ready_mr = mr_dict['User_1'][key][mr]
            slack_data["text"] += f"\n*mr*: {mr} - {status_mr_func(ready_mr, mr)}\n"
            for status_mr in mr_dict["User_1"][key][mr]:
                slack_data["text"] += f"• {status_mr} {mr_dict['User_1'][key][mr][status_mr]}\n"

    slack_data["text"] += f"\n"
    slack_data["text"] += f"\n#################################################################################\n"
    slack_data["text"] += f"\n*User_2* - активных задач: {len(user2_issiu)}\n\n"
    for key in user2_issiu:
        test_jira = f'https://jira.site.ru/browse/{key}'
        status = status_jira_func(test_jira)
        slack_data["text"] += f"\n> <https://jira.site.ru/browse/{key}|{key}> | {status}"
        for mr in mr_dict["User_2"][key]:
            ready_mr = mr_dict['User_2'][key][mr]
            slack_data["text"] += f"\n*mr*: {mr} - {status_mr_func(ready_mr, mr)} \n"
            for status_mr in mr_dict["User_2"][key][mr]:
                slack_data["text"] += f"• {status_mr} {mr_dict['User_2'][key][mr][status_mr]}\n"
    slack_data["text"] += f"\n"
    slack_data["text"] += f"\n#################################################################################\n"
    slack_data["text"] += f"\n*User_3* - активных задач: {len(user3_issiu)}\n\n"
    for key in user3_issiu:
        test_jira = f'https://jira.site.ru/browse/{key}'
        status = status_jira_func(test_jira)
        slack_data["text"] += f"\n> <https://jira.site.ru/browse/{key}|{key}> | {status}"
        for mr in mr_dict["User_3"][key]:
            ready_mr = mr_dict['User_3'][key][mr]
            slack_data["text"] += f"\n*mr*: {mr} - {status_mr_func(ready_mr, mr)}\n"
            for status_mr in mr_dict["User_3"][key][mr]:
                slack_data["text"] += f"• {status_mr} {mr_dict['User_3'][key][mr][status_mr]}\n"
    slack_data["text"] += f"\n"
    slack_data["text"] += f"\n#################################################################################\n"
    slack_data["text"] += f"\n*User_4* - активных задач: {len(user4_issiu)}\n\n"

    for key in user4_issiu:
        test_jira = f'https://jira.site.ru/browse/{key}'
        status = status_jira_func(test_jira)
        slack_data["text"] += f"\n> <https://jira.site.ru/browse/{key}|{key}> | {status}"
        for mr in mr_dict["User_4"][key]:
            ready_mr = mr_dict['User_4'][key][mr]
            slack_data["text"] += f"\n*mr*: {mr} - {status_mr_func(ready_mr, mr)}\n"
            for status_mr in mr_dict["User_4"][key][mr]:
                slack_data["text"] += f"• {status_mr} {mr_dict['User_4'][key][mr][status_mr]}\n"
    slack_data["text"] += f"\n"

    response = requests.post(
        webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

driver.implicitly_wait(0.4)
while True:
    search_mr = driver.find_elements(By.CLASS_NAME, "merge-request")
    search_pagination = driver.find_element(By.CLASS_NAME, "pagination")
    search_pagination_button = search_pagination.find_element(By.LINK_TEXT, "Next")
    for item in search_mr:
        mr_author = item.find_element(By.CLASS_NAME, "author-link").text
        if mr_author in authors_list:
            try: mr_link = item.find_element(By.CLASS_NAME, 'js-prefetch-document').get_attribute("href")
            except:
                mr_link = 'None'
                pass
            try: mr_task = item.find_element(By.CLASS_NAME, 'js-prefetch-document').text
            except:
                mr_task = 'None'
                pass
            try: mr_label = item.find_element(By.CLASS_NAME, 'gl-label').text
            except:
                mr_label = 'None'
                pass
            try: mr_likes = item.find_element(By.CLASS_NAME, 'issuable-upvotes').text
            except:
                mr_likes = 'None'
                pass
            try: mr_comments = item.find_element(By.CLASS_NAME, 'issuable-comments').text
            except:
                mr_comments = 'None'
                pass
            update_dict(mr_author, mr_task, mr_link, mr_label, mr_likes, mr_comments)
        else: pass
    try:
        search_pagination_button.click()
    except:
        send_slack()
        break
