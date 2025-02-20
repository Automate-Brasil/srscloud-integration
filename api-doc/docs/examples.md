# 📌 Exemplos de Uso da API SRS

Este documento contém exemplos práticos de como interagir com a API SRS usando Python. Os exemplos cobrem autenticação, execução de processos, gerenciamento de filas, extração de relatórios e envio de notificações.

---

## 🔹 **Autenticação e Configuração Inicial**
Antes de fazer qualquer requisição, configure o token de autenticação.

```python
import requests

TOKEN = "EID128d4c452d8c4be3ba3c01548c024082_b0cfefce-79b8-4301-92a9-3a106c153793"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
```

---

## 🔹 **Iniciar Execução**
```python
url = "https://<srs-dominio>/api/execucao/iniciar"
payload = {
    "Token": TOKEN,
    "Workflow": "P28",
    "Tarefa": "",
    "NomeMaquina": "SA210-TEC"
}
response = requests.post(url, json=payload, headers=HEADERS)
print(response.json())
```

---

## 🔹 **Registrar Logs**
```python
def registrar_log(execucaoId, mensagem):
    url = "https://<srs-dominio>/api/execucao/log"
    payload = {
        "Token": TOKEN,
        "ExecucaoId": execucaoId,
        "StatusId": 2,
        "Descricao": mensagem
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

execucao_id = "5aa2bbfa-bbc2-4530-8ebd-d2df63623b4b"
registrar_log(execucao_id, "Processo iniciado com sucesso")
```

---

## 🔹 **Gerenciar Filas**
### **Inserir Tarefa na Fila**
```python
url = "https://<srs-dominio>/api/fila/inserir"
payload = {
    "Token": TOKEN,
    "Workflow": "relatorios",
    "Tarefa": "atividade",
    "Referencia": "Execucao_Mensal",
    "ParametrosEntrada": {"DataInicio": "2024-12-01", "DataFim": "2025-01-01"}
}
response = requests.post(url, json=payload, headers=HEADERS)
print(response.json())
```

### **Obter Próxima Tarefa**
```python
url = "https://<srs-dominio>/api/fila/proximo"
payload = {"Token": TOKEN}
response = requests.get(url, json=payload, headers=HEADERS)
print(response.json())
```

---

## 🔹 **Gerar Relatório de Atividades**
```python
url = "https://<srs-dominio>/api/relatorio/relatorio_atividade"
payload = {
    "Token": TOKEN,
    "DataInicio": "2024-12-01",
    "DataFim": "2025-01-01",
    "Workflow": "P28",
    "Pagina": 0,
    "Limite": 1000
}
response = requests.post(url, json=payload, headers=HEADERS)
print(response.json())
```

---

## 🔹 **Finalizar Execução**
```python
url = "https://<srs-dominio>/api/execucao/finalizar"
payload = {
    "Token": TOKEN,
    "ExecucaoId": "5aa2bbfa-bbc2-4530-8ebd-d2df63623b4b",
    "Status": "Ok",
    "Descricao": "Execução concluída"
}
response = requests.post(url, json=payload, headers=HEADERS)
print(response.json())
```

---

Estes exemplos cobrem os principais fluxos de uso da API SRS.