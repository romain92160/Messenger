from datetime import datetime # gestion de dates
from typing import Optional 
import os # pour 
import json # utiliser json
import sys
import requests # requetes http
from rich.console import Console # affichage
from rich.table import Table # affichage
from rich import box # affichage


# Classes User, Channel et Message

class User:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id


class Channel:
    def __init__(self, id: int, name: str, member_ids: list[int]):
        self.id = id
        self.name = name
        self.member_ids = member_ids


class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int, content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content


# Classe des fonctions annexes ( elles seront utiles dans la suite)

class Annexe:
    @staticmethod
    def users_from_json(json_users: list[dict]) -> list[User]:
        return [User(u["name"], u["id"]) for u in json_users]

    @staticmethod
    def users_to_json(users: list[User]) -> list[dict]:
        return [{"id": u.id, "name": u.name} for u in users]

    @staticmethod
    def channels_from_json(json_channels: list[dict]) -> list[Channel]:
        return [Channel(c["id"], c["name"], c.get("member_ids", [])) for c in json_channels]

    @staticmethod
    def channels_to_json(channels: list[Channel]) -> list[dict]:
        return [{"id": c.id, "name": c.name, "member_ids": c.member_ids} for c in channels]

    @staticmethod
    def messages_from_json(json_messages: list[dict]) -> list[Message]:
        return [
            Message(m["id"], m["reception_date"], m["sender_id"], m["channel"], m["content"])
            for m in json_messages
        ]

    @staticmethod
    def messages_to_json(messages: list[Message]) -> list[dict]:
        return [
            {
                "id": m.id,
                "reception_date": m.reception_date,
                "sender_id": m.sender_id,
                "channel": m.channel,
                "content": m.content,
            }
            for m in messages
        ]

    def generateur_d_id(ids: list[int]) -> int:
        return max(ids) + 1 if ids else 1

    def trouver_nom_par_id(user_id: int) -> Optional[str]:
        for user in storage.get_users():
            if user.get("id") == user_id:
                return user.get("name")
        return None


annexe = Annexe()


# Stockage : Remote et Local

class RemoteStorage:
    def __init__(self, url: str):
        self.url = url.rstrip("/")

    # USERS
    def get_users(self) -> list[dict]:
        requete = requests.get(self.url + "/users")
        if requete.status_code != 200:
            print(requete.text)
            return []
        return requete.json()

    def create_user(self, new_user_name: str) -> Optional[dict]:
        payload = {"name": new_user_name}
        requete = requests.post(self.url + "/users/create", json=payload)
        if requete.status_code != 200:
            print(requete.text)
            return None
        return requete.json()

    # CHANNELS
    def get_channels(self) -> list[dict]:
        requete = requests.get(self.url + "/channels")
        if requete.status_code != 200:
            print(requete.text)
            return []
        data = requete.json()
        if isinstance(data, dict) and "channels" in data:
            return data["channels"]
        return data

    def create_channel(self, new_channel_name: str) -> Optional[dict]:
        payload = {"name": new_channel_name}
        requete= requests.post(self.url + "/channels/create", json=payload)
        if requete.status_code != 200:
            print(requete.text)
            return None
        return requete.json()

    def join_channel(self, channel_id: int, user_id: int) -> Optional[dict]:
        payload = {"user_id": user_id}
        requete = requests.post(
            self.url + f"/channels/{channel_id}/join",
            json=payload
        )
        if requete.status_code != 200:
            print(requete.text)
            return None
        return requete.json()

    # MESSAGES
    def get_messages_channel(self, channel_id: int) -> list[dict]:
        requete = requests.get(self.url + f"/channels/{channel_id}/messages")
        if requete.status_code != 200:
            print(requete.text)
            return []
        return requete.json()

    def post_message(self, channel_id: int, sender_id: int, content: str) -> Optional[dict]:
        payload = {"sender_id": sender_id, "content": content}
        requete = requests.post(
            self.url + f"/channels/{channel_id}/messages/post",
            json=payload
        )
        if requete.status_code != 200:
            print(requete.text)
            return None
        return requete.json()


