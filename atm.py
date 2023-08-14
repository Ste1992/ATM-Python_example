from correntista import Correntista


class Atm:
    correntista = Correntista()  # Initializes the "correntista" class in order to access its methods
    correntista.load_data_from_csv("account_data.csv")  # Loads the data at the start of the program

    access = False  # Inizialmente l'utente non è loggato
    registrazione_completata = False
    correntista.iban_generator()
    correntista.welcome()

    while True:
        if not access:  # The user is still offline: Signs up and logs in - or - logs in
            try:
                scelta = float(input("Selezione: "))
            except ValueError:
                print("Input non valido.")
                continue

            if scelta == 1:  # The user signs up and logs in
                correntista.registrazione_utente()
                correntista.save_data_to_csv("account_data.csv")  # Saves the data every time changes occur
                registrazione_completata = True  # The user signed up
                correntista.login_utente()
                access = True  # Login successful
            elif scelta == 2:  # The user logs in: Account already registered
                correntista.login_utente()
                access = True  # The user successfully logs in
            else:  # Error message if the choice is not 1 or 2
                print("Selezione non valida.")

        if access or registrazione_completata:  # The user accesses the menu once online

            try:
                scelta = float(input("""Menu:\n\t1. Deposito\n\t2. Prelievo\n\t3. Bonifico\n\t4. Esci\nSelezione: """))
                if scelta < 1 or scelta > 4:
                    print("Input non valido.")
                    continue
            except ValueError:  # If the input is not a number
                print("Input non valido. Inserisci un numero.")
                continue

            if scelta == 1:  # Bank deposit
                correntista.deposito()
                correntista.save_data_to_csv("account_data.csv")
                continue
            elif scelta == 2:  # Withdrawal
                correntista.prelievo()
                correntista.save_data_to_csv("account_data.csv")
                continue
            elif scelta == 3:  # Bank transfer
                correntista.bonifico()
                correntista.save_data_to_csv("account_data.csv")
                continue
            elif scelta == 4:
                correntista.logout()
                access = False  # Stops the session
                correntista.save_data_to_csv("account_data.csv")
                print("Account scollegato con successo.")
                break
