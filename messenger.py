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

print('=== Messenger ===')
print('x. Leave, utilisateurs, groupes')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
elif choice == 'utilisateurs' :
    for i in range(len(server['users'])):
         print(server['users'][i]['name'])
elif choice == 'groupes':
    for i in range(len(server['channels'])):
        print(server['channels'][i]['name'])
        choicechannel = input('Select a channel')
        for e in server['messages'] :
            if e['channel'] == choicechannel :
                print(e['content'])
else:
    print('Unknown option:', choice)