class LocalStorage:
    
    def __init__(self, filename: str):
        self.filename = filename

    # USERS
    def get_users(self) -> list[dict]:
        return annexe.users_to_json(server["users"])

    def create_user(self, new_user_name: str) -> dict:
        user_ids = [u.id for u in server["users"]]
        new_id = annexe.generateur_d_id(user_ids)
        server["users"].append(User(new_user_name, new_id))
        return {"id": new_id, "name": new_user_name}

    # CHANNELS
    def get_channels(self) -> list[dict]:
        return annexe.channels_to_json(server["channels"])

    def create_channel(self, new_channel_name: str) -> dict:
        channel_ids = [c.id for c in server["channels"]]
        new_id = annexe.generateur_d_id(channel_ids)
        server["channels"].append(Channel(new_id, new_channel_name, []))
        return {"id": new_id, "name": new_channel_name, "member_ids": []}

    def join_channel(self, channel_id: int, user_id: int) -> Optional[dict]:
        channel = next((ch for ch in server["channels"] if ch.id == channel_id), None)
        if channel is None:
            print("Channel inconnu.")
            return None
        if not any(u.id == user_id for u in server["users"]):
            print("Utilisateur inconnu.")
            return None
        if user_id not in channel.member_ids:
            channel.member_ids.append(user_id)
        return {"id": channel.id, "name": channel.name, "member_ids": channel.member_ids}

    # MESSAGES
    def get_messages_channel(self, channel_id: int) -> list[dict]:
        messages = [m for m in server["messages"] if m.channel == channel_id]
        return annexe.messages_to_json(messages)

    def post_message(self, channel_id: int, sender_id: int, content: str) -> Optional[dict]:
        if not any(ch.id == channel_id for ch in server["channels"]):
            print("Channel inconnu.")
            return None
        if not any(u.id == sender_id for u in server["users"]):
            print("Utilisateur inconnu.")
            return None

        message_ids = [m.id for m in server["messages"]]
        message_id = annexe.generateur_d_id(message_ids)
        reception_date = datetime.now().isoformat(sep=" ", timespec="seconds")
        msg = Message(message_id, reception_date, sender_id, channel_id, content)
        server["messages"].append(msg)
        return annexe.messages_to_json([msg])[0]

    # load et save
    def load(self) -> None:
        global server
        if not os.path.exists(self.filename):
            server = {"users": [], "channels": [], "messages": []}
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            raw = json.load(f)

        server = {"users": [], "channels": [], "messages": []}
        server["users"] = annexe.users_from_json(raw.get("users", []))
        server["channels"] = annexe.channels_from_json(raw.get("channels", []))
        server["messages"] = annexe.messages_from_json(raw.get("messages", []))

    def sauvegarder(self) -> None:
        raw = {
            "users": annexe.users_to_json(server["users"]),
            "channels": annexe.channels_to_json(server["channels"]),
            "messages": annexe.messages_to_json(server["messages"]),
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=4, ensure_ascii=False)


# Affichage

