import requests  # Biblioteca para fazer requisições HTTP
import gspread  # Biblioteca para interagir com o Google Sheets
from oauth2client.service_account import ServiceAccountCredentials  # Biblioteca para autenticação com o Google API
import time  # Biblioteca para controlar o tempo de execução

def coletar_dados_api(url):
    """
    Função para fazer uma requisição à API e coletar dados.
    """
    try:
        response = requests.get(url)  # Faz a requisição para a URL fornecida
        response.raise_for_status()  # Verifica se houve algum erro na requisição

        if response.text.strip() == "":
            print("A resposta da API está vazia.")  # Mensagem se a resposta estiver vazia
            return None

        try:
            return response.json()  # Tenta converter a resposta para JSON
        except ValueError:
            print("Erro ao decodificar a resposta como JSON.")
            print("Resposta recebida:", response.text)  # Mostra a resposta recebida para depuração
            return None
    except requests.RequestException as err:
        print(f"Erro ao acessar a API: {err}")  # Mensagem de erro se houver problemas com a requisição
        return None

def achatar_dicionario(d, prefixo=''):
    """
    Função recursiva para achatar dicionários aninhados.
    """
    itens = []
    for chave, valor in d.items():
        nova_chave = f"{prefixo}_{chave}" if prefixo else chave  # Cria uma nova chave combinando o prefixo com a chave original
        if isinstance(valor, dict):
            itens.extend(achatar_dicionario(valor, nova_chave).items())  # Chama a função recursivamente para dicionários aninhados
        else:
            itens.append((nova_chave, valor))  # Adiciona o valor ao item
    return dict(itens)

def enviar_para_google_sheets(dados, nome_planilha):
    """
    Função para enviar os dados coletados para uma planilha Google Sheets.
    """
    if not dados:
        print("Nenhum dado a enviar para o Google Sheets")  # Mensagem se não houver dados para enviar
        return

    # Define os escopos de acesso às APIs do Google Sheets e Google Drive
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Carrega as credenciais do arquivo JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais_google_sheets.json', scope)
    # Autoriza o cliente com as credenciais
    client = gspread.authorize(creds)

    try:
        # Abre a planilha pelo nome
        sheet = client.open(nome_planilha).sheet1
    except gspread.SpreadsheetNotFound:
        print(f"Planilha '{nome_planilha}' não encontrada.")  # Mensagem se a planilha não for encontrada
        return
    except Exception as e:
        print(f"Erro de autenticação: {e}")  # Mensagem de erro se houver problemas com a autenticação
        return

    print("Limpando a planilha...")
    sheet.clear()  # Limpa o conteúdo da planilha

    # Prepara o cabeçalho com os nomes das colunas
    header = list(achatar_dicionario(dados[0]).keys())
    header.append('Ano')  # Adiciona a coluna 'Ano' ao cabeçalho
    print("Enviando cabeçalho...")
    sheet.append_row(header)  # Adiciona o cabeçalho à planilha

    linhas_para_inserir = []
    for item in dados:
        item_achatado = achatar_dicionario(item)  # Achata o dicionário para formato de linha
        item_achatado['Ano'] = item_achatado.get('Ano', 'Desconhecido')  # Adiciona o ano ao item
        linhas_para_inserir.append(list(item_achatado.values()))  # Adiciona a linha à lista

    # Envia os dados em lotes para evitar exceder o limite de requisições
    batch_size = 1000  # Define o tamanho do lote
    try:
        total_linhas = len(linhas_para_inserir)  # Total de linhas a serem enviadas
        print(f"Iniciando envio de {total_linhas} linhas em lotes de {batch_size}...")

        for i in range(0, total_linhas, batch_size):
            lote = linhas_para_inserir[i:i + batch_size]  # Cria um lote de linhas
            sheet.append_rows(lote, value_input_option='RAW')  # Adiciona o lote à planilha
            print(f"Lote {i // batch_size + 1} enviado: {len(lote)} linhas")
            time.sleep(5)  # Pausa para evitar exceder o limite de requisições

        print("Dados enviados com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")  # Mensagem de erro se ocorrer algum problema durante o envio

def main():
    anos = range(2010, 2021)  # Define o intervalo de anos
    todos_dados = []

    for ano in anos:
        url_api = f'https://apisidra.ibge.gov.br/values/t/5938/n6/all/p/{ano}/v/37'  # Cria a URL da API para cada ano
        dados_pib = coletar_dados_api(url_api)  # Coleta os dados da API

        if not dados_pib:
            print(f"Não foi possível obter dados do PIB para o ano {ano}.")  # Mensagem se não for possível obter dados
            continue

        print(f"Encontrados {len(dados_pib) - 1} registros de PIB para o ano {ano}.")  # Mensagem com o número de registros

        # Adiciona o ano aos dados
        for item in dados_pib[1:]:
            item['Ano'] = ano

        todos_dados.extend(dados_pib[1:])  # Adiciona os dados ao total

        # Atraso para não sobrecarregar o servidor
        time.sleep(5)

    # Processa e envia os dados para o Google Sheets
    enviar_para_google_sheets(todos_dados, 'BD_PIB_MUNICIPIOS')

if __name__ == "__main__":
    main()
