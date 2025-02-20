# 📍 Endpoints da API SRS

## 🔹 `/api/execucao/iniciar` (POST)<a id="iniciar-execucao"></a>
- **Descrição:** Inicia um novo processo de execução.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `Usuario` (objeto JSON, obrigatório) - Informações do usuário que inicia a execução:
        - `UsuarioId` (string, obrigatório)
        - `NomeUsuario` (string, obrigatório)
        - `EmailUsuario` (string, opcional)
        - `PerfilId` (string, obrigatório)
    - `ExecucaoId` (string, opcional) - Identificador da execução (caso já exista).
    - `Workflow` (string, obrigatório) - Nome do workflow associado à execução.
    - `Tarefa` (string, obrigatório) - Nome da tarefa a ser executada.
    - `NomeMaquina` (string, obrigatório) - Nome da máquina onde a execução será iniciada.
    - `Funcao` (string, opcional, padrão: `''`) - Função executada.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada.

- **JSON de Exemplo:**

```json
  {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "EmpresaId": "empresa_001",
    "Usuario": {
        "UsuarioId": "usr_123",
        "NomeUsuario": "João Silva",
        "EmailUsuario": "joao.silva@email.com",
        "PerfilId": "admin"
    },
    "Workflow": "processo_geral",
    "Tarefa": "tarefa_001",
    "NomeMaquina": "Servidor_01",
    "Funcao": "IniciarProcesso",
    "LinhaComando": 10
  }
```

  - **Resposta de Sucesso:**

```json
{
  "status": "sucesso",
  "execucao_id": "12345",
  "Parametros": { 
    "param1": "valor1", 
    "param2": "valor2" 
  }
}
```

  - **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `401`: Máquina não autorizada.
    - `404`: Workflow ou tarefa não encontrados.

---

## 🔹 `/api/execucao/log` (POST)<a id="registrar-log"></a>
- **Descrição:** Registra logs da execução.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `ExecucaoId` (string, obrigatório) - Identificador da execução.
    - `Descricao` (string, obrigatório) - Mensagem do log.
    - `Status` (string, opcional, padrão: `'Log'`) - Tipo do log (`Log`, `Alerta`, etc.).
    - `Funcao` (string, opcional, padrão: `''`) - Função associada ao log.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada ao log.
    - `Arquivo` (arquivo binário, opcional) - Arquivo a ser anexado ao log.
- **Exemplo de Requisição:**

```json
{
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "EmpresaId": "empresa_001",
  "ExecucaoId": "exec_56789",
  "Descricao": "Processo iniciado com sucesso.",
  "Status": "Log",
  "Funcao": "RegistrarEvento",
  "LinhaComando": 20
}
```

  - **Resposta de Sucesso:**

```json
{
  "status": "sucesso"
}
```

  - **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Execução não encontrada.

---

## 🔹 `/api/execucao/finalizar` (POST)<a id="finalizar-execucao"></a>
- **Descrição:** Finaliza uma execução em andamento.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `ExecucaoId` (string, obrigatório) - Identificador da execução.
    - `Status` (string, obrigatório) - Status final da execução (`Ok` ou `Erro`).
    - `Descricao` (string, opcional, padrão: `'Execucao finalizada'`) - Mensagem descritiva do encerramento.
    - `Funcao` (string, opcional, padrão: `''`) - Função associada ao encerramento.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada ao encerramento.
- **Exemplo de Requisição:**

```json
{
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "EmpresaId": "empresa_001",
  "ExecucaoId": "exec_56789",
  "Status": "Ok",
  "Descricao": "Processo finalizado com êxito.",
  "Funcao": "FinalizarProcesso",
  "LinhaComando": 30
}
```  

  - **Resposta de Sucesso:**

```json
{
  "status": "finalizado"
}
```

  - **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Execução não encontrada.
    - `409`: Execução já finalizada.

---

