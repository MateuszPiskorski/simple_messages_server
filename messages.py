import argparse

from psycopg2 import connect, OperationalError

from clcrypto import check_password
from models import Message, User


parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="message recipient")
parser.add_argument("-s", "--send", help="message content")
parser.add_argument("-l", "--list", help="list all user messages", action="store_true")

args = parser.parse_args()


def list_messages(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        messages = Message.load_all_messages(cur, user.id)
        for message in messages:
            from_ = User.load_user_by_id(cur, message.from_id)
            print(20 * "-")
            print(f"from: {from_.username}")
            print(f"date: {message.creation_date}")
            print(message.text)
            print(20 * "-")
    else:
        print("Incorrect password!")


def send_message(cur, username, password, recipient, text):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        recipient = User.load_user_by_username(cur, recipient)
        if not recipient:
            print("Recipient does not exist!")
        else:
            if len(text) > 255:
                print("Message too long (max 255 characters)")
            else:
                message = Message(user.id, recipient.id, text)
                message.save_to_db(cur)
    else:
        print("Incorrect password!")


if __name__ == '__main__':
    try:
        cnx = connect(database="msg_server_db", user="postgres", password="asdf11", host="localhost")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.list:
            list_messages(cursor, args.username, args.password)
        elif args.username and args.password and args.to and args.send:
            send_message(cursor, args.username, args.password, args.to, args.send)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)
