import json, requests, inspect, base64, os, sys, time
from urllib3.util import parse_url, Url
from urllib.parse import quote
from datetime import datetime
import logging

__version__ = "2.5.1"

"""# Versão 2026.02.16"""

"""# Status válidos para execução
--- valores para StatusId ou Status voce pode usar um ou outro ---
        	   StatusId	Status	    Descricao
StatusExecucao	0	    Acionado	Execução criada e aguardando ser iniciada
StatusExecucao	1	    Inicio	    Inicio
StatusExecucao	2	    Log	        Log
StatusExecucao	3	    Alerta	    Alerta
StatusExecucao	4	    Ok	        Encerrado com Sucesso
StatusExecucao	5	    Erro	    Encerrado com Erro
"""

"""# Status válidos para fila
--- valores para StatusId ou Status voce pode usar um ou outro ---
           StatusID	Status	    Descricao
StatusFila	0	    NaFila	    Aguardando
StatusFila	1	    FilaExec	Em execução
StatusFila	2	    FilaOk	    Finalizado com Sucesso
StatusFila	3	    FilaErro	Finalizado com erro
"""


class JsonFormatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage().replace("\n", " ").replace("\r", " ")
        log_dict = {
            "timestamp": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
            "levelname": record.levelname,
            "filename": record.filename,
            "funcname": record.funcName,
            "lineno": record.lineno,
            "message": record.message,
        }
        return json.dumps(log_dict, ensure_ascii=False)
    