## 🔹 `/api/fila/inserir` (POST)<a id="inserir-tarefa"></a>
- **Descrição:** Insere uma nova tarefa na fila.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `Usuario` (objeto JSON, obrigatório) - Informações do usuário:
        - `UsuarioId` (string, obrigatório)
        - `NomeUsuario` (string, obrigatório)
        - `EmailUsuario` (string, opcional)
        - `PerfilId` (string, obrigatório)
    - `ExecucaoId` (string, opcional) - Identificador da execução associada à fila.
    - `Workflow` (string, obrigatório) - Nome do workflow associado à fila.
    - `Tarefa` (string, obrigatório) - Nome da tarefa da fila.
    - `Referencia` (string, obrigatório) - Referência da tarefa.
    - `ParametrosEntrada` (objeto JSON, obrigatório) - Parâmetros da tarefa.
    - `Status` (string, opcional, padrão: `'NaFila'`) - Status inicial da tarefa na fila (`NaFila`, `EmExecucao`).
    - `Mensagem` (string, opcional, padrão: `''`) - Mensagem associada à inserção da fila.
    - `Funcao` (string, opcional, padrão: `''`) - Função associada à inserção.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada à inserção.
    - `Lote` (lista de objetos JSON, opcional) - Lista de tarefas para inserção em lote:
```json
    [
      {
        "Referencia": "valor",
        "ParametrosEntrada": {
          "param1": "valor1",
          "param2": "valor2"
        }
      }
    ]
```

- **Resposta de Sucesso:**

```json
{
  "status": "sucesso",
  "FilaId": "12345"
}
```

- **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Workflow ou tarefa não encontrados.

---

## 🔹 `/api/fila/proximo` (GET)<a id="proxima-tarefa"></a>
- **Descrição:** Retorna a próxima tarefa da fila.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `ExecucaoId` (string, obrigatório) - Identificador da execução que está requisitando a tarefa.
    - `Lote` (int, opcional, padrão: `1`) - Quantidade de tarefas a serem retornadas.
    - `FilaId` (string, opcional) - Identificador específico da fila a ser recuperada.
    - `Funcao` (string, opcional, padrão: `''`) - Função associada à requisição.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada à requisição.
- **Resposta de Sucesso:**

```json
{
  "status": "sucesso",
  "Fila": 
    [
      {
        "FilaId": "12345",
        "Referencia": "valor",
        "ParametrosEntrada": {
          "param1": "valor1"
        }
      }
    ]
}
```

- **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Nenhuma tarefa disponível.

---

## 🔹 `/api/fila/atualizar` (POST)<a id="atualizar-tarefa"></a>
- **Descrição:** Atualiza o status de uma tarefa na fila.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `ExecucaoId` (string, obrigatório) - Identificador da execução associada à fila.
    - `FilaId` (string, obrigatório se não for um lote) - Identificador da fila.
    - `Status` (string, obrigatório) - Novo status da fila (`FilaOk`, `FilaErro`, `NaFila`, `EmExecucao`).
    - `ParametrosSaida` (objeto JSON, opcional) - Parâmetros resultantes da execução.
    - `Mensagem` (string, opcional) - Mensagem associada à atualização.
    - `Funcao` (string, opcional, padrão: `''`) - Função associada à atualização.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada à atualização.
    - `Lote` (lista de objetos JSON, opcional) - Lista de atualizações para múltiplas filas:
```json
    [
      {
        "FilaId": "12345",
        "Status": "FilaOk",
        "ParametrosSaida": {
          "resultado": "sucesso"
        },
        "Mensagem": "Tarefa concluída."
      }
    ]
```
- **Resposta de Sucesso:**

```json
{
  "status": "sucesso",
  "Mensagem": "Atualização realizada com sucesso"
}
```

- **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Tarefa não encontrada.

---

## 🔹 `/api/fila/consultar` (GET)<a id="consultar-fila)"></a>
- **Descrição:** Consulta o estado atual da fila.
- **Parâmetros (JSON):**
    - `Token` (string, obrigatório) - Token de autenticação.
    - `EmpresaId` (string, obrigatório) - Identificador da empresa.
    - `ExecucaoId` (string, obrigatório) - Identificador da execução associada à fila.
    - `Workflow` (string, obrigatório) - Nome do workflow da tarefa.
    - `Tarefa` (string, obrigatório) - Nome da tarefa.
    - `Criterios` (objeto JSON, obrigatório) - Critérios de busca no formato MongoDB:

        - ```json
          [
            {
              "StatusId": { "$eq": 1 }
            }
          ]
          ```

    - `OrderBy` (string, opcional) - Campo para ordenação.
    - `Limite` (int, opcional, padrão: `100`) - Número máximo de resultados (máximo permitido: 100).
    - `Funcao` (string, opcional, padrão: `''`) - Função associada à consulta.
    - `LinhaComando` (int, opcional, padrão: `0`) - Linha de comando associada à consulta.

