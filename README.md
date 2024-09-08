# Coleta de Dados PIB Municípios SP

Este projeto coleta dados do PIB dos municípios de São Paulo usando a API do IBGE e os envia para uma planilha no Google Sheets utilizando a API do Google Cloud.

## Índice
1. [Configuração do Google Cloud API](#configuração-do-google-cloud-api)
2. [Configuração do Código Python](#configuração-do-código-python)
3. [Execução do Código](#execução-do-código)
4. [Estrutura do Código](#estrutura-do-código)
5. [Notas Adicionais](#notas-adicionais)

## 1. Configuração do Google Cloud API

### 1.1 Criar um Projeto no Google Cloud Platform
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Clique em **Selecionar um Projeto** e depois em **Novo Projeto**.
3. Dê um nome ao projeto e clique em **Criar**.

### 1.2 Ativar as APIs Google Sheets e Google Drive
1. No painel do projeto, vá para **APIs e Serviços** > **Biblioteca**.
2. Pesquise por **Google Sheets API** e **Google Drive API**, e ative ambas.

### 1.3 Criar Credenciais
1. Vá para **APIs e Serviços** > **Credenciais**.
2. Clique em **Criar Credenciais** e selecione **Conta de Serviço**.
3. Preencha as informações da conta de serviço e clique em **Criar**.
4. No próximo passo, você pode definir permissões para a conta, mas o padrão geralmente é suficiente.
5. Após criar a conta, clique em **Concluído** e vá para a lista de contas de serviço.
6. Encontre a conta criada, clique nela, e depois em **Adicionar Chave** > **JSON**. Isso fará o download de um arquivo `.json` com suas credenciais. Renomeie esse arquivo para `credenciais_google_sheets.json`.

### 1.4 Compartilhar a Planilha com a Conta de Serviço
1. Abra a planilha Google Sheets que você deseja usar.
2. Clique no botão **Compartilhar** e adicione o e-mail da conta de serviço (encontrado no arquivo JSON baixado) com permissão de edição.

## 2. Configuração do Código Python

### 2.1 Instalar Dependências
Certifique-se de que as bibliotecas necessárias estão instaladas. Você pode instalá-las usando o seguinte comando:

```bash
pip install requests gspread oauth2client
```

### 2.2 Atualizar o Código
Certifique-se de que o nome do arquivo JSON no código Python corresponde ao nome do arquivo JSON que você baixou:

### 2.3 Estrutura do Código
O código Python realiza as seguintes tarefas:
1. Coleta Dados da API: Faz requisições à API do IBGE para obter dados do PIB dos municípios de São Paulo para os anos de 2010 a 2021.
2. Processa os Dados: Trata e formata os dados coletados, adicionando o ano aos registros.
3. Envia para o Google Sheets: Usa a API do Google Sheets para inserir os dados em uma planilha, enviando em lotes para evitar problemas de quota.

## 3. Execução do Código
Para executar o código Python, use o seguinte comando:

```bash
python seu_script.py
```

Substitua seu_script.py pelo nome do arquivo Python que contém o código.

## 4. Estrutura do Código
1. Função coletar_dados_api(url): Faz uma requisição à API do IBGE e retorna os dados no formato JSON.
2. Função achatar_dicionario(d, prefixo=''): Achata dicionários aninhados para um formato mais simples.
3. Função enviar_para_google_sheets(dados, nome_planilha): Envia os dados processados para uma planilha do Google Sheets.
4. Função main(): Controla o fluxo principal do código, coletando dados para cada ano e enviando-os para o Google Sheets.

## 5. Notas Adicionais
* Quota da API do Google Sheets: Certifique-se de respeitar os limites de quota para evitar erros de quota.
* Atrasos entre requisições: O código inclui atrasos entre as requisições para evitar sobrecarregar o servidor da API.

