class Validador:
    @staticmethod
    def valida_comissao(comissao: int) -> bool:
        if comissao >= 0:
            return True
        return False
    
    @staticmethod
    def valida_email(email: str) -> bool:
        import re
        regex = r'^[a-zA-Z0-9]@[a-zA-Z0-9].[a-z]'
        # muito legal 
        if re.search(regex, email):
            return True
        return False

    @staticmethod
    def valida_senha(senha: str) -> bool:
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
    def valida_nome_restaurante(restaurante_nome: str) -> bool:
        if len(restaurante_nome) > 10:
            return True
        return False 