- **Resposta de Sucesso:**

```json
{
  "status": "sucesso",
  "Fila": [
    {
      "FilaId": "12345",
      "Status": "EmExecucao",
      "Referencia": "valor"
    }
  ]
}
```

- **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `404`: Nenhuma tarefa encontrada.

---

## 🔹 `/api/credencial/obter`  (GET)<a id="obter-credencial"></a>
- **Descrição:** Obtém as credenciais de um usuário autorizado.

- **Parâmetros de Entrada**

    | Nome       | Tipo   | Obrigatório | Descrição |
    |------------|--------|------------|-----------|
    | `Token`    | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `Usuario`  | string | ✅ Sim      | Identificação do usuário para o qual as credenciais serão recuperadas. |
    | `Sistema`  | string | ✅ Sim      | Nome do sistema ao qual a credencial pertence. |

- **Exemplo de Resposta**
```json
{
  "status": "sucesso",
  "credencial": {
    "Usuario": "usuario_001",
    "Sistema": "sistema_x",
    "Login": "usuario_x",
    "Senha": "********",
    "ExpiraEm": "2025-12-31"
  }
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `404`  | `Credencial não encontrada` | O usuário ou sistema informado não possui credenciais cadastradas. |

---

## **🔹 `/api/credencial/atualizar`**  (POST)<a id="atualizar-credencial"></a>
- **Descrição:** Atualiza a credencial de um usuário autorizado.

- **Parâmetros de Entrada**

    | Nome       | Tipo   | Obrigatório | Descrição |
    |------------|--------|------------|-----------|
    | `Token`    | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `Usuario`  | string | ✅ Sim      | Identificação do usuário cuja credencial será atualizada. |
    | `Sistema`  | string | ✅ Sim      | Nome do sistema ao qual a credencial pertence. |
    | `NovaSenha`| string | ✅ Sim      | Nova senha a ser definida para o usuário. |

- **JSON de Exemplo**
```json
{
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "Usuario": "usuario_001",
  "Sistema": "sistema_x",
  "NovaSenha": "nova_senha_segura"
}
```

- **Exemplo de Resposta**
```json
{
  "status": "sucesso",
  "mensagem": "Credencial atualizada com sucesso."
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário autenticado não tem permissão para alterar esta credencial. |
    | `400`  | `Requisição inválida` | Dados ausentes ou mal formatados na requisição. |

---

## **🔹 `/api/tarefa/executar`**  (POST)<a id="executar-tarefa"></a>
- **Descrição:** Inicia a execução de uma tarefa específica.

- **Parâmetros de Entrada**

      | Nome         | Tipo   | Obrigatório | Descrição |
    |-------------|--------|------------|-----------|
    | `Token`     | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `EmpresaId` | string | ✅ Sim      | Identificação da empresa. |
    | `Usuario`   | objeto | ✅ Sim      | Informações do usuário que está acionando a tarefa. |
    | `Workflow`  | string | ✅ Sim      | Nome do fluxo de trabalho vinculado à tarefa. |
    | `Tarefa`    | string | ✅ Sim      | Nome da tarefa a ser executada. |
    | `Maquina`   | string | ✅ Sim      | Nome do servidor/máquina onde a tarefa será executada. |
    | `FilaId`    | string | ❌ Não      | ID da fila de execução (se aplicável). |
    | `ExecucaoId`| string | ❌ Não      | ID de uma execução existente (caso a tarefa seja parte de um fluxo maior). |
    | `Funcao`    | string | ❌ Não      | Nome da função responsável pela execução. |
    | `LinhaComando` | int  | ❌ Não      | Número de referência de linha de comando. |

- **JSON de Exemplo**
```json
{
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "EmpresaId": "empresa_001",
  "Usuario": {
    "UsuarioId": "user_123",
    "NomeUsuario": "Renato",
    "EmailUsuario": "renato@email.com",
    "PerfilId": "admin"
  },
  "Workflow": "processo_financeiro",
  "Tarefa": "validar_pagamento",
  "Maquina": "Servidor_01",
  "FilaId": "fila_12345",
  "ExecucaoId": "exec_67890",
  "Funcao": "ExecutarValidacao",
  "LinhaComando": 10
}
```

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "Acionamento da tarefa validar_pagamento direcionado para a máquina Servidor_01 a partir da API webservice."
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário não tem permissão para executar a tarefa. |
    | `400`  | `Parâmetros inválidos` | Algum parâmetro essencial está ausente ou mal formatado. |

## **🔹 `/api/tarefa/parametro`**  (POST)<a id="obter-parametro"></a>
- **Descrição:** Atualiza um parâmetro de uma tarefa já cadastrada.

-  **Parâmetros de Entrada**

    | Nome         | Tipo   | Obrigatório | Descrição |
    |-------------|--------|------------|-----------|
    | `Token`     | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `EmpresaId` | string | ✅ Sim      | Identificação da empresa. |
    | `Usuario`   | objeto | ✅ Sim      | Informações do usuário que está realizando a atualização. |
    | `Workflow`  | string | ✅ Sim      | Nome do fluxo de trabalho vinculado à tarefa. |
    | `Tarefa`    | string | ✅ Sim      | Nome da tarefa a ser alterada. |
    | `Parametro` | string | ✅ Sim      | Nome do parâmetro que será atualizado. |
    | `Valor`     | string | ✅ Sim      | Novo valor para o parâmetro. |
    | `ExecucaoId`| string | ❌ Não      | ID da execução vinculada à alteração. |
    | `Funcao`    | string | ❌ Não      | Nome da função que está alterando o parâmetro. |
    | `LinhaComando` | int  | ❌ Não      | Número de referência de linha de comando. |

- **JSON de Exemplo**
```json
{
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "EmpresaId": "empresa_001",
  "Usuario": {
    "UsuarioId": "user_123",
    "NomeUsuario": "Renato",
    "PerfilId": "admin"
  },
  "Workflow": "processo_financeiro",
  "Tarefa": "validar_pagamento",
  "Parametro": "valor_minimo",
  "Valor": "5000",
  "ExecucaoId": "exec_67890",
  "Funcao": "AtualizarParametro",
  "LinhaComando": 12
}
```

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "Parâmetro 'valor_minimo' da tarefa 'validar_pagamento' foi atualizado para '5000'."
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário não tem permissão para alterar esse parâmetro. |
    | `400`  | `Parâmetro não autorizado` | O parâmetro informado não pode ser alterado via API. |

---

## 🔹 `/api/tela/abrir` (POST)<a id="abrir-tela"></a>
- **Descrição:** Envia um comando para abrir uma tela específica em uma máquina remota.

- **Parâmetros de Entrada**

    | Nome             | Tipo   | Obrigatório | Descrição |
    |-----------------|--------|------------|-----------|
    | `Token`         | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `EmpresaId`     | string | ✅ Sim      | Identificação da empresa. |
    | `UsuarioId`     | string | ✅ Sim      | Identificação do usuário que está solicitando a abertura da tela. |
    | `MaquinaServer` | string | ✅ Sim      | Nome da máquina que enviará o comando. |
    | `MaquinaClient` | string | ✅ Sim      | Nome da máquina onde a tela será aberta. |

- **Exemplo de Requisição em Python**

```python
import requests

url = "https://<srs-dominio>/api/tela/abrir"
payload = {
  "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "EmpresaId": "empresa_001", 
  "UsuarioId": "user_123",
  "MaquinaServer": "Servidor_01", 
  "MaquinaClient": "PC_Cliente_02"}

response = requests.post(url, data=payload)
print(response.json())
```

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "Ordem enviada para a máquina: (Servidor_01)!"
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário autenticado não tem permissão para abrir telas remotamente. |
    | `400`  | `Máquina não identificada` | Um ou ambos os parâmetros `MaquinaServer` e `MaquinaClient` não foram informados ou são inválidos. |
    | `404`  | `Máquina não encontrada` | A máquina informada não está ativa ou registrada no sistema. |
    | `500`  | `Erro interno` | Ocorreu um erro inesperado ao processar a solicitação. |

---

## 🔹 `/api/certificado/obter` (GET)<a id="obter-certificado"></a>

- **Descrição:** Obtém um certificado digital associado a um sistema específico.

- **Parâmetros de Entrada**

    | Nome               | Tipo   | Obrigatório | Descrição |
    |-------------------|--------|------------|-----------|
    | `Token`          | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `ExecucaoId`     | string | ✅ Sim      | ID da execução associada à requisição. |
    | `EmpresaId`      | string | ✅ Sim      | Identificação da empresa. |
    | `Sistema`        | string | ✅ Sim      | Nome do sistema ao qual o certificado pertence. |
    | `AliasCertificado` | string | ✅ Sim      | Nome do alias do certificado a ser obtido. |
    | `Funcao`         | string | ❌ Não      | Nome da função solicitante. |
    | `LinhaComando`   | int    | ❌ Não      | Número de referência de linha de comando. |

- **Exemplo de Requisição em Python**

```python
import requests

url = "https://<srs-dominio>/api/certificado/obter"
params = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "ExecucaoId": "exec_12345",
    "EmpresaId": "empresa_001",
    "Sistema": "sistema_x",
    "AliasCertificado": "cert_abc"
}
response = requests.get(url, params=params)
print(response.json())
```

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "Certificado cert_abc do sistema Sistema X concedido",
  "Sistema": {
    "NomeSistema": "Sistema X"
  },
  "Credencial": "Credencial de Segurança",
  "Certificado": "https://api.srs.com/downloads/cert_abc.pfx",
  "Acesso": {
    "login": "usuario_x",
    "senha": "********"
  }
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário autenticado não tem permissão para acessar este certificado. |
    | `404`  | `Certificado não encontrado` | O alias do certificado informado não existe ou não está disponível. |
    | `500`  | `Erro interno` | Ocorreu um erro inesperado ao processar a solicitação. |

---

## 🔹 `/api/notificacao/notificar` (POST)<a id="enviar-notificacao"></a>
- **Descrição:** Envia uma notificação para um ou mais usuários por diferentes canais. A API SRS permite enviar notificações para usuários via **WhatsApp, Teams, Email ou Portal**. 

- **Parâmetros de Entrada**

  | Nome          | Tipo   | Obrigatório | Descrição |
  |--------------|--------|------------|-----------|
  | `Token`      | string | ✅ Sim      | Token de autenticação para acessar a API. |
  | `ExecucaoId` | string | ✅ Sim      | ID da execução associada à notificação. |
  | `EmpresaId`  | string | ✅ Sim      | Identificação da empresa. |
  | `Assunto`    | string | ✅ Sim      | Assunto da notificação. |
  | `Mensagem`   | string | ✅ Sim      | Conteúdo da mensagem a ser enviada. |
  | `Canal`      | lista  | ✅ Sim      | Canais de envio (`Whatsapp`, `Teams`, `Email`, `Portal`). |
  | `Destino`    | lista  | ✅ Sim      | Lista de destinatários (`UsuarioId` ou `Token`). |
  | `Confidencial` | int  | ❌ Não      | Define se a mensagem é confidencial (`0` = Não, `1` = Sim). |

- **Exemplo de Requisição em Python**

```python
import requests

url = "https://<srs-dominio>/api/notificacao/notificar"
payload = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "ExecucaoId": "exec_12345",
    "EmpresaId": "empresa_001",
    "Assunto": "Atualização do Sistema",
    "Mensagem": "O sistema será atualizado hoje às 23h.",
    "Canal": ["Email", "Teams"],
    "Destino": [{"UsuarioId": "user_123"}, {"Token": "abcd-efgh-ijkl"}],
    "Confidencial": 1
}

response = requests.post(url, data=payload)
print(response.json())
```


- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "Enviado com sucesso.",
  "Erro": []
}
```

- **Possíveis Erros**

    | Código | Mensagem | Descrição |
    |--------|---------|-----------|
    | `401`  | `Unauthorized` | Token ausente ou inválido. |
    | `403`  | `Acesso negado` | O usuário autenticado não tem permissão para enviar notificações. |
    | `400`  | `Parâmetros inválidos` | Algum parâmetro essencial está ausente ou mal formatado. |
    | `404`  | `Usuário não encontrado` | Nenhum usuário válido foi identificado nos destinatários. |

---

## 🔹 `/api/relatorio/relatorio_atividade` (GET)<a id="relatorio-atividade"></a>
- **Descrição:** Gera um relatório das atividades executadas dentro de um período.

- **Parâmetros de Entrada**

  | Nome         | Tipo   | Obrigatório | Descrição |
  |-------------|--------|------------|-----------|
  | `Token`     | string | ✅ Sim      | Token de autenticação para acessar a API. |
  | `EmpresaId` | string | ✅ Sim      | Identificação da empresa. |
  | `DataInicio`| string | ✅ Sim      | Data de início (formato `YYYY-MM-DD`). |
  | `DataFim`   | string | ✅ Sim      | Data de fim (formato `YYYY-MM-DD`). |
  | `Pagina`    | int    | ❌ Não      | Número da página de resultados. |
  | `Limite`    | int    | ❌ Não      | Número máximo de registros por página (padrão: `1000`). |
  | `StatusId`  | int    | ❌ Não      | ID do status da atividade. |
  | `Workflow`  | string | ❌ Não      | Nome do workflow a ser filtrado. |
  | `Tarefa`    | string | ❌ Não      | Nome da tarefa específica. |

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Pagina": 0,
  "Limite": 1000,
  "Mensagem": "",
  "Dados": [
    {
      "FilaId": "12345",
      "StatusId": 1,
      "StatusAlias": "Concluído",
      "Referencia": "Tarefa A",
      "DataInclusao": "2025-01-10 14:30:00",
      "DataInicioExecucao": "2025-01-10 14:35:00",
      "DataFimExecucao": "2025-01-10 14:50:00",
      "TempoExecucao": 15.0
    }
  ]
}
```

