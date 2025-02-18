import pandas as pd
from datetime import datetime, timedelta
from cstriggers.core.trigger import QuartzCron

# System Libs
import sys

from data_source.botcity import BotcityApiPlugin
from typing import Hashable, Dict, List, Any

class BotcityDataAccess:
    """ Representa o acesso aos dados do botcity """

    def __init__(self, dso: BotcityApiPlugin):
        """
        Construtor

        :param dso: plugin de acesso à api do botcity
        """
        self._dso = dso

    def get_tasks_data(self) -> List[Dict[Hashable, Any]]:
        """
        Coleta dados sobre as tarefas executadas
        :returns: lista de dicionários com os dados
        """
        result = self._dso.get_tasks(size=100, limit=100)

        # como vamos apresentar o erro no tooltip, vamos criar uma hashtable contendo o id da tarefa e a mensagem de erro
        errors = self._dso.get_errors(size=100, limit=100)['content']
        errors_lookup = {error['taskId']: error['message'] for error in errors}

        data = []
        task_error = ''

        for task in result['content']:


            # se deu erro, vamos retornar a mensagem do erro
            if task.get('finishStatus', '') in ['PARTIALLY_COMPLETED', 'FAILED']:
                task_id = task.get('id')
                task_error = errors_lookup.get(task_id, '')

            row = {
                'status': task.get('finishStatus') if task.get('state')=='FINISHED' else task.get('state'),
                'error_message': task_error,
                'id': task.get('id'),
                'bot': task.get('agentId'),
                'automations': task.get('parameters', {}).get('automations'),
                'description': task.get('activityName', '').split(' - ', 1)[-1],
                'start_date': task.get('dateCreation'),
                'end_date': task.get('dateLastModified'),
                'runner': task.get('machineId', ''),
                'creator': task.get('userCreationName'),
                'message': task.get('finishMessage')
            }

            data.append(row)

        df = pd.DataFrame(data)

        if not df.empty:

            df['start_date'] = pd.to_datetime(df['start_date']).dt.tz_convert('America/Sao_Paulo').dt.strftime(r'%d/%m/%Y %H:%M')

            df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce').dt.tz_convert('America/Sao_Paulo').dt.strftime(r'%d/%m/%Y %H:%M')

        df = df.sort_values(by=['start_date'])

        return df.to_dict('records')

    def get_schedules_data(self) -> List[Dict[Hashable, Any]]:
        """
        Coleta dados sobre as tarefas agendadas
        :returns: lista de dicionários com os dados
        """
        result = self._dso.get_schedulings()

        # como o cron está baseado no horário utc, vamos pegar uma data de início e fim também utc
        from_date = datetime.utcnow()
        to_date = from_date + timedelta(days=1)

        data = []
        for schedule in result['content']:
            try:
                # vamos pegar a lista de datas das próximas execuções dado uma data de início e fim
                cron = schedule['cron']

                cron_obj = QuartzCron(schedule_string=cron, start_date=from_date, end_date=to_date)

                next_schedules = cron_obj.next_triggers(number_of_triggers=10,isoformat=True)

                # adicionamos ao dataframe
                for next_schedule in next_schedules:

                    row = {
                        'bot': schedule.get('activityLabel'),
                        'automations': schedule.get('parameters', {}).get('automations'),
                        #'Descrição': schedule.get('activityName', '').split(' - ', 1)[-1],
                        'start_date': next_schedule,
                    }
                    data.append(row)

            except Exception as error:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(f'Error Message: {str(error)} | Error line number:{exc_traceback.tb_lineno}')
                pass

        df = pd.DataFrame(data)

        if not df.empty:
            # Garantimos que a coluna 'start_date' está no formato datetime
            df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')

            # Se a coluna ainda não tem timezone, aplicamos UTC antes de converter
            if df['start_date'].dt.tz is None:
                df['start_date'] = df['start_date'].dt.tz_localize('UTC')

            # Convertemos para o fuso horário de São Paulo
            df['start_date'] = df['start_date'].dt.tz_convert('America/Sao_Paulo')

            # Formatamos para o formato brasileiro
            df['start_date'] = df['start_date'].dt.strftime('%d/%m/%Y %H:%M')

            # Ordenamos e pegamos os 20 primeiros registros
            df = df.sort_values(by=['start_date']).head(20)

        return df.to_dict('records')

    def get_runners_data(self) -> List[Dict[Hashable, Any]]:
        """
        Coleta dados sobre a disponibilidade dos runners
        :returns: lista de dicionários com os dados
        """
        result = self._dso.get_runners()
        
        data = []
        for runner in result['content']:
            row = {
                'online': runner.get('isOnline'),
                'name': runner.get('name'),
            }

            data.append(row)

        df = pd.DataFrame(data)
        # ordena (Runners offline vem primeiro)
        df = df.sort_values(by=['online', 'name'])

        return df.to_dict('records')