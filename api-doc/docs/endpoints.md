# 📍 Endpoints da API SRS

## 🔹 `/api/execucao/iniciar` (POST)
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
- **Exemplo de Requisição:**

    ```json
    {
    "Token": "abc123xyz",
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
        "param2": "valor2" }
    }
    ```

  - **Possíveis Erros:**
    - `400`: Requisição inválida.
    - `403`: Token inválido.
    - `401`: Máquina não autorizada.
    - `404`: Workflow ou tarefa não encontrados.

---

## 🔹 `/api/execucao/log` (POST)
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
    "Token": "abc123xyz",
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

## 🔹 `/api/execucao/finalizar` (POST)
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
    "Token": "abc123xyz",
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

## 🔹 `/api/fila/inserir` (POST)
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
        - ```json
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

## 🔹 `/api/fila/proximo` (GET)
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
        "Fila": [
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

## 🔹 `/api/fila/atualizar` (POST)
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
        - ```json
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

## 🔹 `/api/fila/consultar` (GET)
- **Descrição:** Consulta o estado atual da fila.
- **Parâmetros (JSON):**
  - `Token` (string, obrigatório) - Token de autenticação.
  - `EmpresaId` (string, obrigatório) - Identificador da empresa.
  - `ExecucaoId` (string, obrigatório) - Identificador da execução associada à fila.
  - `Workflow` (string, obrigatório) - Nome do workflow da tarefa.
  - `Tarefa` (string, obrigatório) - Nome da tarefa.
  - `Criterios` (objeto JSON, obrigatório) - Critérios de busca no formato MongoDB:
    ```json
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

## 🔹 `/api/credencial/obter` (GET)
- **Descrição:** Obtém credenciais de um usuário.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/credencial/atualizar` (POST)
- **Descrição:** Atualiza credenciais de um usuário.
- **Parâmetros:**
  - `Token` (string, obrigatório)
  - `Usuario` (string, obrigatório)
  - `NovaSenha` (string, obrigatório)

## 🔹 `/api/tarefa/parametro` (GET)
- **Descrição:** Obtém parâmetros de uma tarefa.
- **Parâmetros:**
  - `Token` (string, obrigatório)
  - `TarefaID` (int, obrigatório)

## 🔹 `/api/tarefa/executar` (POST)
- **Descrição:** Executa uma tarefa específica.
- **Parâmetros:**
  - `Token` (string, obrigatório)
  - `TarefaID` (int, obrigatório)

## 🔹 `/api/tela/abrir` (POST)
- **Descrição:** Abre uma interface específica.
- **Parâmetros:**
  - `Token` (string, obrigatório)
  - `Tela` (string, obrigatório)

## 🔹 `/api/certificado/obter` (GET)
- **Descrição:** Obtém informações de um certificado.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/notificacao/notificar` (POST)
- **Descrição:** Envia uma notificação para um usuário.
- **Parâmetros:**
  - `Token` (string, obrigatório)
  - `Mensagem` (string, obrigatório)

## 🔹 `/api/relatorio/relatorio_atividade` (GET)
- **Descrição:** Gera um relatório de atividades.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/relatorio/relatorio_auditoria` (GET)
- **Descrição:** Gera um relatório de auditoria.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/relatorio/relatorio_maquina` (GET)
- **Descrição:** Gera um relatório de máquinas.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/relatorio/relatorio_sistema` (GET)
- **Descrição:** Gera um relatório do sistema.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/relatorio/relatorio_execucao` (GET)
- **Descrição:** Gera um relatório de execuções.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/interno/finaliza_execucao` (POST)
- **Descrição:** Finaliza uma execução interna.
- **Parâmetros:**
  - `Token` (string, obrigatório)

## 🔹 `/api/interno/cria_execucao` (POST)
- **Descrição:** Cria uma nova execução interna.
- **Parâmetros:**
  - `Token` (string, obrigatório)
