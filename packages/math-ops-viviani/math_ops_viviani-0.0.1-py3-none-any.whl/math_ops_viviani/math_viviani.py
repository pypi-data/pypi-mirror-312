class Calculadora:
    """
    Classe para realizar operações matemáticas básicas.
    """
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def soma(self):
        return self.num1 + self.num2

    def subtracao(self):
        return self.num1 - self.num2

    def multiplicacao(self):
        return self.num1 * self.num2

    def divisao(self):
        if self.num2 == 0:
            return "Erro: divisão por zero!"
        return self.num1 / self.num2

    def exponenciacao(self):
        return self.num1 ** self.num2

# Função principal para interagir com o usuário
def main():
    print("Bem-vindo à Calculadora!")
    
    # Entrada do usuário
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    
    # Instanciar a calculadora
    calc = Calculadora(num1, num2)
    
    # Exibir os resultados
    print(f"Soma: {calc.soma()}")
    print(f"Subtração: {calc.subtracao()}")
    print(f"Multiplicação: {calc.multiplicacao()}")
    print(f"Divisão: {calc.divisao()}")
    print(f"Exponenciação: {calc.exponenciacao():.2f}")

# Executar o programa
if __name__ == "__main__":
    main()