## 🔹 `/api/relatorio/relatorio_auditoria` (GET)<a id="relatorio-auditoria"></a>
- **Descrição:** Gera um relatório de auditoria de ações realizadas pelos usuários.

-  **Parâmetros de Entrada**

    | Nome          | Tipo   | Obrigatório | Descrição |
    |--------------|--------|------------|-----------|
    | `Token`      | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `EmpresaId`  | string | ✅ Sim      | Identificação da empresa. |
    | `DataInicio` | string | ✅ Sim      | Data de início (`YYYY-MM-DD`). |
    | `DataFim`    | string | ✅ Sim      | Data de fim (`YYYY-MM-DD`). |
    | `EmailUsuario` | string | ❌ Não      | Filtrar auditoria por e-mail do usuário. |

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "",
  "Dados": [
    {
      "Data": "2025-01-15 10:30:00",
      "UsuarioId": "user_123",
      "NomeUsuario": "Renato",
      "EmailUsuario": "renato@email.com",
      "Acao": "Alteração de credenciais",
      "Detalhes": "Usuário alterou credencial de acesso ao sistema."
    }
  ]
}
```

## 🔹 `/api/relatorio/relatorio_sistema` (GET)<a id="relatorio-sistema"></a>
- **Descrição:** Retorna informações detalhadas sobre os sistemas integrados.

- **Exemplo de Requisição em Python**

```python
import requests

