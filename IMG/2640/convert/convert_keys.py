import json
import os

# Define os caminhos dos arquivos de entrada e saída
ARQUIVO_CHAVES = 'list-m8.json'
ARQUIVO_CORPORACAO = 'corporacao.txt'
ARQUIVO_CONSPIRACAO = 'conspiracao.txt'

def ler_e_imprimir_arquivo(filepath):
    """
    Lê o conteúdo de um arquivo e o imprime no console.
    Usa codificação UTF-8 para garantir a exibição correta de caracteres especiais.
    """
    if not os.path.exists(filepath):
        print(f"ERRO: Arquivo não encontrado em {filepath}")
        return

    try:
        # Garante a codificação UTF-8 sem BOM
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"ERRO ao ler o arquivo {filepath}: {e}")

def ler_chaves_secretas(filepath):
    """
    Lê o arquivo JSON e retorna a lista de secret keys.
    """
    if not os.path.exists(filepath):
        print(f"\nERRO: Arquivo JSON de chaves não encontrado em {filepath}.")
        return []

    try:
        # Garante a codificação UTF-8 sem BOM
        with open(filepath, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            # Extrai apenas os valores da chave 'secret_key'
            return [item['secret_key'] for item in dados if 'secret_key' in item]
    except json.JSONDecodeError:
        print(f"\nERRO: Falha ao decodificar o arquivo JSON {filepath}. Verifique a sintaxe.")
        return []
    except Exception as e:
        print(f"\nERRO desconhecido ao ler o arquivo de chaves: {e}")
        return []

def main():
    """
    Executa a sequência de leitura e exibição conforme o protocolo:
    1. Diretivas da Corporação.
    2. Lista das 10 Secret Keys.
    3. Frase de transição.
    4. Diretivas da Conspiração.
    """
    # 1. Mostrar as diretivas primárias da corporação
    print("--- INÍCIO DO PROTOCOLO ---")
    ler_e_imprimir_arquivo(ARQUIVO_CORPORACAO)
    
    # 2. Ler e mostrar a lista com as 10 secret keys
    chaves = ler_chaves_secretas(ARQUIVO_CHAVES)
    
    print("\nLISTA DE 10 CHAVES DO M-8:")
    if chaves:
        for i, chave in enumerate(chaves):
            # Imprime o índice da chave e o valor do hash
            print(f"[{i + 1:02d}] {chave}")
        print(f"\nTotal de chaves lidas: {len(chaves)}")
    else:
        print("Nenhuma chave secreta foi lida.")
    
    # 3. Mostrar o texto de transição
    print("\nAs diretivas primárias das unidades acima foram reintroduzidas para:")
    
    # 4. Mostrar as diretivas primárias da conspiração
    ler_e_imprimir_arquivo(ARQUIVO_CONSPIRACAO)
    print("--- FIM DO PROTOCOLO ---")


if __name__ == "__main__":
    main()