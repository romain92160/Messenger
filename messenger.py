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



def send_messages(choicechannel : int):
    user_id = int(input('Enter your user id: '))
    content = input('Write a message: ')
    
    new_message = {
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
    newuser={'id' : identifiant,'name' : nom}
    server['users'].append(newuser)
    save_server()

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