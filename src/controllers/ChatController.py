import inspect
from flask import request, redirect, url_for
from src.core.utils import auth
from src.models.user import User
from src.models.db_worker import get_db


class ChatController(object):

    def __init__(self):
        self.conn = get_db()
        self.cursor = self.conn.cursor()
        self.username = request.args.get('login')
        if self.username:
            self.user = User.get_user_by_login(self.cursor, self.username)

    @auth
    def run(self, chat_name=None):
        chats = self.user.get_chat_list(self.cursor)
        if chat_name:
            cur_chat = None
            for chat in chats:
                if chat.name == chat_name:
                    cur_chat = chat
                    break
            if cur_chat is None:
                return redirect(url_for('/chat'))
            cur_massages = cur_chat.get_last_messages(self.cursor, 20)
            return str({cur_chat.name: cur_massages})
        return str({chat.name: chat.get_last_messages(self.cursor, 4) for chat in chats})

    @auth
    def test(self):
        print(request.args.get('login'))
        return 'hello, world!'