class Affichage:
    def __init__(self, console: Console, storage):
        self.console = console
        self.storage = storage
    #  Utiles
    def clear_console(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def afficher_users(self) -> None:
        table = Table(title="[blue]Utilisateurs[/blue]", box=box.ASCII)
        table.add_column("ID", justify="right")
        table.add_column("Nom")
        for user in storage.get_users():
            table.add_row(str(user.get("id", "")), str(user.get("name", "")))
        self.console.print(table)

    def afficher_groupes(self) -> None:
        table = Table(title="[blue]Groupes[/blue]", box=box.ASCII)
        table.add_column("ID", justify="right")
        table.add_column("Nom")
        for channel in storage.get_channels():
            table.add_row(str(channel.get("id", "")), str(channel.get("name", "")))
        self.console.print(table)

    # Fonctionnalités de la Messagerie
    def ecrire_message_sur_channel(self) -> None:
        self.clear_console()
        self.afficher_groupes()
        try:
            channel_id = int(input("Donne l'id du channel: "))
            self.afficher_users()
            sender_id = int(input("Donne l'id de l'utilisateur (envoyeur): "))
            texte = input("Contenu du message: ")
            storage.post_message(channel_id, sender_id, texte)
        except ValueError:
            print("Entrée invalide.")
        input("Appuyez sur Entrée...")

    def trouver_id_channel_prive(self, user: str, destinataire: str) -> Optional[int]:
        nom1 = f"discussion privée de: {user} et {destinataire}".lower()
        nom2 = f"discussion privée de: {destinataire} et {user}".lower()

        for channel in storage.get_channels():
            nom_actuel = str(channel.get("name", "")).lower()
            if nom_actuel == nom1 or nom_actuel == nom2:
                return channel.get("id")
        return None

    def creation_channel_prive(self, user_name: str, dest_name: str, user_id: int, dest_id: int) -> Optional[int]:
        nom = f"discussion privée de: {user_name} et {dest_name}"
        result = storage.create_channel(nom)
        if not result:
            return None

        new_channel_id = result.get("id")
        if new_channel_id is None:
            print("Impossible de récupérer l'id du channel.")
            return None

        storage.join_channel(new_channel_id, user_id)
        storage.join_channel(new_channel_id, dest_id)
        return int(new_channel_id)

    def ecrire_message_prive(self) -> None:
        self.clear_console()
        self.afficher_users()
        print("--- Message Privé ---")

        try:
            user_id = int(input("Ton ID (envoyeur): "))
            user_name = annexe.trouver_nom_par_id(user_id)
            if user_name is None:
                print("Utilisateur introuvable.")
                input("Entrée...")
                return

            dest_id = int(input("ID du destinataire: "))
            dest_name = annexe.trouver_nom_par_id(dest_id)
            if dest_name is None:
                print("Destinataire introuvable.")
                input("Entrée...")
                return

            channel_id = self.trouver_id_channel_prive(user_name, dest_name)
            if channel_id:
                texte = input(f"Message pour {dest_name}: ")
                storage.post_message(channel_id, user_id, texte)
            else:
                print(f"Création d'une conversation avec {dest_name}...")
                new_id = self.creation_channel_prive(user_name, dest_name, user_id, dest_id)
                if new_id:
                    texte = input("Premier message: ")
                    storage.post_message(new_id, user_id, texte)

        except ValueError:
            print("Entrée invalide.")
        input("Appuyez sur Entrée...")

    def lire_messages_channel(self) -> None:
        self.clear_console()
        try:
            channel_id = int(input("Donne l'id du channel à lire: "))
            messages = storage.get_messages_channel(channel_id)

            table = Table(title="[blue]Messages[/blue]", box=box.ASCII)
            table.add_column("Sender ID", justify="right")
            table.add_column("Content")

            for m in messages:
                table.add_row(str(m.get("sender_id", "")), str(m.get("content", "")))

            self.console.print(table)
        except ValueError:
            print("Entrée invalide.")
        input("Appuyez sur Entrée pour continuer...")

    #  Différents ajouts
    def ajout_utilisateur(self) -> None:
        new_user_name = input("Donne le nom de ton utilisateur: ").strip()
        if not new_user_name:
            print("Nom vide.")
        else:
            storage.create_user(new_user_name)
        input("Entrée...")

    def ajout_groupe(self) -> None:
        new_channel_name = input("Donne le nom du channel: ").strip()
        if not new_channel_name:
            print("Nom vide.")
        else:
            storage.create_channel(new_channel_name)
        input("Entrée...")

    def rejoindre_channel(self) -> None:
        self.clear_console()
        self.afficher_groupes()
        try:
            channel_id = int(input("Donne l'id du channel à rejoindre: "))
            self.afficher_users()
            user_id = int(input("Donne l'id de l'utilisateur à ajouter: "))
            storage.join_channel(channel_id, user_id)
        except ValueError:
            print("Entrée invalide.")
        input("Entrée...")

    # Menus divers 
    def menu_utilisateur(self) -> None:
        self.clear_console()
        self.console.print("[bold blue]Utilisateurs[/bold blue]")
        print("1. Utilisateurs actuels")
        print("2. Ajouter un utilisateur")
        print("3. Retour")

        choice = input("Select an option: ").strip()
        if choice == "1":
            self.afficher_users()
            input("Entrée...")
        elif choice == "2":
            self.ajout_utilisateur()
        elif choice == "3":
            return
        else:
            print("Option inconnue.")
            input("Entrée...")

    def menu_channels(self) -> None:
        self.clear_console()
        self.console.print("[bold blue]Groupes[/bold blue]")
        print("1. Groupes actuels")
        print("2. Ajouter un groupe")
        print("3. Rejoindre un groupe")
        print("4. Retour")

        choice = input("Select an option: ").strip()
        if choice == "1":
            self.afficher_groupes()
            input("Entrée...")
        elif choice == "2":
            self.ajout_groupe()
        elif choice == "3":
            self.rejoindre_channel()
        elif choice == "4":
            return
        else:
            print("Option inconnue.")
            input("Entrée...")

    def menu_messages(self) -> None:
        self.clear_console()
        self.console.print("[bold blue]Messages[/bold blue]")
        print("1. Écrire sur un channel")
        print("2. Écrire un message privé")
        print("3. Lire les messages")
        print("4. Retour")

        choice = input("Select an option: ").strip()
        if choice == "1":
            self.ecrire_message_sur_channel()
        elif choice == "2":
            self.ecrire_message_prive()
        elif choice == "3":
            self.lire_messages_channel()
        elif choice == "4":
            return
        else:
            print("Option inconnue.")
            input("Entrée...")

    def menu(self) -> None:
        while True:
            self.clear_console()
            self.console.print("[bold blue]=== Messenger ===[/bold blue]")
            print("1. Utilisateurs")
            print("2. Channels")
            print("3. Messages")
            print("4. Leave")

            choice = input("Select an option: ").strip()
            if choice == "4":
                self.clear_console()
                print("Bye!")
                if isinstance(storage, LocalStorage):
                    storage.sauvegarder()
                return
            elif choice == "1":
                self.menu_utilisateur()
            elif choice == "2":
                self.menu_channels()
            elif choice == "3":
                self.menu_messages()
            else:
                print("Unknown option:", choice)
                input("Entrée...")



# Programme principal

URL_par_defaut = "https://groupe5-python-mines.fr"
Save_par_defaut = "save.json"

console = Console()
server: dict = {"users": [], "channels": [], "messages": []}

# Mode par défaut
mode = "remote"
URL = URL_par_defaut
SAVE_FILE = Save_par_defaut

import interface
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="donne le nom du mode à utiliser")
parser.add_argument("link", help = "donne soit le nom du fichier json, soit l'URL du site web")
parser.add_argument("interface", help = "dpnne le mode : soit terminal, soit interface")
args = parser.parse_args()

#Gestion du mode
if args.mode in ("local", "l", "loc", "lo"):
    mode = "local"
elif args.mode in ("remote", "r", "re", "remo"):
    mode = "remote"

if mode == "local":
    print("Mode LOCAL choisi")
    storage = LocalStorage(SAVE_FILE)
    console = Console()
    storage.load()
else :
    print("Mode REMOTE choisi")
    console = Console()
    storage = RemoteStorage(URL)

#gestion de l'URL / fichier json

if "http" in args.link :
    URL = args.link
elif "json" in args.link :
    SAVE_FILE = args.link

if args.interface == "interface":
    interface.MessengerGUI(storage).mainloop()
else : 
    affichage = Affichage(console, storage)
    affichage.menu()