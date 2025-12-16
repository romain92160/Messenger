from datetime import datetime
import json

class User:
    def __init__(user, id: int, name: str):
            user.id = id
            user.name = name


class Channel:
    def __init__(channel, id: int, name: str, member_ids=None):
        channel.id = id
        channel.name = name
        channel.member_ids = member_ids or []

class Message:
    def __init__(self, id: int, channel: int, sender_id: int, content: str, reception_date: str):
        self.id = id
        self.channel = channel
        self.sender_id = sender_id
        self.content = content
        self.reception_date = reception_date



with open('server.json', 'r') as file:
        server = json.load(file)
        server_user = [User(user['id'], user['name']) for user in server['users']]
        server['users'] = server_user
        


def save_server():

    server_user = [{'id': user.id, 'name': user.name} for user in server['users']]
    server['users'] = server_user

    server_messages = [{
            'id': self.id,
            'channel': self.channel,
            'sender_id': self.sender_id,
            'content': self.content,
            'reception_date': self.reception_date
        } for self in server['messages']]
    server['messages'] = server_messages

    server_channels = [{
            'id': chan.id,
            'name': chan.name,
            'member_ids': chan.member_ids
        } for chan in server['channels']]
    server['channels'] = server_channels

    with open('server.json', 'w') as file:
        json.dump(server, file, indent=4)

    

'''
def user_class():
    user_list = []    
    for user in server['users']:
        user_class = (User(user['id'], user['name']))
        user_list.append(user_class)
   ''' 



def afficher_utilisateur():    
    for user in server['users']:
        print(user.name)

def afficher_groupes():
    for chan in server['channels']:
        print(chan.id,chan.name)



def send_messages(choicechannel : int):
    user_id = int(input('Enter your user id: '))
    content = input('Write a message: ')
    
    new_message = Message(
        'id': len(server['messages']) + 1,
        'channel': choicechannel,
        'sender_id': user_id,
        'content': content,
        'reception_date': datetime.now().isoformat()

 }
   
    server['messages'].append(new_message)
    save_server()
    for mess in server['messages'] :
            if mess['channel'] == choicechannel :
                print(mess['reception_date'][:16].replace('T', ' '), mess['content'])
    choicemessage = input('Envoyer un autre message ? (oui/non) : ')
    if choicemessage == 'oui' :
        user_id = int(input('Enter your user id: '))
        send_messages(choicechannel)
    else : 
        menu()




def afficher_messages():
    choicechannel = int(input('Select a channel id : '))
    for mess in server['messages'] :
        if mess['channel'] == choicechannel :
            print(mess['reception_date'][:16].replace('T', ' '), mess['content'])
    send_messages(choicechannel)




def ajouter_utilisateur():
    identifiant = int(input('identifiant: '))
    nom = str(input('nom utilisateur: '))
    newuser=User(identifiant, nom)
    server['users'].append(newuser)




def ajouter_groupe():
    identifiant = max(channel['id'] for channel in server['channels']) + 1
    nom = str(input('nom du groupe: '))
    membres = []
    ajout=input('Encore un nouveau membre ? (oui/non) : ')
    while ajout == 'oui':
        nouveaumembre=input('Identifiant du nouveau membre: ')
        membres.append(nouveaumembre)
        ajout=input('Encore un nouveau membre ? (oui/non) : ')
    nouveaugroupe={'id': identifiant, 'name': nom, 'member_ids': membres}
    server['channels'].append(nouveaugroupe)
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