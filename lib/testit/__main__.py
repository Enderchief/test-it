import os
from os import path
from importlib import import_module
from types import ModuleType
from typing import Any

from colored import fg, bg, attr
TEST_FOLDERS = ('tests')


RED = fg('red')
GREEN = fg('green')
WHITE = fg('white')
GREY = fg('8')
RESET = attr('reset')


def main():

    p = path.abspath(f'./tests')
    if path.exists(p):
        test_dir = p
    else:
        print(f'{RED}Error: {RESET}No test folder found')
        return None

    files = []
    for file in os.listdir(test_dir):
        if file.endswith('.py'):
            files.append(import_module(f'tests.{file[:-3]}'))

    for file in files:
        run_tests(file)


def run_tests(file: ModuleType):
    for case in dir(file):
        if case.startswith('test_'):
            run_test(file, case)


def run_test(file: ModuleType, case: str):
    test = getattr(file, case)
    if callable(test):
        x, is_pass, description = test()

        desc = f'{fg("yellow")}{attr("bold")} {case} - {description}{RESET}'
        if is_pass:
            print(f'\n\n{WHITE}{bg("green")} PASS {RESET} {desc}')  
        else:
            print(f'\n\n{WHITE}{bg("red")} FAIL {RESET} {desc}')

        for i in x:
            if i['passed']:
                print('%s✓%s' % (GREEN, GREY), i['message'])
            else:
                print('%s✗%s' % (RED, GREY), i['message'])
                if i.get('callable'):
                    print(f'   {RED}- Expected: {WHITE}\t\t{i["name"]}({i["args_str"]}) {i["expected"]}')
                else:
                    print(f'   {RED}- Expected: {WHITE}\t\t{i["name"]} {i["expected"]}')
                print(f'   {RED}+ Recieved value: {WHITE}\t{i["recieved"]}')
        
    else:
        print(f'{case} is not a test case')



main()