url = "https://<srs-dominio>/api/relatorio/relatorio_atividade"
params = {
    "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "EmpresaId": "empresa_001",
    "DataInicio": "2025-01-01",
    "DataFim": "2025-01-31"
}

response = requests.get(url, params=params)
print(response.json())
```

## 🔹 `/api/relatorio/relatorio_execucao` (GET)<a id="relatorio-execucao"></a>
- **Descrição:** Retorna um relatório detalhado sobre as execuções de tarefas dentro de um período.

- **Parâmetros de Entrada**

  | Nome         | Tipo   | Obrigatório | Descrição |
  |-------------|--------|------------|-----------|
  | `Token`     | string | ✅ Sim      | Token de autenticação para acessar a API. |
  | `EmpresaId` | string | ✅ Sim      | Identificação da empresa. |
  | `DataInicio`| string | ✅ Sim      | Data de início do relatório (`YYYY-MM-DD`). |
  | `DataFim`   | string | ✅ Sim      | Data de fim do relatório (`YYYY-MM-DD`). |
  | `Pagina`    | int    | ❌ Não      | Número da página para paginação. |
  | `Limite`    | int    | ❌ Não      | Número máximo de registros por página (padrão: `1000`). |
  | `StatusId`  | int    | ❌ Não      | Filtrar execuções por status específico. |
  | `Workflow`  | string | ❌ Não      | Filtrar execuções por workflow. |
  | `Tarefa`    | string | ❌ Não      | Filtrar execuções por nome da tarefa. |

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Pagina": 0,
  "Limite": 1000,
  "Mensagem": "",
  "Dados": [
    {
      "ExecucaoId": "exec_12345",
      "Workflow": "processo_financeiro",
      "Tarefa": "validar_pagamento",
      "Status": "Concluído",
      "DataInicioExecucao": "2025-01-10 14:35:00",
      "DataFimExecucao": "2025-01-10 14:50:00",
      "TempoExecucao": 15.0,
      "Maquina": "Servidor_01",
      "Usuario": {
        "UsuarioId": "user_123",
        "NomeUsuario": "Renato",
        "EmailUsuario": "renato@email.com"
      }
    }
  ]
}
```

