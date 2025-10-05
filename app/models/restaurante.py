class Restaurante:
    contador = 0
    def __init__(self, email: str, senha: str, restaurante_nome: str, comissao: int):
        Restaurante.contador += 1
        self.pk = Restaurante.contador
        self.email = email.lower()
        self.senha = senha
        self.restaurante_nome = restaurante_nome
        self.comissao = comissao
        
    def __str__(self):
        return f'{self.restaurante_nome}'
    
    @staticmethod
    def validar_comissao(comissao: int) -> bool:
        if comissao >= 0:
            return True
        return False
    
    @staticmethod
    def validar_email(email: str) -> bool:
        if email.count('@') != 1:
            return False
        elif email.count('.') < 1:
            return False
        usuario, dominio = email.split('@')
        if len(usuario) < 1 or len(dominio) < 3:
            return False
        elif ' ' in usuario or ' ' in dominio:
            return False
        elif dominio[0] == '.' or dominio[-1] == '.':
            return False
        return True
    
    @staticmethod
    def validar_senha(senha: str) -> bool:
        if len(senha) < 5:
            return False
        if not any(caracter.isupper() for caracter in senha):
            return False    
        if not any(caracter.islower() for caracter in senha):
            return False                
        if not any(caracter.isdigit() for caracter in senha):
            return False
        return True

    @staticmethod
    def validar_nome(restaurante_nome: str) -> bool:
        if len(restaurante_nome) < 10:
            return False
        return True