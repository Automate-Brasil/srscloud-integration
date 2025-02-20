# 🔐 Autenticação na API SRS

A API SRS requer autenticação para a maioria dos seus endpoints. O acesso é controlado por meio de um **Token** que deve ser enviado no cabeçalho de cada requisição.

## Como Funciona a Autenticação
- O cliente deve fornecer um **Token de autenticação** válido.
- Se o token for inválido ou expirado, a API retornará um erro `403 - Não autorizado`.
- No **payload da requisição**, a chave deve ser enviada exatamente como **`Token`** (com `T` maiúsculo).

## **Usando Python (requests)**
```python
import requests

url = "https://<srs-dominio>/api/relatorio/relatorio_atividade"

payload = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "DataInicio": "2024-12-01",
    "DataFim": "2025-01-01",
    "Workflow": "P28",
    "Tarefa": "", # opcional
    "Limite": 1000, # 1000 é o máximo por página
    "Pagina": 0 # primeira página
}

response = requests.post(url, data=payload)
print(response.json())
```

## **Erros Comuns**
| Código HTTP | Motivo |
|------------|----------------------------------|
| `400` | Token ausente ou malformado |
| `403` | Token inválido ou expirado |
| `500` | Erro interno no servidor |

## **Obtenção de Token**
O token de autenticação pode ser obtido via perfil do usuário no SRS Cloud. 

Se precisar de mais informações sobre autenticação, consulte a equipe de desenvolvimento.

