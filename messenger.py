from datetime import datetime
import json

with open('server.json', 'r') as file:
    server = json.load(file)

def save_server():
    with open('server.json', 'w') as file:
        json.dump(server, file, indent=4)

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
    newuser={'id' : identifiant,'name' : nom}
    server['users'].append(newuser)
    save_server()

def ajouter_groupe():
    identifiant = int(input('identifiant du groupe: '))
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
    print('x. Leave, menu principal, utilisateurs, groupes, nouvel utilisateur, nouveau groupe')
    choice = input('Select an option: ')
    if choice == 'x':
        print('Bye!')
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