#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db_worker
import logging
import chat


class User:
    def __init__(self, id, login, email, role, password):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.role = role

    def __str__(self):
        return 'id = {0},\tlogin = {1},\temail = {2},\tpassword = {3},\trole = {4}'.format(
                self.id, self.login, self.email, self.password, self.role)

    @staticmethod
    def get_all_users(conn):
        users = db_worker.execute(conn, 'CALL GET_ALL_USERS()')
        return [User(id=u['USER_ID'],
                     login=u['LOGIN'],
                     email=u['EMAIL'],
                     password=u['PASSWORD'],
                     role=u['ROLE'])
                for u in users]

    @staticmethod
    def get_user_by_id(conn, id):
        u = db_worker.execute(conn, 'CALL GET_USER_BY_ID(%s)', (id,))
        if len(u) == 0:
            logging.write('Пользователя № %s не существует!' % id)
            return None
        u = u[0]
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    role=u['ROLE'])

    @staticmethod
    def get_user_by_login(conn, log):
        u = db_worker.execute(conn, 'CALL GET_USER_BY_LOGIN(%s)', (log,))
        if len(u) == 0:
            logging.write('Пользователя %s не существует!' % log)
            return None
        u = u[0]
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    role=u['ROLE'])

    def get_chat_list(self, conn):
        chats = db_worker.execute(conn, 'CALL GET_CHAT_LIST_BY_USER_ID(%s)', (self.id,))
        return [chat.Chat(id=ch['CHAT_ID'],
                          name=ch['NAME'])
                for ch in chats]

    @staticmethod
    def create_user(conn, u):
        result = db_worker.execute(conn,
                                   'CALL CREATE_USER(%s, %s, %s, %s)',
                                   (u.login, u.email, u.password, u.role)
                                   )
        result = result[0]
        return result['NEW_ID']

    @staticmethod
    def delete_user(conn, u):
        return db_worker.change(conn, 'CALL DELETE_USER_BY_ID(%s)', (u.id,))


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor(dictionary=True)

    # Поиск пользователя по логину:
    # - если пользователь с указанным логином не найден, он добавляется в базу;
    # - если найден - удаляется из базы.
    login = 'user_x'
    logging.write('----------------\nПользователь %s:' % login)
    user_x = User.get_user_by_login(cursor, login)
    if user_x:
        logging.write('Пользователь %s найден:' % login)
        logging.write(user_x)
        result = User.delete_user(cursor, user_x)
        logging.write('Пользователь %s удалён. Строк изменено: %s' % (login, result))
    else:
        user_x = User(id=0, login=login, email='test@test.test', password='1', role='staffer')
        user_x.id = User.create_user(cursor, user_x)
        logging.write('Пользователь %s добавлен:' % login)
        logging.write(user_x)

    # Поиск всех пользователей
    user_list = User.get_all_users(cursor)
    logging.write('----------------\nВсего пользователей: %s' % len(user_list))
    for u in user_list:
        logging.write(u)
        current_user_chats_list = u.get_chat_list(cursor)
        logging.write('Список чатов %s:' % u.login)
        for ch in current_user_chats_list:
            logging.write(ch)
        logging.write('')

    # Поиск списка чатов пользователя
    login = 'admin'
    user_admin = User.get_user_by_login(cursor, login)
    logging.write('Список чатов пользователя %s:' % login)
    admin_chat_list = user_admin.get_chat_list(cursor)
    for chat in admin_chat_list:
        logging.write(chat)

    # Поиск пользователя по id
    id = 2
    logging.write('----------------\nПользователь id = %s' % id)
    user2 = User.get_user_by_id(cursor, id)
    logging.write(user2)

    # sql-инъекция
    login = 'john\'); DROP database freebee;-- '
    logging.write('----------------\nПользователь %s:' % login)
    user_drop_table = User.get_user_by_login(cursor, login)
    logging.write(user_drop_table)

    # Поиск пользователя, отсутствующего в базе
    login = 'dfghjskdlf'
    logging.write('----------------\nПользователь %s:' % login)
    user_nonsense = User.get_user_by_login(cursor, login)
    logging.write(user_nonsense)

    cursor.close()
    db.commit()
    db.close()