- **Possíveis Erros**

| Código | Mensagem | Descrição |
|--------|---------|-----------|
| `401`  | `Unauthorized` | Token ausente ou inválido. |
| `403`  | `Acesso negado` | O usuário autenticado não tem permissão para acessar este relatório. |
| `400`  | `Parâmetros inválidos` | Algum parâmetro essencial está ausente ou mal formatado. |
| `404`  | `Nenhuma execução encontrada` | Não há registros dentro do período solicitado. |


## 🔹 `/api/relatorio/relatorio_maquina` (GET)<a id="relatorio-maquina"></a>
**Descrição:** Retorna um relatório detalhado sobre o uso de máquinas no ambiente de execução.

- **Parâmetros de Entrada**

    | Nome         | Tipo   | Obrigatório | Descrição |
    |-------------|--------|------------|-----------|
    | `Token`     | string | ✅ Sim      | Token de autenticação para acessar a API. |
    | `EmpresaId` | string | ✅ Sim      | Identificação da empresa. |
    | `DataInicio`| string | ✅ Sim      | Data de início (`YYYY-MM-DD`). |
    | `DataFim`   | string | ✅ Sim      | Data de fim (`YYYY-MM-DD`). |
    | `Maquina`   | string | ❌ Não      | Nome de uma máquina específica para filtrar o relatório. |

