from datetime import datetime

server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi 👋'
        }
    ]
}


def afficher_utilisateur():
    for user in server['users']:
        idnom = str(user['id']) + '. ' + user['name']
        print(idnom)
        #idnom = f"{user['id']}.{user['name']}"

def afficher_groupes():
    for chan in server['channels']:
        print(chan['id'],chan['name'])

def afficher_messages():
    choicechannel = int(input('Select a channel id : '))
    for mess in server['messages'] :
        if mess['channel'] == choicechannel :
            print(mess['content'])

def ajouter_utilisateur():
    identifiant = int(input('identifiant: '))
    nom = str(input('nom utilisateur: '))
    server['users'].append({'id' : identifiant,'name' : nom})

def menu():
    print('=== Messenger ===')
    print('x. Leave, menu principal, utilisateurs, groupes, nouvel utilisateur, nouveau groupe')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
    elif choice == 'utilisateurs' :
        afficher_utilisateur()
    elif choice == 'groupes':
        afficher_groupes()
        afficher_messages()
    elif choice == 'nouvel utilisateur' :
        ajouter_utilisateur()

print('=== Messenger ===')
print('x. Leave, menu principal, utilisateurs, groupes, nouvel utilisateur, nouveau groupe')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'utilisateurs' :
    afficher_utilisateur()
elif choice == 'groupes':
    afficher_groupes()
    afficher_messages()
elif choice == 'nouvel utilisateur' :
    ajouter_utilisateur()
elif

else:
    print('Unknown option:', choice)
