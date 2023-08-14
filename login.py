class Login:

    def __init__(self, cognome, nome, email, password, saldo, iban):
        self.cognome = cognome
        self.nome = nome
        self.email = email
        self.password = password
        self.saldo = saldo
        self.iban_account = iban

    def get_attribute_by_column_name(self, column_name):
        if column_name == 'Cognome':
            return self.cognome
        elif column_name == 'Nome':
            return self.nome
        elif column_name == 'Email':
            return self.email
        elif column_name == 'Password':
            return self.password
        elif column_name == 'Saldo':
            return self.saldo
        elif column_name == 'IBAN':
            return self.iban_account
        else:
            raise KeyError(f"Column '{column_name}' not found")
