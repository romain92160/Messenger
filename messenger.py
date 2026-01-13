from datetime import datetime
import json
import requests
import os


class User:
    def __init__(user, id: int, name: str):
            user.id = id
            user.name = name
    @classmethod
    def from_dict(cls, d):
        return cls(d.get('id'), d.get('name'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class Channel:
    def __init__(channel, id: int, name: str, member_ids=None):
        channel.id = id
        channel.name = name
        channel.member_ids = member_ids or []
    @classmethod
    def from_dict(cls, d):
        return cls(d.get('id'), d.get('name'), d.get('member_ids', []))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'member_ids': self.member_ids}
    

class Message:
    def __init__(self, id: int, channel: int, sender_id: int, content: str, reception_date: str):
        self.id = id
        self.channel = channel
        self.sender_id = sender_id
        self.content = content
        self.reception_date = reception_date

    @classmethod
    def from_dict(cls, d):
        sid = d.get('sender_id', d.get('user_id'))
        return cls(d.get('id'), d.get('channel'), sid, d.get('content', ''), d.get('reception_date', ''))

    def to_dict(self):
        return {
            'id': self.id,
            'channel': self.channel,
            'sender_id': self.sender_id,
            'content': self.content,
            'reception_date': self.reception_date
        }

class RemoteStorage:
    def get_users(self):
        response = requests.get('https://groupe5-python-mines.fr/users')
        response.raise_for_status
        users_data = response.json()
        return [User(user['id'], user['name']) for user in users_data]
    def create_user(self, name: str):
        response = requests.post('https://groupe5-python-mines.fr/users/create', json={'name': name})
        if response.status_code != 200:
            print(response.text)
    def get_channels(self):
        response = requests.get('https://groupe5-python-mines.fr/channels')
        response.raise_for_status
        channels_data = response.json()
        return [Channel(chan['id'], chan['name'], chan.get('member_ids', [])) for chan in channels_data]
    def create_channel(self, name: str):
        response = requests.post('https://groupe5-python-mines.fr/channels/create', json={'name': name})
        if response.status_code != 200:
            print(response.text)
    def join_channel(self, channel_id: int, user_id: int):
        response = requests.post(f'https://groupe5-python-mines.fr/channels/{channel_id}/join', json={'user_id': user_id})
        if response.status_code != 200:
            print(response.text)
    def get_channel_members(self, channel_id: int):
        response = requests.get(f'https://groupe5-python-mines.fr/channels/{channel_id}/members')
        response.raise_for_status
        members_data = response.json()
        return [User.from_dict(m) for m in members_data]
    def get_messages(self, channel_id: int):
        response = requests.get(f'https://groupe5-python-mines.fr/channels/{channel_id}/messages')
        response.raise_for_status
        messages_data = response.json()
        return [Message.from_dict(m) for m in messages_data]
    def create_message(self, channel: int, sender_id: int, content: str):
        response = requests.post(f'https://groupe5-python-mines.fr/channels/{channel}/messages/post', json={'sender_id': sender_id, 'content': content})
        if response.status_code != 200:
            print(response.text)

def load_server(path='server.json'):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'users': [], 'channels': [], 'messages': []}

    data.setdefault('users', [])
    data.setdefault('channels', [])
    data.setdefault('messages', [])

    # convertir dict -> objets si nécessaire
    data['users'] = [User.from_dict(u) if isinstance(u, dict) else u for u in data['users']]
    data['channels'] = [Channel.from_dict(c) if isinstance(c, dict) else c for c in data['channels']]
    data['messages'] = [Message.from_dict(m) if isinstance(m, dict) else m for m in data['messages']]

    return data

def save_server(path='server.json'):
    server_copy = {
        'users': [u.to_dict() for u in server.get('users', [])],
        'channels': [c.to_dict() for c in server.get('channels', [])],
        'messages': [m.to_dict() for m in server.get('messages', [])],
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(server_copy, f, indent=4, ensure_ascii=False)

server = load_server('server.json')


def afficher_utilisateur():    
    for user in RemoteStorage().get_users():
        print(f"{user.id}. {user.name}")

def afficher_groupes():
    for chan in RemoteStorage().get_channels():
        print(chan.id,chan.name)
    consulter_groupes = input('Consulter les membres d\'un groupe ? (oui/non) : ')
    if consulter_groupes == 'oui':
        choicechannel = int(input('Select a channel id : '))
        members = RemoteStorage().get_channel_members(choicechannel)
        print('Membres du groupe :')
        for member in members:
            print(f"{member.id}. {member.name}")
    return

def send_messages(choicechannel : int):
    user_id = int(input('Enter your user id: '))
    content = input('Write a message: ')
    
    next_id = max((m.id for m in server['messages']), default=0) + 1
    new_message = Message(
        next_id,
        choicechannel,
        user_id,
        content,
        datetime.now().isoformat()
    )

    server['messages'].append(new_message)
    save_server()

    print('Messages dans le channel :')
    
    for mess in server['messages']:
        if mess.channel == choicechannel:
            print(mess.reception_date[:16].replace('T', ' '), mess.content)

    choicemessage = input('Envoyer un autre message ? (oui/non) : ')
    if choicemessage == 'oui':
        send_messages(choicechannel)
    else:
        menu()




def afficher_messages():
    choicechannel = int(input('Voir les messages du groupe (identifiant) : '))
    messages = RemoteStorage().get_messages(choicechannel)
    for mess in messages:
            print(mess.reception_date[:16].replace('T', ' '), mess.sender_id, mess.content)
    send_messages(choicechannel)




def ajouter_utilisateur():
    #next_id = max((getattr(u, 'id', 0) for u in server.get('users', [])), default=0) + 1
    nom = str(input('nom utilisateur: '))
    RemoteStorage().create_user(nom)
    #newuser = User(next_id, nom)
    #server['users'].append(newuser)
    save_server()


def get_channel_id_by_name(name: str):
    """Retourne l'id d'un channel par son nom"""
    channels = RemoteStorage().get_channels()
    for chan in channels:
        if chan.name == name:
            return chan.id
    return None 


def ajouter_groupe():
    nom = str(input('Nom du groupe: '))
    RemoteStorage().create_channel(nom)
    
    channel_id = get_channel_id_by_name(nom)
    if channel_id is None:
        print("Erreur : impossible de récupérer l'id du channel")
        return
    
    ajout = input('Encore un nouveau membre ? (oui/non) : ')
    while ajout == 'oui':
        afficher_utilisateur()
        try:
            nouveaumembre = int(input('Identifiant du nouveau membre: '))
            RemoteStorage().join_channel(channel_id, nouveaumembre)
        except ValueError:
            print("Identifiant invalide")
        ajout = input('Encore un nouveau membre ? (oui/non) : ')
    save_server()




def menu():

    print('=== Messenger ===')
    print('x. Sauvegarder et quitter, menu principal, utilisateurs, groupes, nouvel utilisateur, nouveau groupe')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
        save_server()
    elif choice == 'utilisateurs' :
        afficher_utilisateur()
        menu()
    elif choice == 'groupes':
        afficher_groupes()
        afficher_messages()
        menu()
    elif choice == 'nouvel utilisateur' :
        ajouter_utilisateur()
        menu()
    elif choice == 'nouveau groupe' :
        ajouter_groupe()
        menu()
    else:
        print('Unknown option:', choice)
        menu()


menu()