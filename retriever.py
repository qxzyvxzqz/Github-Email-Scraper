import requests
from bs4 import BeautifulSoup
import random


def retrieve_email():
    global x, c
    username_file_path = input("Username File Path: ")
    output_file_path = input("Output File Path: ")
    usernames = open(username_file_path).read().strip().split()
    commits = []
    for username in usernames:
        try:
            r = requests.get('https://github.com/' + username + '?tab=repositories')
            bs = BeautifulSoup(r.content, features='html.parser')
            for link in bs.findAll('a', itemprop='name codeRepository'):
                x = link.get('href')
            r2 = requests.get('https://github.com' + x + '/commits?author=' + username)
            bs = BeautifulSoup(r2.content, features='html.parser')
            for links in bs.findAll('a', class_='Link--primary text-bold js-navigation-open markdown-title'):
                c = links.get('href')
                commits.append(c)
            y = random.choice(commits)
            r3 = requests.get('https://github.com' + y + '.patch').text
            if 'From:' in r3:
                print('@' + username, r3[r3.find('<') + 1:r3.find('>')])
                print('@' + username, r3[r3.find('<') + 1:r3.find('>')], file=open(output_file_path, 'a'))
        except Exception as e:
            print(f"[-] {e}")
            pass


if __name__ == "__main__":
    retrieve_email()
