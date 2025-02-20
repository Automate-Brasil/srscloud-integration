# 📌 Exemplos de Uso da API SRS

Este documento contém exemplos práticos de como interagir com a API SRS usando Python. Os exemplos cobrem autenticação, execução de processos, gerenciamento de filas, extração de relatórios e envio de notificações.

---

## 🔹 **Iniciar Execução**
```python
url = "https://<srs-dominio>/api/execucao/iniciar"
payload = {
    "Token": "XXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Workflow": "P28",
    "Tarefa": "",
    "NomeMaquina": "SA210-TEC"
}
response = requests.post(url, data=payload)
print(response.json())
```

---

## 🔹 **Registrar Logs**
```python
def registrar_log(execucaoId, mensagem):
    url = "https://<srs-dominio>/api/execucao/log"
    payload = {
        "Token": "XXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "ExecucaoId": execucaoId,
        "StatusId": 2,
        "Descricao": mensagem
    }
    response = requests.post(url, json=payload)
    return response.json()

execucao_id = "5aa2bbfa-bbc2-4530-8ebd-d2df63623b4b"
registrar_log(execucao_id, "Processo iniciado com sucesso")
```

---

## 🔹 **Inserir Tarefa na Fila**
```python
url = "https://<srs-dominio>/api/fila/inserir"
payload = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Workflow": "relatorios",
    "Tarefa": "atividade",
    "Referencia": "Execucao_Mensal",
    "ParametrosEntrada": {"DataInicio": "2024-12-01", "DataFim": "2025-01-01"}
}
response = requests.post(url, data=payload)
print(response.json())
```

## 🔹 **Obter Próxima Tarefa**
```python
url = "https://<srs-dominio>/api/fila/proximo"
payload = {"Token": TOKEN}
response = requests.get(url, data=payload)
print(response.json())
```

---

## 🔹 **Gerar Relatório de Atividades**
```python
url = "https://<srs-dominio>/api/relatorio/relatorio_atividade"
payload = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "DataInicio": "2024-12-01",
    "DataFim": "2025-01-01",
    "Workflow": "P28",
    "Pagina": 0,
    "Limite": 1000
}
response = requests.post(url, data=payload)
print(response.json())
```

---

## 🔹 **Finalizar Execução**
```python
url = "https://<srs-dominio>/api/execucao/finalizar"
payload = {
    "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "ExecucaoId": "5aa2bbfa-bbc2-4530-8ebd-d2df63623b4b",
    "Status": "Ok",
    "Descricao": "Execução concluída"
}
response = requests.post(url, data=payload)
print(response.json())
```

---

Estes exemplos cobrem os principais fluxos de uso da API SRS.