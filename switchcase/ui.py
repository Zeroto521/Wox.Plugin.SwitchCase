# -*- coding: utf-8 -*-

import copy
from typing import List

import pyperclip

from wox import Wox

from .constants import *
from .templates import *


class Main(Wox):

    messages_queue = []

    def sendNormalMess(self, title: str, subtitle: str):
        message = copy.deepcopy(RESULT_TEMPLATE)
        message['Title'] = title
        message['SubTitle'] = subtitle

        self.messages_queue.append(message)

    def sendActionMess(self, title: str, subtitle: str, method: str, value: List):
        # information
        message = copy.deepcopy(RESULT_TEMPLATE)
        message['Title'] = title
        message['SubTitle'] = subtitle

        # action
        action = copy.deepcopy(ACTION_TEMPLATE)
        action['JsonRPCAction']['method'] = method
        action['JsonRPCAction']['parameters'] = value
        message.update(action)

        self.messages_queue.append(message)

    def query(self, param: str) -> List[dict]:
        param = param.strip()

        if param:
            keyword, *string = param.split()
            string = ''.join(string)
            if string:
                if keyword == upperKeyword_long or keyword.startswith(upperKeyword_short):
                    value = str(string).upper()
                    self.sendActionMess(
                        "{} -> {}".format(string, value),
                        "Copy to clipboard.",
                        "copy2clipboard", [value]
                    )
                elif keyword == lowerKeyword_long or keyword.startswith(lowerKeyword_short):
                    value = str(string).lower()
                    self.sendActionMess(
                        "{} -> {}".format(string, value),
                        "Copy to clipboard.",
                        "copy2clipboard", [value]
                    )
                else:
                    self.sendNormalMess(
                        'Switch Case', 'Please check your keywords.')
            else:
                self.sendNormalMess(
                    'Switch Case', 'Please input words.')
        else:
            self.sendNormalMess(
                'Switch Case', 'Follow your words after the keyword.')

        return self.messages_queue

    def copy2clipboard(self, value: str):
        pyperclip.copy(value)
