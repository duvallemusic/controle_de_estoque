# programa de controle de estoque
# o menu principal do programa possui as seguintes opções:
# 1. Cadastrar produto
# 2. Listar produtos
# 3. remover produto
# 4. atualizar quantidade de produto
# 5. Sair

# Sistema de Gerenciamento de 

#função de exibir menu

import json

def exibir_menu():
    print("\n===== ESTOQUE FÁCIL =====")
    print("\n===== MENU =====")
    print("1) Adicionar produto")
    print("2) Listar produtos")
    print("3) Remover produto")
    print("4) Atualizar quantidade de produto")
    print("5) Sair")
    print("6) Salvar estoque em arquivo")
    print("7) Carregar estoque de arquivo")
    return input("Escolha uma opção (1-7): ").strip()

#função que define a quantidade de produtos como numero inteiro
def ler_inteiro(mensagem, minimo=None):
    while True:
        valor = input(mensagem).strip()
        try:
            num = int(valor)
            if minimo is not None and num < minimo:
                print(f"Valor deve ser >= {minimo}.")
                continue
            return num
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

#função que define o preço do produto como numero float
# permite usar ponto ou vírgula como separador decimal
def ler_float(mensagem, minimo=None):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            num = float(valor)
            if minimo is not None and num < minimo:
                print(f"Valor deve ser >= {minimo}.")
                continue
            return num
        except ValueError:
            print("Entrada inválida. Digite um número (use ponto ou vírgula para decimais).")

# função para adicionar produto ao estoque
# verifica se o nome do produto já existe
def adicionar_produto(estoque):
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Nome do produto não pode ser vazio.")
        return

    quantidade = ler_inteiro("Quantidade: ", minimo=0)
    preco = ler_float("Preço: R$ ", minimo=0.0)

    if nome in estoque:
        print("Produto já existia. Atualizando quantidade e preço.")
    estoque[nome] = {"quantidade": quantidade, "preço": preco}
    print(f"Produto '{nome}' salvo com sucesso.")


def listar_produtos(estoque):
    if not estoque:
        print("Nenhum produto cadastrado.")
        return

    print("\n=== LISTA DE PRODUTOS ===")
    # Ordena alfabeticamente pelo nome do produto (case-insensitive) usando lambda
    for nome, dados in sorted(estoque.items(), key=lambda x: x[0].lower()):
        qtd = dados["quantidade"]
        preco = dados["preço"]
        print(f"{nome}: {qtd} disponível(is) - R$ {preco:.2f}")


def remover_produto(estoque):
    nome = input("Nome do produto a remover: ").strip()
    if nome in estoque:
        del estoque[nome]
        print(f"Produto '{nome}' removido com sucesso.")
    else:
        print("Erro: produto não encontrado.")


def atualizar_quantidade(estoque):
    nome = input("Nome do produto: ").strip()
    if nome not in estoque:
        print("Erro: produto não encontrado.")
        return
    nova_qtd = ler_inteiro("Nova quantidade: ", minimo=0)
    estoque[nome]["quantidade"] = nova_qtd
    print(f"Quantidade do produto '{nome}' atualizada para {nova_qtd}.")

def salvar_estoque(estoque):
    caminho = input("Nome do arquivo para salvar (padrão: estoque.json): ").strip() or "estoque.json"
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estoque, f, ensure_ascii=False, indent=2)
        print(f"Estoque salvo em '{caminho}'.")
    except OSError as e:
        print(f"Erro ao salvar arquivo: {e}")


def carregar_estoque():
    caminho = input("Nome do arquivo para carregar (padrão: estoque.json): ").strip() or "estoque.json"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # validação básica do formato
        if not isinstance(dados, dict):
            raise ValueError("Formato inválido: esperado dicionário de produtos.")
        for nome, item in dados.items():
            if not (isinstance(item, dict) and "quantidade" in item and "preço" in item):
                raise ValueError(f"Formato inválido no produto '{nome}'.")
            # normaliza tipos
            item["quantidade"] = int(item["quantidade"])
            item["preço"] = float(item["preço"])

        print(f"Estoque carregado de '{caminho}'.")
        return dados
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Erro ao interpretar o arquivo: {e}")
    except OSError as e:
        print(f"Erro ao ler o arquivo: {e}")
    return None    

# menu principal do programa

def main():
    estoque = {}
    while True:
        opcao = exibir_menu()
        if opcao == "1":
            adicionar_produto(estoque)
        elif opcao == "2":
            listar_produtos(estoque)
        elif opcao == "3":
            remover_produto(estoque)
        elif opcao == "4":
            atualizar_quantidade(estoque)
        elif opcao == "5":
            print("Programa finalizado. Obrigado por usar o Estoque Fácil!")
            break
        elif opcao == "6":
            salvar_estoque(estoque)
        elif opcao == "7":
            dados = carregar_estoque()
            if dados is not None:
                estoque = dados  # substitui o estoque atual pelo carregado
        else:
            print("Opção inválida. Digite um número correspondente a opção desejada disponível no menu.")


if __name__ == "__main__":
    main()
