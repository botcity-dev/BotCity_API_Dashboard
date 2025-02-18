import json
import time
import requests
from functools import lru_cache
from typing import Any, Dict, List
from app import configurations as config

class BotcityApiPlugin:

    API_URL = 'https://developers.botcity.dev/api/v2'
    TOKEN_EXPIRATION_TIME = 3600

    def __init__(self, login: str, key: str):
        self._login = login
        self._key = key
        self._token = None
        self._start_time = None

    def _get_access_token(self):
        if self._start_time is not None:
            if time.time() - self._start_time > self.TOKEN_EXPIRATION_TIME:
                self._token = None

        if self._token is None:
            url = f'{self.API_URL}/workspace/login'

            payload = json.dumps({
                'login': self._login,
                'key': self._key
            })

            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()

            self._token = response.json().get('accessToken')
            self._start_time = time.time()

        return self._token
    
    def _get(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {
            'organization': config.MAESTRO_WORKSPACE,
            'token': self._get_access_token()
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def _list(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = params or {}
        result = None

        limit = params.pop('limit', None)

        while True:
            page_result = self._get(url, params)

            is_last = page_result.get('last', True)
            is_empty = page_result.get('empty', True)

            page = page_result.get('number', 0)
            params['page'] = page + 1

            if result is None:
                result = page_result
            else:
                content = result.get('content', [])
                content.extend(page_result.get('content', []))
                result['content'] = content

            if is_last or is_empty or (limit is not None and len(result.get('content', [])) >= limit):
                break

        content = result.get('content', [])[:limit]
        result['content'] = content

        return result
    
    def get_tasks(self, *, 
                  days: int = None, state_filter: str = None, activity_label: str = None, machine_id: str = None,
                  page: int = None, size: int = None, sort: List[str] = None,
                  limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/task'

        params = {
            'days': days,
            'stateFilter': state_filter,
            'activityLabel': activity_label,
            'machineId': machine_id,
            'page': page,
            'size': size,
            'sort': sort,
            'limit': limit
        } 

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    def get_bots(self, *, 
                 bot_id: str = None,
                 page: int = None, size: int = None, sort: List[str] = None,
                 limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/bot/pagination'

        params = {
            'botId': bot_id,
            'page': page,
            'size': size,
            'sort': sort,
            'limit': limit
        } 

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    def get_activities(self, *, 
                       automation: str = None, label: str = None, name: str = None,
                       page: int = None, size: int = None, sort: List[str] = None,
                       limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/activity/pagination'

        params = {
            'automation': automation,
            'label': label,
            'name': name,
            'page': page,
            'size': size,
            'sort': sort,
            'limit': limit
        } 

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    def get_runners(self, *,
                    machine_id: str = None, is_online: bool = None, runner_type: str = None,
                    page: int = None, size: int = None, sort: List[str] = None,
                    limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/machine/pagination'

        params = {
            'machineId': machine_id,
            'isOnline': is_online,
            'type': runner_type,
            'page': page,
            'size': size,
            'sort': sort,
            'limit': limit
        } 

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    def get_schedulings(self, *,
                        page: int = None, size: int = None, sort: List[str] = None,
                        limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/scheduling'

        params = {
            'page': page,
            'size': size,
            'sort': sort,
            'limit': limit
        } 

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    def get_errors(self, *,
                   page: int = None, size: int = None, sort: List[str] = None,
                   days: int = None, task_id: str = None, automation_label: str = None,
                   limit: int = None) -> Dict[str, Any]:
        url = f'{self.API_URL}/error'

        params = {
            'page': page,
            'size': size,
            'sort': sort,
            'days': days,
            'taskId': task_id,
            'automationLabel': automation_label,
            'limit': limit
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self._list(url, params)
    
    @lru_cache(maxsize=2000)
    def get_error_by_id(self, error_id: str) -> Dict[str, Any]:
        url = f'{self.API_URL}/error/{error_id}'
        return self._get(url)