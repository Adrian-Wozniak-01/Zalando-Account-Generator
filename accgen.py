# TO DO
# Get emails from txt file
# Better error handling - create exceptions
# Create GUI

import random
import string
from colorama import Fore
from colorama import Style
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from os import system
from seleniumwire import webdriver
system("title "+'KryptoN#2137 Zalando Account Generator')


def slow_type(element, text, delay=0.1):
    for character in text:
        element.send_keys(character)
        time.sleep(delay)


global email_list
email_list = []

global proxy_list
proxy_list = []

proxies = open("proxy.txt", "r")
for x in proxies:
    item = x.split(":")
    proxy_host = item[0]
    proxy_port = item[1]
    proxy_login = item[2]
    proxy_password = item[3].rstrip('\n')

    proxy_list.append([proxy_host, proxy_port, proxy_login, proxy_password])


# Show proxy list
# print(proxy_list)


def work():

    email_min_lenght = int(input('Min email lenght: '))
    email_max_lenght = int(input('Max email lenght: '))
    domain = input('Input your domain: @')
    how_many = int(input('How many emails do you want: '))
    firstName = input('First name: ')
    lastName = input('Last name: ')

    def answer_1():
        global pass_choice, password_return, password_max_lenght, password_static_return
        answer = input('Static or random password s/r: ').lower()

        if answer == 's':
            pass_choice = 's'
            password_static_return = input('Input password: ')
        elif answer == 'r':
            pass_choice = 'r'
            password_max_lenght = int(input('Max password lenght: '))
        else:
            print(Fore.RED+'Wrong choice!'+Fore.WHITE)
            answer_1()

    answer_1()
    discord_webhook = input('Input webhook or leave blank: ')

    global i
    i = 0

    for _ in range(how_many):
        i_proxy_list = proxy_list[i]
        global driver
        PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--start-maximized")

        options = {
            'proxy': {
                'http': f'http://{i_proxy_list[2]}:{i_proxy_list[3]}@{i_proxy_list[0]}:{i_proxy_list[1]}',
                'https': f'http://{i_proxy_list[2]}:{i_proxy_list[3]}@{i_proxy_list[0]}:{i_proxy_list[1]}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }}
        driver = webdriver.Chrome(
            PATH, chrome_options=chrome_options, seleniumwire_options=options)

        # next time use new proxy
        i += 1
        email_number = random.randint(email_min_lenght, email_max_lenght)
        email = ''.join(random.choice(string.ascii_letters)
                        for x in range(email_number))
        email_return = email + '@'+domain
        email_list.append(email_return)

        if pass_choice == 'r':
            password_number = random.randint(6, password_max_lenght)
            password_return = ''.join(random.choice(
                string.ascii_letters) for x in range(password_number))
        else:
            password_return = password_static_return
        print(
            f'http://{i_proxy_list[2]}:{i_proxy_list[3]}@{i_proxy_list[0]}:{i_proxy_list[1]}')

        driver.get("https://www.zalando.pl/login/?view=register")
        start = time.time()

        register = WebDriverWait(driver, 3, 1).until(
            lambda d: d.find_element_by_xpath("/html/body/div[1]/div/section/div/div[2]/div/button/span"))
        register.click()
        # while True: pass

        first_name = WebDriverWait(driver, 3, 1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[1]/div/div/input"))
        first_name.clear()
        # first_name.send_keys(firstName)
        slow_type(first_name, firstName)

        last_name = WebDriverWait(driver, 3, 1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[2]/div/div/input"))
        last_name.clear()
        # last_name.send_keys(lastName)
        slow_type(last_name, lastName)

        email_address = WebDriverWait(driver, 3, 1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[3]/div/div/input"))
        email_address.clear()
        # email_address.send_keys(email_return)
        slow_type(email_address, email_return)

        password = WebDriverWait(driver, 3, 1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[4]/div[1]/div/input"))
        password.clear()
        # password.send_keys(password_return)
        slow_type(password, password_return)

        time.sleep(0.5)
        preferences = WebDriverWait(driver, 3, 0.1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[5]/div/div[2]/div/div[3]/div/label"))
        preferences.click()

        time.sleep(0.5)
        newsletter = WebDriverWait(driver, 3, 0.1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[6]/div/div/label"))
        newsletter.click()

        time.sleep(0.5)
        # Zarejestruj się
        register = WebDriverWait(driver, 3, 0.1).until(lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[7]/button"))
        register.click()
        time.sleep(4)

        end = time.time()
        creating_time = end - start
        creating_time = round(creating_time, 2)

        current_site_url = driver.current_url
        if discord_webhook != '':
            if current_site_url != 'https://www.zalando.pl/login/?view=register':
                date = datetime.now()
                currdate = "["+str(date.hour) + ':' + \
                    str(date.minute) + ':' + str(date.second) + "]"
                print(Fore.GREEN+currdate+'Account Created!'+Fore.WHITE)
                # with open('zalando_email_out.txt', 'a') as f:
                #    f.write(email_return + ':'+password_return+'\n')

                webhook = DiscordWebhook(discord_webhook)
                embed = DiscordEmbed(
                    title='Successful Register!', color='39C16C')
                embed.set_footer(text='KryptoN#2137 Zalando Account Generator')
                embed.set_timestamp()

                embed.add_embed_field(name='🌍Site', value='Zalando')
                embed.add_embed_field(
                    name='📧Email', value=str('||'+email_return+'||'))
                embed.add_embed_field(name='⏰Time', value=str(creating_time))
                webhook.add_embed(embed)
                response = webhook.execute()
            # else webhook, że nie udało się
            else:
                date = datetime.now()
                currdate = "["+str(date.hour) + ':' + \
                    str(date.minute) + ':' + str(date.second) + "]"
                print(Fore.RED+currdate+'Failed Register!'+Fore.WHITE)

                webhook = DiscordWebhook(discord_webhook)
                embed = DiscordEmbed(title='Failed Register!', color='FF0000')
                embed.set_footer(text='KryptoN#2137 Zalando Account Generator')
                embed.set_timestamp()

                embed.add_embed_field(name='🌍Site', value='Zalando')
                embed.add_embed_field(
                    name='📧Email', value=str('||'+email_return+'||'))
                embed.add_embed_field(name='⏰Time', value=str(creating_time))
                webhook.add_embed(embed)
                response = webhook.execute()
        driver.quit()


work()

# write to file
with open('zalando_email_out.txt', 'a') as f:
    for email in email_list:
        f.write(email+":"+password_static_return+'\n')

# Discord:
# KryptoN#2137
