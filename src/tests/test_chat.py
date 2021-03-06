import unittest
from models import db_worker
from models import chat


class TestChat(unittest.TestCase):
    # TODO продумать автоматическую инициализацию тестовых данных
    """
    Тесты корректно работают только на данных,
    формируемых скриптами из sql/re_init_db
    """
    def setUp(self):
        self.db = db_worker.get_db()
        self.cursor = self.db.cursor(dictionary=True)

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_all_chat(self):
        print('asd')
        chat_list = chat.Chat.get_all_chats(self.cursor)
        self.assertEqual(3, len(chat_list))

    def test_chat_all_messages(self):
        ch = chat.Chat(name='support-1', id=1)
        message_list = ch.get_messages(self.cursor)
        self.assertEqual(3, len(message_list))
        message_list = ch.get_messages(self.cursor, offset=0, limit=2)
        self.assertEqual(2, len(message_list))
        message_list = ch.get_messages(self.cursor, limit=1)
        self.assertEqual(1, len(message_list))

    def test_user_list(self):
        ch1 = chat.Chat(id=1, name='support-1')
        userlst1 = ch1.get_user_list(self.cursor)
        self.assertEqual(2, len(userlst1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
