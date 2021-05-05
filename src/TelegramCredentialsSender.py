import telethon
from telethon import TelegramClient
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest, AddContactRequest
import phonenumbers
from rich.progress import track
import csv

from config import *

# telegram API credentials. Visit https://core.telegram.org/
API_NAME = ''
API_HASH = ''
API_ID = ''


def get_login_message(name: str, password: str) -> str:
    return f'**👋 Hello, I\'m authomatical credentials sender**\n' \
           f'I was made by sultanowskii ([Github](https://github.com/sultanowskii))\n' \
           f'Please don\'t write me - I won\'t answer you\n\n' \
           f'Login: `{name}`\n' \
           f'Password: `{password}`\n'


# Requires user.csv
def send_credentials():
    bad_logins = 0
    all_logins = 0
    chats = {}

    with open('users.csv', 'r') as data:
        users = csv.DictReader(data)
        for user in users:
            chats[user['telegram']] = get_login_message(user['name'], user['password'])
            all_logins += 1

    contacts = []
    client = TelegramClient(API_NAME, api_hash=API_HASH, api_id=API_ID)
    print('[*] Connected to telegram')


    async def send():
        cntr = 0

        # adding contacts in client to make it possible to send message by number
        for contact, message in track(chats.items(), description='Sending messages...'):
            if not (contact.isdigit() or contact[1:].isdigit()):
                # surely not phone number, skip it
                continue
            try:
                x = phonenumbers.parse(contact, None)
            except Exception:
                continue
            if phonenumbers.is_valid_number(x):
                contacts.append(InputPhoneContact(
                    client_id=0,
                    phone=contact,
                    first_name=f'FN{cntr}',
                    last_name=f'LN{cntr}'
                ))
                cntr += 1
        result = await client(ImportContactsRequest(contacts=contacts))
        
        for contact, message in chats.items():
            entity = await client.get_entity(contact)
            try:
                await client.send_message(entity=entity, message=message)
            except Exception as e:
                print(f'[!] Message wasn\'t sent because of error:\n{e}')
                bad_logins += 1
            print(f'[.] Sent message to {contact}')

    with client:
        client.loop.run_until_complete(send())
    percentage = round((all_logins - bad_logins) / all_logins * 100, 2)
    print(f'[*] {percentage}% of messages sent successfully')


if __name__ == '__main__':
    send_credentials()