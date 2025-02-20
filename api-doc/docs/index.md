# 📘 Documentação da API SRS

Bem-vindo à documentação oficial da **API SRS**! Aqui você encontrará informações detalhadas sobre os endpoints, autenticação e exemplos de requisições.

## 🔹 Visão Geral
A API SRS fornece endpoints organizados por categorias, permitindo a interação com diferentes serviços, como execução de tarefas, gerenciamento de filas, autenticação, notificações e geração de relatórios.

### **📍 Estrutura dos Endpoints**
Os endpoints seguem o seguinte padrão:

```
/api/<tipo>/<acao>
```

Onde:
- **`tipo`** define a categoria do serviço (ex: `execucao`, `fila`, `credencial`, etc.).
- **`acao`** define a operação a ser realizada dentro da categoria.

## 🚀 **Endpoints Disponíveis**

### 🔹 Execução de Processos
- [`/api/execucao/iniciar`](endpoints.md#iniciar-execucao) - Inicia um novo processo.
- [`/api/execucao/log`](endpoints.md#registrar-log) - Registra logs da execução.
- [`/api/execucao/finalizar`](endpoints.md#finalizar-execucao) - Finaliza um processo.

### 🔹 Gerenciamento de Filas
- [`/api/fila/inserir`](endpoints.md#inserir-tarefa) - Insere uma nova tarefa na fila.
- [`/api/fila/proximo`](endpoints.md#proxima-tarefa) - Retorna a próxima tarefa da fila.
- [`/api/fila/atualizar`](endpoints.md#atualizar-tarefa) - Atualiza uma tarefa na fila.
- [`/api/fila/consultar`](endpoints.md#consultar-fila) - Consulta o estado atual da fila.

### 🔹 Autenticação e Credenciais
- [`/api/credencial/obter`](endpoints.md#obter-credencial) - Obtém credenciais de um usuário.
- [`/api/credencial/atualizar`](endpoints.md#atualizar-credencial) - Atualiza credenciais de um usuário.

### 🔹 Tarefas e Execução
- [`/api/tarefa/parametro`](endpoints.md#obter-parametro) - Obtém parâmetros de uma tarefa.
- [`/api/tarefa/executar`](endpoints.md#executar-tarefa) - Executa uma tarefa específica.

### 🔹 Ações em Telas
- [`/api/tela/abrir`](endpoints.md#abrir-tela) - Abre uma interface específica.

### 🔹 Certificados
- [`/api/certificado/obter`](endpoints.md#obter-certificado) - Obtém informações de um certificado.

### 🔹 Notificações
- [`/api/notificacao/notificar`](endpoints.md#enviar-notificacao) - Envia uma notificação para um usuário.

### 🔹 Relatórios
- [`/api/relatorio/relatorio_atividade`](endpoints.md#relatorio-atividade) - Relatório de atividades.
- [`/api/relatorio/relatorio_auditoria`](endpoints.md#relatorio-auditoria) - Relatório de auditoria.
- [`/api/relatorio/relatorio_maquina`](endpoints.md#relatorio-maquina) - Relatório de máquinas.
- [`/api/relatorio/relatorio_sistema`](endpoints.md#relatorio-sistema) - Relatório do sistema.
- [`/api/relatorio/relatorio_execucao`](endpoints.md#relatorio-execucao) - Relatório de execuções.

### 🔹 Funções Internas (Administração)
- [`/api/interno/finaliza_execucao`](endpoints.md#finalizar-execucao-interna) - Finaliza uma execução interna.
- [`/api/interno/cria_execucao`](endpoints.md#criar-execucao) - Cria uma nova execução interna.
- [`/api/interno/cria_fila`](endpoints.md#criar-fila) - Cria uma fila de execução.
- [`/api/interno/atualiza_fila`](endpoints.md#atualizar-fila-interna) - Atualiza uma fila interna.
- [`/api/interno/registra_log`](endpoints.md#registrar-log-interno) - Registra um log interno.
- [`/api/interno/executa_agendamento`](endpoints.md#executar-agendamento) - Executa um agendamento interno.
- [`/api/interno/realoca_fila`](endpoints.md#realocar-fila) - Realoca uma fila de processos.
- [`/api/interno/novo_cliente`](endpoints.md#novo-cliente) - Cadastra um novo cliente.
- [`/api/interno/atualiza_usuario`](endpoints.md#atualizar-usuario) - Atualiza dados de um usuário.
- [`/api/interno/atualiza_maquina`](endpoints.md#atualizar-maquina) - Atualiza informações de uma máquina.
- [`/api/interno/backup_empresa`](endpoints.md#backup-empresa) - Gera um backup da empresa.
- [`/api/interno/excluir_empresa`](endpoints.md#excluir-empresa) - Exclui uma empresa.

## 🔐 **Autenticação**
A API SRS exige autenticação via **Token** para acessar a maioria dos endpoints.

**Exemplo de cabeçalho HTTP:**
```sh
Authorization: Bearer SEU_TOKEN_AQUI
```

## 🎯 **Testando a API**
Para testar os endpoints, você pode utilizar ferramentas como:
- **Postman**
- **cURL**
- **Swagger UI** (se configurado)

**Exemplo de requisição via cURL:**
```sh
curl -X POST "http://localhost:8000/api/execucao/iniciar" \
     -H "Authorization: Bearer SEU_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"Parametros": {"chave": "valor"}}'
```

## 📚 **Mais Informações**
Para detalhes completos sobre cada endpoint, consulte a página [Endpoints](endpoints.md).