class TextFormatter(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage().replace("\n", " ").replace("\r", " ")
        log = f'{datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")}\t{record.levelname}\t{record.filename}\t{record.funcName}\t{record.lineno}\t{record.message}'
        return log

class SRS:
    # Funções de configuração
    def __init__(self, token:str, maquina:str, workflow:str, tarefa:str, url:str = 'https://api.srscloud.com.br/', 
                 logFile:str="DEBUG", logFormat="Text", execucaoId=False, filaId=False) -> None:
        self.url = url
        self.token = token
        self.workflow = workflow
        self.tarefa = tarefa
        self.maquina = maquina
        self.usarProxy = False
        self.logFile = logFile
        self.execucaoId = execucaoId
        self.filaId = filaId
        hoje = datetime.now().strftime("%Y-%m-%d")
        self.localLog = f'c:/Automate Brasil/log/{workflow}/{tarefa}/log_{hoje}.txt'

        # Configuração do log 
        handler = logging.StreamHandler()
        if logFormat.upper() == "JSON": 
            formatter = JsonFormatter()
        else:
            formatter = TextFormatter()
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        if self.logFile:
            if not os.path.isdir(os.path.dirname(self.localLog)): 
                print('criando pasta:', os.path.dirname(self.localLog))
                os.makedirs(os.path.dirname(self.localLog), exist_ok=True)

        file_handler = logging.FileHandler(self.localLog, encoding='utf-8')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.logFile.upper(), logging.DEBUG))
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

        try:
            arg1 = sys.argv[1] #recebe a ExecucaoId 
            if len(arg1) == 24: self.execucaoId = arg1
            logging.info(f'ExecucaoId recebido por argumento: {self.execucaoId}')
        except: self.execucaoId = execucaoId

        try: 
            arg2 = sys.argv[2] #recebe a FilaId
            if len(arg2) == 24: self.filaId = arg2
            logging.info(f'FilaId recebido por argumento: {self.filaId}')
        except: self.filaId = filaId

        if not self.execucaoId: 
            try:
                argumentos = r"C:\Automate Brasil\Agent\temp\argumentos.txt"
                with open(argumentos, "r") as f: args = f.read()
                execucaoId, filaId = args.split(';')
                os.remove(argumentos)
                logging.info(f'ExecucaoId {execucaoId} e FilaId {filaId} recebidos por arquivo')
            except: argumentos = False

    def proxy(self, server:str, user:str, password:str) -> None:
        """DICA: coloque sua senha criptografada como variavel de ambiente"""
        logging.info(f'Atribuindo configuração de proxy - servidor: {server}, usuario: {user}')
        self.usarProxy = True
        self.server = server 
        self.user = user 
        self.password = password
        url_dict = parse_url(self.server)._asdict()
        url_dict['auth'] = self.user + ':' + quote(self.password, '')
        urlProxy =  Url(**url_dict).url
        self.urlProxy = {'http': urlProxy, 'https': urlProxy}
        logging.info('Configuração de proxy registrada')
    
    def setExecucaoId(self, execucaoId:str) -> None:
        logging.info(f'Atribuindo ExecucaoId: {execucaoId}')
        self.execucaoId = execucaoId
        
    def setFilaId(self, filaId:str) -> None:
        logging.info(f'Atribuindo FilaId: {filaId}')
        self.filaId = filaId


    # Funções de apoio
    def setLogFile(self, localLog:str, logFile:str) -> None:
        logging.info(f'Atribuindo configuração de log em arquivo - Local do arquivo: {localLog}, nivel de log: {logFile}')
        self.logFile = logFile
        self.localLog = localLog
        if self.logFile:
            logging.basicConfig(filemode='a', filename=self.localLog)
        logging.getLogger().setLevel(getattr(logging, logFile.upper(), logging.DEBUG))

    def formatar_arquivo(self, arquivo:str) -> dict: #formata o arquivo para enviar
        logging.info(f'Formatando arquivo para base64 para envio: {arquivo}')
        retorno = {}
        nomeArquivo = os.path.basename(arquivo).lower()
        with open(arquivo, "rb") as f: arquivo64 = base64.b64encode(f.read())
        
        arquivo64 = arquivo64.decode('ascii')
        retorno = {'filename':nomeArquivo, 'base64': arquivo64}
        logging.debug(f'Arquivo formatado')
        return retorno

    def salvar_arquivo(self, link:str, destino:str) -> bool: #recebe o link do arquivo e salva com o nome e local desejado
        try:
            logging.info(f'Salvando arquivo do link: {link} para o destino: {destino}')
            r = requests.get(link)
            with open(destino, 'wb') as f: f.write(r.content)
            return True
        except Exception as e:
            erro = {'Msg': 'Erro ao salvar arquivo', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            logging.error(f'Falha ao salvar arquivo: {erro}')
            return False

    def logMaquina(self, nivel:str, mensagem:str) -> None:
        """### Função Obsoleta use a biblioteca logging diretamente para registrar logs em arquivo e console, esta função é mantida para compatibilidade com versões anteriores, mas os logs registrados por ela não seguem o formato estruturado.
        ##### Niveis de log
        'debug' = registra todos os paraemtros de entrada e saida de cada interação
        'info' = registra todos os acessos sem os detalhes de entrada e saida 
        'alert' = registra inicio e fim de execução, alteração de parametros, credenciais e erros
        False = desabilita o registro de log em arquivo
        """
        match nivel.upper(): 
            case 'DEBUG': logging.debug(mensagem)
            case 'ERROR': logging.error(mensagem)
            case 'ALERT': logging.warning(mensagem)
            case _: logging.info(mensagem)


    # Funçoes de comunicação com as APIs do SRS
    # controle de execução
    def execucaoIniciar(self) -> dict: 
        """##### Retorno:
        {"Autorizado": true, "ExecucaoId": "","Mensagem": "",
        "Parametros": [{
            "AlteradoPorAPI": 0,
            "NomeParametro": "",
            "TipodadoId": "1",
            "ValorParametro": ""
        }]} 
        """
        entrada = {'Token':self.token,
            'Workflow':self.workflow,
            'Tarefa':self.tarefa,
            'NomeMaquina':self.maquina,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if self.execucaoId: entrada['ExecucaoId'] = self.execucaoId
        logging.warning(f'----EXECUCAO INICIADA----')
        logging.debug(f'Parametros envidados:{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/execucao/iniciar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/execucao/iniciar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            logging.error(f'Falha ao iniciar execução: {erro}')
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}

        if retorno["Autorizado"]: 
            self.execucaoId = retorno['ExecucaoId']
            logging.info(f'Execução:{self.execucaoId} iniciada com sucesso')
            configuracao = {}
            if len(retorno['Parametros'])>0:
                for par in retorno['Parametros']:
                    if par['TipodadoId'] == '6':
                        configuracao[par['NomeParametro']] = json.loads(par['ValorParametro'])
                    else:
                        configuracao[par['NomeParametro']] = par['ValorParametro']
            retorno['Configuracao'] = configuracao
            logging.debug(f'Parametros de configuração recebidos: {configuracao}')
        else: 
            logging.error(f'Falha ao iniciar execução: {retorno}')
            sys.exit()
        return retorno

    def log(self, statusId:int, mensagem:str, arquivo:str='') -> dict:
        """Log de status da execução, use para registrar o andamento da execução, mensagens de alerta e erros diretamente no SRS Cloud"""
        entrada = {'Token': self.token,
            'StatusId':statusId, #(2=mensagem de andamento, 3=alerta)
            'Descricao':mensagem,
            'ExecucaoId': self.execucaoId,
            'FileMode':'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        if arquivo:
            if 'filename' not in arquivo: arquivo = self.formatar_arquivo(arquivo)
            entrada['Arquivo'] = json.dumps(self.formatar_arquivo(arquivo))

        logging.debug(f'Registrando log :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/execucao/log", data=entrada, proxies=self.urlProxy, verify=False, files=arquivo)
        else: response = requests.request("POST", f"{self.url}api/execucao/log", data=entrada, files=arquivo)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            logging.error(f'Falha ao registrar log: {erro}')
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}

        if not retorno["Autorizado"]: logging.error(f'Falha ao registrar log: {retorno}')
        return retorno

    def parametroAtualizar(self, parametro:str, valor, workflow=False, tarefa=False) -> dict:
        """- voce pode criar parametros com permissão de alteração pelo robo
        - utilize esta função para alterar estes parametros"""
        if not tarefa: tarefa = self.tarefa
        if not workflow: workflow = self.workflow
        entrada={'Token': self.token,
            'Workflow': workflow,
            'Tarefa': tarefa,
            'Parametro': parametro,
            'Valor': valor,
            'FileMode':'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        logging.info(f'Alterando paramertos da tarefa- Parametros envidados:{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/tarefa/parametro", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/tarefa/parametro", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f'Falha ao alterar parametro: {erro}')

        if not retorno["Autorizado"]: logging.error(f'Falha ao tentar alterar parametro: {retorno}')
        return retorno

    def execucaoFinalizar(self, status:str='Ok', statusId:int=4, mensagem:str='Execução finalizada') -> dict:
        """#para registrar um erro use status='Erro' ou statusId 5"""
        entrada = {'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'Descricao':mensagem,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if statusId !=4: entrada['StatusId'] = statusId
        elif status != 'Ok': entrada['Status'] = status

        logging.info(f'Finalizando execução :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/execucao/finalizar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/execucao/finalizar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f'Falha ao finalizar execução: {erro}')

        if not retorno["Autorizado"]: logging.error(f'Falha ao finalizar execução: {retorno}')
        return retorno

    def executarTarefa(self, workflow:str, tarefa:str, maquina:str, filaId=False) -> dict: 
        entrada = {'Token': self.token,
            'Workflow':workflow,
            'Tarefa': tarefa, 
            'NomeMaquina': maquina,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if filaId: entrada['FilaId'] = filaId
        if self.execucaoId: entrada['ExecucaoId'] = self.execucaoId

        logging.info(f'Tarefa Executar, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/tarefa/executar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/tarefa/executar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao requisitar execução de tarefa: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao executar tarefa: {retorno}')
        return retorno
    
    def enviarNotificacao(self, canal:list, destino:list, assunto:str, mensagem:str, confidencial:int=0): 
        """Canais válidos: **Whatsapp, Teams, Email, Portal (** Betatest)
        múltiplos canais = ['Email', 'Portal']
        Use usuarioId, usuarioToken ou perfil como destinatário
        multiplos destinos = [{'Token': 'yyy'}, {'UsuarioId':'xxx'}, {'Perfil':'Admin'}, {'Perfil':'Todos'}]
        confidencial = 1 para dados sensiveis, não registra log do donteudo da mensagem
        """
        if type(destino) != str: destino = json.dumps(destino)
        if type(canal) != str: canal = json.dumps(canal)
        entrada = {'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'Canal': canal,
            'Destino': destino, 
            'Assunto': assunto, 
            'Mensagem': mensagem, 
            'Confidencial': confidencial,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if confidencial ==0: logging.info(f'Enviar notificação, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/notificacao/notificar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/notificacao/notificar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao enviar notificação: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao enviar notificação: {retorno}')
        return retorno


    # controle de credenciais
    def credencialObter(self, sistema:str) -> dict:
        """Retorno:
        {"Autorizado": true,
        "Credencial": {
            "CredencialId": "28d23acb-2739-4498-9e23-9e0decd154b9",
            "EmExecucao": null,
            "ExpiraEm": "Tue, 26 Dec 2023 00:00:00 GMT",
            "Expirada": 0,
            "GerarSenha": 0,
            "NomeCredencial": "RoboAdm",
            "ResponsavelCelular": "",
            "ResponsavelEmail": "",
            "ResponsavelNome": ""
        },
        "CredencialParametro": {
            "Empresa": "Automate",
            "Senha": "batatafrita",
            "Usuario": "Christian"
        },
        "Mensagem": "Credencial RoboAdm do sistema SAP concedida",
        "Sistema": {
            "AcessoExclusivo": 0,
            "Autorizado": true,
            "Caminho": "http://localhost:123/sap",
            "Corporativo": 1,
            "NomeSistema": "SAP",
            "RespNegEmail": "marcelo.favero@automate.com.br",
            "RespNegNome": "Marcelo Favero",
            "RespNegTelefone": "11973097301",
            "RespTecEmail": "herminio.pereira@automate.com.br",
            "RespTecNome": "Herm\u00ednio Pereira",
            "RespTecTelefone": "11998725567",
            "SistemaId": "1",
            "TipoAcesso": "Login e Senha",
            "TipoAcessoId": "1",
            "TipoInterface": "WebBrowser",
            "TipoInterfaceId": "1"
        }}
        """
        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'Sistema':sistema,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Credencial obter, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/credencial/obter", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/credencial/obter", data=entrada)

        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}

        if not retorno["Autorizado"]: logging.error(f'Falha ao obter credencial: {retorno}')
        return retorno

    def credencialAlterar(self, credencialId:str, expiraEm=False, parametro=False, valorAntigo=False, valorNovo=False, ativo:int=1) -> dict:
        """#utilize esta função para atualizar o status (1=ativo/0=inativo), senhas e data da expiração das credenciais"""
        entrada={'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'CredencialId': credencialId,
            'Ativo': ativo,#1=ativo, 0=inativo
            'ExpiraEm': expiraEm,
            'Parametro': parametro,
            'ValorAntigo': valorAntigo,
            'ValorNovo': valorNovo,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        log = {'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'CredencialId': credencialId,
            'Ativo': ativo,#1=ativo, 0=inativo
            'ExpiraEm': expiraEm,
            'Parametro': parametro,
            'ValorAntigo': 'valorAntigo',
            'ValorNovo': 'valorNovo',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Credencial obter, parametros :{log}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/credencial/atualizar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/credencial/atualizar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao alterar credencial: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao alterar credencial: {retorno}')
        return retorno


    # controle de fila
    def filaInserir(self, referencia:str, parametrosEntrada:dict, workflow=False, tarefa=False, inserirExecutando=False) -> dict: 
        if type(parametrosEntrada) != str: parametrosEntrada = json.dumps(parametrosEntrada)
        if not tarefa: tarefa = self.tarefa
        if not workflow: workflow = self.workflow

        entrada={'Token': self.token,
            'Workflow': workflow,
            'Tarefa': tarefa,
            'Referencia': referencia,
            'ParametrosEntrada': parametrosEntrada,
            'FileMode':'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if inserirExecutando: entrada['Status'] = 'EmExecucao'
        if self.execucaoId: entrada['ExecucaoId'] = self.execucaoId

        logging.info(f'Fila inserir, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/inserir", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/inserir", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao inserir fila: {erro}")

        if retorno["Autorizado"]: 
            if inserirExecutando: 
                self.filaId = retorno['FilaId']
                logging.info(f'Item {referencia} inserido na fila da tarefa {tarefa} com sucesso: {retorno["FilaId"]} e agora está em execução')
            else: logging.info(f'Item {referencia} inserido na fila da tarefa {tarefa} com sucesso: {retorno["FilaId"]}')
        else: logging.error(f'Falha ao inserir item de fila: {retorno}')
        return retorno

    def filaInserirLote(self, lote:list, workflow=False, tarefa=False) -> dict:
        """#lote = [{'Referencia': 'valor', 'ParametrosEntrada':{'Parametro':'valor', 'Parametro': 'valor'}, 'Arquivos': {'NomeParametro':'path do arquivo'}}]"""

        if type(lote) != str: lote = json.dumps(lote)
        if not tarefa: tarefa = self.tarefa
        if not workflow: workflow = self.workflow

        entrada={'Token': self.token,
            'Workflow': workflow,
            'Tarefa': tarefa,
            'Lote': lote,
            'FileMode': 'b64',
            'ExecucaoId': self.execucaoId,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Fila inserir LOTE, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/inserir", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/inserir", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao inserir fila lote: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao inserir lote na fila: {retorno}')
        return retorno

    def filaProximo(self, qtd:int=1) -> dict:#retorna o proximo item da fila, voce pode alterar a quantidade para trazer mais de 1
        """Resultado:
        { "Autorizado": true,
        "Fila": [
            {
            "DataInclusao": "2025-12-30 10:15:59",
            "DataUltimoStatus": "2025-12-30 10:15:59",
            "FilaId": "xxx",
            "Lote": "xxx",
            "Mensagem": "Acionamento manual pelo site",
            "ParametrosEntrada": "{\"Email\": \"exemplo@automate.com.br\", \"Nome\": \"Exemplo\"}",
            "Realocado": 0,
            "Referencia": "Execucao Manual"
            }
        ],
        "Mensagem": ""
        }
        """
        entrada = {'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'Lote': qtd,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if self.filaId: entrada['FilaId'] = self.filaId

        logging.info(f'FilaProximo, parametros:{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/proximo", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/proximo", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: 
            retorno = json.loads(response.text)
            if retorno["Autorizado"]:
                for item in retorno['Fila']: 
                    self.filaId = item['FilaId']
                    if type(item['ParametrosEntrada']) == str:
                        item['ParametrosEntrada'] = json.loads(item['ParametrosEntrada'])
                    logging.info(f'Item de fila recebido: {self.filaId}')
            else: logging.info(f'Sem registros na fila: {retorno}')
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao buscar proximo da fila: {erro}")
            self.filaId = False
        
        return retorno

    def filaAtualizar(self, filaId=False, parametrosSaida:dict={}, statusId:int=2, status:str='FilaOk', proximo:int=0, mensagem:str='Fila atualizada com sucesso') -> dict:
        if type(parametrosSaida) != str: parametrosSaida = json.dumps(parametrosSaida)
        if not filaId: filaId = self.filaId

        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'FilaId':filaId,
            #'StatusId': statusId, #(0=aguardando, 1=em execucao, 2=encerrado com sucesso, 3=encerrado com erro)
            'Mensagem':mensagem,
            'ParametrosSaida': parametrosSaida,
            'Proximo':proximo,
            'FileMode': 'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if statusId !=2: entrada['StatusId'] = statusId
        elif status != 'Ok': entrada['Status'] = status

        logging.info(f'Fila atualizar, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/atualizar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/atualizar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao atualizar imte de fila: {erro}")

        if retorno["Autorizado"]: 
            logging.debug(f'Item de fila {filaId} atualizado com sucesso')
            if proximo >0:
                if retorno['Proximo']['Autorizado']:
                    for item in retorno['Proximo']['Fila']: 
                        self.filaId = item['FilaId']
                        if type(item['ParametrosEntrada']) == str:
                            item['ParametrosEntrada'] = json.loads(item['ParametrosEntrada'])
                        logging.info(f'Item de fila recebido: {self.filaId}')
                else: logging.info(f'Sem registros na fila: {retorno}')

        else: logging.error(f'Falha ao atualizar item de fila: {retorno}')
        return retorno

    def filaAtualizarLote(self, lote:int) -> dict:
        """Atualiza vários registros ao mesmo tempo (todos os itens atualizados devem, obrigatoriamente, 
        estar em status 1(em Execucao) vinculados a esta execucaoId)
        lote = [{'FilaId': filaId, 
            'Status': 'FilaOk', 
            'ParametrosSaida': {'Parametro':'valor', 'Parametro': 'valor'},
            'Mensagem': 'mensagem', 
        }]"""

        if type(lote) != str: lote = json.dumps(lote)

        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'Lote':lote,
            'FileMode': 'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Fila atualizar em lote, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/atualizar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/atualizar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}

        if not retorno["Autorizado"]: logging.error(f'Falha ao atualizar lote de fila: {retorno}')
        return retorno

    def filaConsultar(self, criterio:list, ordenadoPor:str, limite:int=10, workflow=False, tarefa=False) -> dict:
        """Retorno:
        {"Autorizado": true,
        "Fila": [
            {
            "DataInclusao": "Fri, 01 Sep 2023 11:03:42 GMT",
            "DataInicioExecucao": "Mon, 29 Jan 2024 16:45:46 GMT",
            "DataUltimoStatus": "Mon, 29 Jan 2024 16:45:46 GMT",
            "ExecucaoId": "9c2c8d24-2cbd-4fbe-9ab6-d330166bfd47",
            "FilaId": "409ed1a7-eaf7-4dda-b46e-5c2f7b019b5a",
            "Mensagem": "Acionamento manual pelo site",
            "ParametrosEntrada": "{\"Email\": \"christian.marcondes@automate.com.br\", \"Nome\": \"Christian\"}",
            "ParametrosSaida": null,
            "Realocado": 0,
            "Referencia": "Execucao Manual",
            "StatusAlias": "EmExecucao",
            "StatusId": "1",
            "TarefaId": "2",
            "UsuarioId": ""
            }
        ],
        "Mensagem": ""}
        #Exemplos de criterios :
            #criterio = [{'Campo':'StatusId', 'Valor':'>0'}]
            #criterio = [{'Campo':'StatusId', 'Valor':'<2'},
            #            {'Campo':'Realocado', 'Valor':'=0'},
            #            {'Campo':'Referencia', 'Valor':'="cadastro Lote 01"'}]
            #criterio = [{'Campo':'Referencia', 'Valor':'like "%cadastro%"'}]
            #criterio = [{'Campo':'DataInclusao', 'Valor':'< "2023/06/26"'}]
        # utilize qualquer campo de retorno acima como parametro Campo
        # em Valor utilize um sinal de comparação ('>', '<', '=', '<>' ou like ) e o valor a ser comparado
        """
        
        if type(criterio) != str: criterio = json.dumps(criterio)
        if not tarefa: tarefa = self.tarefa
        if not workflow: workflow = self.workflow

        entrada={'Token': self.token,
            'ExecucaoId': self.execucaoId,
            'Workflow': workflow,
            'Tarefa': tarefa,
            'Criterios': criterio,
            'OrderBy': ordenadoPor,
            'Limite':limite,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Fila consultar, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/fila/consultar", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/fila/consultar", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao consultar fila: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao consultar fila: {retorno}')
        return retorno

    def relatorio(self, relatorio:str, dataInicio, dataFim, workflowAlias=False, tarefaAlias=False, statusId=False, pagina:int=0, limite:int=1000) -> dict:
        """Relatorios válidos: relatorio_atividade, relatorio_maquina, relatorio_auditoria, relatorio_execucao, relatorio_sistema
            formato das datas: 'YYYY-mm-dd'
        """
        if type(dataInicio) != str: dataInicio = dataInicio.strftime('%Y-%m-%d')
        if type(dataFim) != str: dataFim = dataFim.strftime('%Y-%m-%d')
        parametrosEntrada = {'DataInicio': dataInicio, 'DataFim':dataFim, 'Limite': limite, 'Pagina':pagina}
        if workflowAlias: parametrosEntrada['Workflow'] = workflowAlias
        if tarefaAlias: parametrosEntrada['Tarefa'] = tarefaAlias
        if statusId: parametrosEntrada['StatusId'] = statusId
        parametrosEntrada = json.dumps(parametrosEntrada)
        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'ParametrosEntrada': parametrosEntrada,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }

        logging.info(f'Requisição relatorio: {relatorio}, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}api/relatorio/{relatorio}", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}api/relatorio/{relatorio}", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao requisitar relatorio: {erro}")

        if not retorno["Autorizado"]: logging.error(f'Falha ao requisitar relatorio: {relatorio}: {retorno}')
        return retorno

    # Agentes de IA 
    def agenteIA(self, agenteAlias:str, prompt:str) -> dict:
        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'Prompt': prompt,
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        logging.info(f'Chamando AgenteIA: {agenteAlias}, Prompt :{prompt}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}ia/{agenteAlias}", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}ia/{agenteAlias}", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao acionar agenteIA: {erro}")
            
        return retorno

    # principais serviços do BotStore
    def botstoreRequisicaoGenerica(self, servico:str, parametrosEntrada:dict, assincrono:bool=False) -> dict:
        """Consulte a lista de serviços no portal SRS > BotStore, estamos sempre criando novos para você""" 
        if type(parametrosEntrada) != str: parametrosEntrada = json.dumps(parametrosEntrada)
        entrada = {'Token': self.token,
            'ExecucaoId':self.execucaoId,
            'ParametrosEntrada': parametrosEntrada,
            'FileMode': 'b64',
            'Funcao':inspect.stack()[1][3],
            'LinhaComando':inspect.currentframe().f_back.f_lineno
        }
        if assincrono: entrada['Retorno'] = 1
        logging.info(f'Requisição de serviço BOTSTORE: {servico}, parametros :{entrada}')
        if self.usarProxy: response = requests.request("POST", f"{self.url}botstore/{servico}", data=entrada, proxies=self.urlProxy, verify=False)
        else: response = requests.request("POST", f"{self.url}botstore/{servico}", data=entrada)

        logging.debug(f'Retorno: {response.text}')
        try: retorno = json.loads(response.text)
        except Exception as e: 
            erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
            retorno = {'Autorizado': False, 'Mensagem': f'Falha na comunicação:{erro}'}
            logging.error(f"Falha ao BotStore {servico}: {erro}")

        return retorno
    
    def bsQuebraCaptcha(self, imagemCaptcha) -> dict:
        if 'filename' not in imagemCaptcha: imagemCaptcha = self.formatar_arquivo(imagemCaptcha)
        parametrosEntrada = {'Captcha': imagemCaptcha}
        return self.botstoreRequisicaoGenerica('captcha', parametrosEntrada)
    
    def bsQuebraRecaptcha(self, googlekey:str, pageurl:str) -> dict:
        logging.info('Iniciando Quebra de Recaptcha Assincrono...')
        parametrosEntrada = {'googlekey': googlekey, 'pageurl': pageurl}
        retorno = self.botstoreRequisicaoGenerica('recaptcha', parametrosEntrada, assincrono=True)
        if retorno['Autorizado']:
            botStoreId = retorno['BotStoreId']
            logging.debug(f'Requisição registrada com sucesso: {botStoreId}')
        else: 
            logging.error(f"Falha ao requisitar Recaptcha: {erro}")
            return retorno
        
        url=f"{self.url}botstore/consulta_andamento"
        
        payload = {'Token': self.token, 'ParametrosEntrada': json.dumps({'BotStoreId':botStoreId})}
        limite = 160 #2 minutos 
        for i in range(limite):
            try:  
                response = requests.post(url, data=payload)
                retorno = json.loads(response.text)
                logging.debug(f"{i} - Aguardando resposta do serviço: {botStoreId}, status: {retorno['Resultado']['StatusId']}")
                if not retorno['Autorizado']: 
                    logging.error(f"Falha ao consultar andamento da requisição: {erro}")
                    return retorno
                elif retorno['Resultado']['StatusId'] != 0: 
                    logging.debug(f"{i} - Retorno identificado: {retorno}")
                    return retorno['Resultado']['ParametrosSaida']
                time.sleep(1)
            except Exception as e: 
                erro = {'Msg': 'Erro', 'type': type(e).__name__, 'message': str(e), 'lineo': e.__traceback__.tb_lineno}
                mensagem = f'Erro no acompanhamento da quebra do recaptcha:{erro} : retorno: {retorno}'
                logging.error(mensagem)
                return {'Autorizado':False, 'Mensagem': mensagem}
    
    def bsConsultaCNPJ(self, cnpj:str) -> dict:
        parametrosEntrada = {'cnpj': cnpj}
        return self.botstoreRequisicaoGenerica('consulta_cnpj', parametrosEntrada)
    
    def bsConsultaSintegra(self, cnpj:str) -> dict:
        parametrosEntrada = {'cnpj': cnpj}
        return self.botstoreRequisicaoGenerica('cnpj_sintegra', parametrosEntrada)
    
    def bsExcel2Json(self, planilha) -> dict:
        if 'filename' not in planilha: planilha = self.formatar_arquivo(planilha)
        parametrosEntrada = {'Planilha': planilha}
        return self.botstoreRequisicaoGenerica('excel2json', parametrosEntrada)
    
    def bsWord2Json(self, documento) -> dict:
        if 'filename' not in documento: documento = self.formatar_arquivo(documento)
        parametrosEntrada = {'Word': documento}
        return self.botstoreRequisicaoGenerica('word2json', parametrosEntrada)
    
    def bsCotacaoMoeda(self, moeda:str, moedaComparacao:str) -> dict:
        """pode ter mais de uma: 'USD,EUR,BRL' """
        parametrosEntrada = {'moedas': moeda, 'moedaComparacao':moedaComparacao}
        return self.botstoreRequisicaoGenerica('comp_cotacao_moedas', parametrosEntrada)
    
    def bsBoleto(self, arquivo) -> dict:
        if 'filename' not in arquivo: arquivo = json.dumps(self.formatar_arquivo(arquivo))
        parametrosEntrada = {'Arquivo': arquivo}
        return self.botstoreRequisicaoGenerica('ib_boletosbancarios', parametrosEntrada)
    
    def bsNotaFiscal(self, arquivo) -> dict:
        if 'filename' not in arquivo: arquivo = json.dumps(self.formatar_arquivo(arquivo))
        parametrosEntrada = {'Arquivo': arquivo}
        return self.botstoreRequisicaoGenerica('ib_nf', parametrosEntrada)