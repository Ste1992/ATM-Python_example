import random
import csv
from login import Login  # importa la classe Login dal file login.py


class Correntista:

    def __init__(self):  # Initilizing the variables
        self.login = Login("cognome", "nome", "email", "password", 0.0, "IBAN")
        self.accounts = set()  # Accounts list variable
        self.account_loggato = None  # Logged in account
        self.account = set()  # Signed up accounts list
        self.nome = None  # User's name
        self.cognome = None  # User's surname
        self.email = None
        self.password = None
        self.nuovo_iban = None
        self.saldo = 0.0  # User's balance
        self.nome_ricevente = None  # Receiver's name
        self.cognome_ricevente = None  # Receiver's surname
        self.iban_ricevente = None  # Receiver's IBAN

    def iban_generator(self):
        letters = "ABCDEFGHILKMNOPQRSTUWVUXYZ"  # Letters' string
        numbers = "0123456789"  # Numbers' string
        # Generate a 12 string casual characters: (8 letters, 2 numbers)
        random_part = random.choices(letters, k=10) + random.choices(numbers, k=2)
        nuovo_iban = "IT" + ''.join(random_part)  # Adds the "IT" prefix at the random_part
        return nuovo_iban

    def welcome(self):  # Welcome menu
        print("Benvenuto in Fuckbank!\nSeleziona dal menù:\n\t1. Registrati\n\t2. Login")

    def registrazione_utente(self):  # Sign up method
        print("Registra un nuovo account\n")
        self.nome = input("Nome: ")
        self.cognome = input("Cognome: ")
        self.email = input("Email: ")
        self.password = input("Password: ")

        nuovo_iban = self.iban_generator()

        # Checks the user email with all the registered mails. If a match is found it asks to try with another one.
        email_esistente = any(account.email == self.email for account in self.accounts)
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
            nuovo_account = Login(self.cognome, self.nome, self.email, self.password, 0.0, nuovo_iban)
            self.accounts.add(nuovo_account)  # Add the new account to the accounts' list

    def login_utente(self):  # User login method
        print("Effettua il login\n")

        while self.account_loggato is None:  # Asks for email and password
            self.email = input("Email: ")
            self.password = input("Password: ")

            for account in self.accounts:  # Checks through all the accounts until it acquires the required account data
                if self.email == account.email and self.password == account.password:  # If they matches
                    print(f"Benvenuto {account.nome} {account.cognome}")  # Welcome message: name + surname
                    self.account_loggato = account  # Aggiungi l'account loggato a self.login_loggato
                    break

            if self.account_loggato is None:  # If the email and password don't match any of the accounts
                scelta = input("""Credenziali errate! Riprova o registrati:
                \t1. Riprova
                \t2. Registrati
                Selezione: """)

                if scelta == "1":  # Try again
                    continue
                elif scelta == "2":  # Sign up
                    self.registrazione_utente()
                    break

    def prelievo(self):  # Withdrawal method
        while True:
            try:  # Checks whether the input is numeric
                importo = float(input("Inserire l'importo da prelevare: €"))
                break
            except ValueError:
                print("Inserisci un valore valido.")
                continue

        if importo <= self.account_loggato.saldo:  # If it's less than the balance, show the result
            self.account_loggato.saldo -= importo
            print(f"\nPrelievo di €{importo} effettuato.\nNuovo saldo: €{self.account_loggato.saldo}\n")
        else:  # If it's more, it fails
            print("Importo non valido o saldo insufficiente.")

    def deposito(self):  # Deposit method
        while True:
            try:  # Checks whether the input is numeric
                importo = float(input("Inserire l'importo da depositare: €"))
                break
            except ValueError:
                print("Inserisci un valore valido.")
                continue

        self.account_loggato.saldo += importo
        print(f"Saldo corrente: €{self.account_loggato.saldo}")

    def bonifico(self):  # Bank transfer method
        bonifico_ok = True  # Checks whether the bank transfer is successful
        while bonifico_ok:
            print(f"Il tuo saldo è: €{self.account_loggato.saldo}")
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

            ricevente_trovato = False  # Checks whether the receiver is found
            account_ricevente = None  # Stores the receiver's data account

            for account in self.accounts:
                if (nome_ricevente == account.nome and
                        cognome_ricevente == account.cognome and
                        iban_ricevente == account.iban):
                    ricevente_trovato = True  # The inputs match an account datas
                    account_ricevente = account  # Initializes the variable
                    break

            if ricevente_trovato:  # Elaborates the transfer and shows the result
                if importo <= self.account_loggato.saldo:  # If the amount to send is less than the balance
                    saldo_utente = self.account_loggato.saldo - importo
                    saldo_ricevente = account.saldo + importo
                    self.account_loggato.saldo = saldo_utente
                    account_ricevente.saldo = saldo_ricevente
                    print(f"Il saldo corrente è: €{saldo_utente}")  # Current user balance
                    print("Bonifico effettuato con successo!")
                    print(f"\nNuovo saldo ricevente: €{saldo_ricevente}")  # Current receiver's balance
                    bonifico_ok = True  # The bank transfer is successful
                elif importo > self.account_loggato.saldo:  # If the amount is more than the balance
                    print("L'importo supera il saldo disponibile!")
                    bonifico_ok = False  # The bank transfer fails
                    continue
                else:  # If the inputs don't match any of the accounts
                    print("Dati inseriti errati!")
                    bonifico_ok = False  # The bank transfer fails
                    continue

    def save_data_to_csv(self, filename):  # Save data method: it takes the file name as parameter
        with open(filename, 'w', newline='') as csvfile:  # Opens, writes the file as a .csv file extension
            fieldnames = ['Cognome', 'Nome', 'Email', 'Password', 'Saldo', 'IBAN']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # L'oggetto csv.DictWriter userà questo file per scrivere i dati.
            # fieldnames: Questi nomi di colonna corrispondono alle chiavi dei dizionari che verranno passati a writerow()
            # per scrivere una riga nel file CSV.

            writer.writeheader()  # Writes the header in the CSV file: it uses the columns' names defined using "DictWriter"

            for account in self.accounts:

                if account.iban_account is None:
                    iban_to_use = self.nuovo_iban
                else:
                    iban_to_use = account.iban_account

                row = {
                    'Cognome': account.cognome,
                    'Nome': account.nome,
                    'Email': account.email,
                    'Password': account.password,
                    'Saldo': str(account.saldo),
                    'IBAN': iban_to_use
                }
                row_str = ", ".join(row.values())
                csvfile.write(row_str + '\n')

    def load_data_from_csv(self, filename):
        self.accounts.clear()  # Clear existing accounts before loading

        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.accounts.add(Login(
                    row['Cognome'],
                    row['Nome'],
                    row['Email'],
                    row['Password'],
                    float(row['Saldo']),
                    row['IBAN']
                ))

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