- **Exemplo de Requisição em Python**

```python
import requests

url = "https://<srs-dominio>/api/relatorio/relatorio_execucao"
params = {
   "Token": "Xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "EmpresaId": "empresa_001",
    "DataInicio": "2025-01-01",
    "DataFim": "2025-01-31"
}

response = requests.get(url, params=params)
print(response.json())
```

- **Exemplo de Resposta**
```json
{
  "Autorizado": true,
  "Mensagem": "",
  "Dados": [
    {
      "Maquina": "Servidor_01",
      "TotalTarefasExecutadas": 150,
      "TempoTotalExecucao": 480.5,
      "Status": "Ativa",
      "UltimaExecucao": "2025-01-29 18:45:00"
    },
    {
      "Maquina": "PC_Cliente_02",
      "TotalTarefasExecutadas": 45,
      "TempoTotalExecucao": 125.0,
      "Status": "Ociosa",
      "UltimaExecucao": "2025-01-25 15:30:00"
    }
  ]
}
```

- **Possíveis Erros**

  | Código | Mensagem | Descrição |
  |--------|---------|-----------|
  | `401`  | `Unauthorized` | Token ausente ou inválido. |
  | `403`  | `Acesso negado` | O usuário autenticado não tem permissão para acessar este relatório. |
  | `400`  | `Parâmetros inválidos` | Algum parâmetro essencial está ausente ou mal formatado. |
  | `404`  | `Nenhuma máquina encontrada` | Não há registros de máquinas dentro do período solicitado. |