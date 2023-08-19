import random
import string
from account_database import LoginDatabase


class Correntista:
    database = LoginDatabase()

    def __init__(self):  # Initilizing the variables
        self.login = Login("cognome", "nome", "email", "password", 0.0, "IBAN")
        self.account = None  # Logged in account
        self.account_loggato = None
        self.nome = None  # User's name
        self.cognome = None  # User's surname
        self.email = None
        self.password = None
        self.nuovo_iban = None
        self.saldo = 0.0  # User's balance
        self.nome_ricevente = None  # Receiver's name
        self.cognome_ricevente = None  # Receiver's surname
        self.iban_ricevente = None  # Receiver's IBAN

    # Iban generator method
    def iban_generator(self):
        letters = string.ascii_letters.upper()  # Print letters upper case
        numbers = string.digits  # Print numbers
        # Generate a 12 string casual characters: (8 letters, 2 numbers)
        random_part = random.choices(letters, k=10) + random.choices(numbers, k=2)
        nuovo_iban = "IT" + ''.join(random_part)  # Adds the "IT" prefix at the random_part
        return nuovo_iban

    def welcome(self):  # Welcome menu
        print("Benvenuto in Fuckbank!\nSeleziona dal menù:\n\t1. Registrati\n\t2. Login")

    def registrazione_utente(self):  # Sign up method
        self.database.init_db()

        print("Registra un nuovo account\n")
        self.nome = input("Nome: ")
        self.cognome = input("Cognome: ")

        # Create and handle email
        email_username = input("Username: ")
        while True:
            try:
                email_dominio = int(input('''Scegli il dominio:
                1- @google.com
                2- @outlook.com
                3- @libero.it
                '''))
                break
            except ValueError:
                print("Inserisci un valore valido.")
                continue

        dominio = ["@google.com", "@outlook.com", "@libero.it"]
        if email_dominio == 1:
            self.email = email_username + dominio[0]
        elif email_dominio == 2:
            self.email = email_username + dominio[1]
        elif email_dominio == 3:
            self.email = email_username + dominio[2]

        self.password = input("Password: ")

        nuovo_iban = self.iban_generator()

        # Checks the user email with all the registered mails. If a match is found it asks to try with another one.
        email_esistente = self.database.user_collection.find_one({'email': self.email}) is not None
        if email_esistente:
            print("Email già registrata. Riprova.")
        else:  # Otherwise the account is correctly registered
            print(f"""Utente registrato!
            Riepilogo
            Nome: {self.nome}
            Cognome: {self.cognome}
            Email: {self.email}
            Password: {self.password}
            Saldo: {self.saldo}
            IBAN: {nuovo_iban}""")

            # Creates a Login object using the user's data
            nuovo_account = {"nome": self.nome, "cognome": self.cognome, "email": self.email, "password": self.password,
                             "saldo": self.saldo, "iban": nuovo_iban}

            # Inserts the Dict into the Database
            insert_result = self.database.user_collection.insert_one(nuovo_account)

            if insert_result.inserted_id:
                print("Account inserito con successo!")
            else:
                print("Errore durante l'inserimento dell'account.")

    def login_utente(self):  # User login method
        self.database.init_db()

        print("Effettua il login\n")
        while True:  # Asks for email and password
            self.email = input("Email: ")
            self.password = input("Password: ")

            self.account_loggato = self.database.user_collection.find_one({"email": self.email, "password": self.password})

            if self.account_loggato is not None:  # If they matches
                self.nome = self.account_loggato['nome']
                self.cognome = self.account_loggato['cognome']
                print(f"Benvenuto {self.nome} {self.cognome}")  # Welcome message: name + surname
                break

            else:  # If the email and password don't match any of the accounts
                scelta = input("""Credenziali errate! Riprova o registrati:
                \t1. Riprova
                \t2. Registrati
                Selezione: """)

                if scelta == "1":  # Try again
                    continue
                elif scelta == "2":  # Sign up
                    self.registrazione_utente()
                    break

    def deposito(self):  # Deposit method
        self.database.init_db()
        while True:
            try:  # Checks whether the input is numeric
                importo = float(input("Inserire l'importo da depositare: €"))
                break
            except ValueError:
                print("Inserisci un valore valido.")
                continue

        nuovo_saldo = self.account_loggato['saldo'] + importo

        self.database.user_collection.update_one(
            {"_id": self.account_loggato['_id']},
            {'$set': {'saldo': nuovo_saldo}}
        )

        self.account_loggato['saldo'] = nuovo_saldo

        print(f"Saldo corrente: €{nuovo_saldo}")

    def prelievo(self):  # Withdrawal method
        self.database.init_db()

        while True:
            try:  # Checks whether the input is numeric
                importo = float(input("Inserire l'importo da prelevare: €"))
                break
            except ValueError:
                print("Inserisci un valore valido.")
                continue

        if importo <= self.account_loggato['saldo']:  # If it's less than the balance, show the result

            nuovo_saldo = self.account_loggato['saldo'] - importo

            self.database.user_collection.update_one(
                {"_id": self.account_loggato['_id']},
                {"$set": {'saldo': nuovo_saldo}}
            )

            self.account_loggato['saldo'] = nuovo_saldo

            print(f"\nPrelievo di €{importo} effettuato.\nNuovo saldo: €{nuovo_saldo}\n")
        else:  # If it's more, it fails
            print("Importo non valido o saldo insufficiente.")

    def bonifico(self):  # Bank transfer method
        bonifico_ok = True  # Checks whether the bank transfer is successful

        while bonifico_ok:
            print(f"Il tuo saldo è: €{self.account_loggato['saldo']}")
            nome_ricevente = input("Nome del ricevente: ")
            cognome_ricevente = input("Cognome del ricevente: ")
            iban_ricevente = input("IBAN: ")

            while True:
                try:  # Checks whether the input is numeric
                    importo = float(input("Inserisci l'importo: €"))
                    break
                except ValueError:
                    print("Inserisci un valore valido.")
                    continue

            account_ricevente = self.database.user_collection.find_one({
                'nome': nome_ricevente,
                'cognome': cognome_ricevente,
                'iban': iban_ricevente
            })

            if account_ricevente is not None:
                if importo <= self.account_loggato['saldo']:  # If the amount to send is less than the balance
                    saldo_utente_loggato = self.account_loggato['saldo'] - importo
                    saldo_ricevente = account_ricevente['saldo'] + importo
                    self.account_loggato['saldo'] = saldo_utente_loggato
                    account_ricevente['saldo'] = saldo_ricevente

                    self.database.user_collection.update_one(
                        {'_id': self.account_loggato['_id']},
                        {"$set": {"saldo": saldo_utente_loggato}}
                    )

                    self.database.user_collection.update_one(
                        {'_id': account_ricevente['_id']},
                        {"$set": {"saldo": saldo_ricevente}}
                    )

                    self.account_loggato['saldo'] = saldo_utente_loggato
                    account_ricevente['saldo'] = saldo_ricevente

                    print(f"Il saldo corrente è: €{saldo_utente_loggato}")  # Current user balance
                    print("Bonifico effettuato con successo!")
                    print(f"\nNuovo saldo ricevente: €{saldo_ricevente}")  # Current receiver's balance
                    bonifico_ok = True  # The bank transfer is successful

                else:  # If the amount is more than the balance
                    print("L'importo supera il saldo disponibile!")
                    bonifico_ok = False  # The bank transfer fails
                    continue

            else:  # If the inputs don't match any of the accounts
                print("Dati inseriti errati!")
                bonifico_ok = False  # The bank transfer fails
                continue

    def logout(self):  # Logout method
        scelta = input("Sei sicuro di voler uscire? Y/N ").casefold()  # Asks the user if to logout
        while scelta == "y" or scelta == "n":
            if scelta == "y":  # If the choice is yes
                print("Logout effettuato con successo!")
                break
            elif scelta == "n":  # if the choice is no
                break
            else:  # Error message if the answer is not "y" or "n"
                print("Scelta errata!")
                continue
        self.database.close_db()

