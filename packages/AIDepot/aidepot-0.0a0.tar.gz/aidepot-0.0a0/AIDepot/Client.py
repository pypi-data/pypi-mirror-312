import asyncio
import json

import websockets
from aiohttp import ContentTypeError
from websockets.exceptions import ConnectionClosedError
import urllib.parse
from typing import *
from datetime import datetime
import tzlocal
import aiohttp

import AIDepot

import nest_asyncio

nest_asyncio.apply()


class Client():

    URL = 'aidepot.net'
    API_PATH = 'api'
    WEBSOCKET_API_PATH = 'api/ws/status'

    def __init__(self, subscriber_id: str, api_key: str):
        self.subscriber_id = subscriber_id
        self.api_key = api_key

        self.headers = {
            'User-Agent': 'AIDepotClient/1.0',
            'accept': 'application/json',
            'X-SUBSCRIBER-ID': subscriber_id,
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        self.session = None

    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._destroy_session())

    def submit_job(self,
                   resource: AIDepot.Resources,
                   job: dict,
                   version: str = '1') -> Tuple[int, Optional[dict], dict]:
        """Submit a job to the server and wait for the response

        Returns:
        When the job submission is successful:
            (HTTP status code of completed job, completed job response, job submission response)
        When the job submission is not successful:
            (HTTP status code of job submission request, None, job submission response)
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._submit_job_async(resource, job, version))

    async def submit_job_async(self,
                               resource: AIDepot.Resources,
                               job: dict,
                               version: str = '1') -> Tuple[int, Optional[dict], dict]:
        """Submit a job to the server and a future waits for the response

        Returns a future. Awaiting the future will return the following:
        When the job submission is successful:
            (HTTP status code of completed job, completed job response, job submission response)
        When the job submission is not successful:
            (HTTP status code of job submission request, None, job submission response)
        """
        return await self._submit_job_async(resource, job, version)

    def start_job(self, resource: AIDepot.Resources, job: dict, version: str = '1') -> Tuple[int, dict]:
        """Start a job and wait for the job submittal status

        Returns (http status code, job submittal response)
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.start_job_async(resource, job, version))

    async def start_job_async(self, resource: AIDepot.Resources, job: dict, version: str = '1') -> Tuple[int, dict]:
        """Start a job without waiting for the job submittal status

        Returns a future, when awaited gives: (http status code, job submittal response)
        """
        return await self._submit_http_request_async(resource, job, version)

    def get_job_result(self, resource: AIDepot.Resources, job_id: int, version='1') -> Tuple[int, dict]:
        """ Fetch the job results given the job_id.

        Does not wait for the job to complete.
        If you want to wait for the job to complete, call connect_and_listen_for_status(...) instead.

        When the job is complete, the responses will be included in the response.
        When the job is pending, the response will note this and not include results.
        If the job failed, the response will note this.
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.get_job_result_async(resource, job_id, version))

    async def get_job_result_async(self, resource: AIDepot.Resources, job_id: int, version='1') -> Tuple[int, dict]:
        """ Fetch the job results given the job_id.

        Does not wait for the job to complete.
        If you want to wait for the job to complete, call connect_and_listen_for_status_async(...) instead.

        When the job is complete, the responses will be included in the response.
        When the job is pending, the response will note this and not include results.
        If the job failed, the response will note this.
        """
        job = {
            'job_id': job_id
        }

        return await self.start_job_async(resource, job, version)

    def connect_and_listen_for_status(self, job_id: int) -> Tuple[int, dict]:
        """ Waits for the job to complete and then immediately returns the response """

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.connect_and_listen_for_status_async(job_id))

    async def connect_and_listen_for_status_async(self, job_id: int) -> Tuple[int, dict]:
        """ Waits for the job to complete and then immediately returns the response """
        websocket_headers = {
            'User-Agent': 'AIDepotClient/1.0',
            'X-SUBSCRIBER-ID': self.subscriber_id,
            'X-API-KEY': self.api_key,
        }

        local_timezone = tzlocal.get_localzone()

        num_retries = 0
        num_chunks = 0
        chunks_received = 0
        chunks = []

        while True:
            try:
                websocket_url = self.build_websocket_route(job_id)

                async with websockets.connect(websocket_url, additional_headers=websocket_headers) as websocket:

                    # Listen and respond to messages indefinitely
                    while True:
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=25)

                            response = json.loads(response)
                            if response == {
                                    'message': 'pong'
                            }:
                                continue

                            if len(response.keys()) == 1 and 'chunks' in response.keys():
                                chunks_received = 0
                                num_chunks = response['chunks']
                                chunks = [None for i in range(num_chunks)]
                            elif len(response.keys()) == 1 and list(response.keys())[0].startswith('chunk_'):
                                key, payload = response.popitem()
                                current_chunk = int(key[6:])
                                if current_chunk > num_chunks:
                                    continue
                                chunks_received += 1
                                chunks[current_chunk] = payload

                                if chunks_received == num_chunks:
                                    result_json = ''.join(chunks)
                                    # Any nicety parsing of the results are done via _parse_dict,
                                    # for example putting timestamps in the user's timezone
                                    result = Client._parse_dict(json.loads(result_json), local_timezone)
                                    return (200, result)
                            elif 'responses' in response.keys():
                                # Any nicety parsing of the results are done via _parse_dict,
                                # for example putting timestamps in the user's timezone
                                result = Client._parse_dict(response, local_timezone)
                                return (200, result)
                            else:
                                return (
                                    500, {
                                        'error':
                                            ValueError(f"Websocket response not understood, keys: {response.keys()}")
                                    })

                        except asyncio.TimeoutError:
                            # Did not receive a response in the number of seconds waiting,
                            # so send a heartbeat to keep the connection alive
                            await websocket.send(json.dumps({'message': 'ping'}))
                        except ConnectionClosedError as e:
                            code = e.rcvd.code
                            if code >= 2000:
                                # Some unretriable error
                                print(f"Error: Connection closed by the websocket server with code : {code}")
                                return (e.rcvd.code, {})
                            else:
                                # Could be a going away notification
                                # Break the inner loop to reconnect
                                break
            except (ConnectionRefusedError, OSError):
                if num_retries < 3:
                    retry_backoff = 3
                    print(f"Failed to connect to the server. Retrying in {retry_backoff} seconds...")
                    await asyncio.sleep(retry_backoff)
                    num_retries += 1
                else:
                    raise
            except Exception as e:
                if num_retries == 0:
                    retry_backoff = 3
                    print(f"Unexpected error: {e}. Retrying in {retry_backoff} seconds...")
                    await asyncio.sleep(retry_backoff)
                else:
                    raise

    @staticmethod
    def build_http_route(resource: AIDepot.Resources, version: str = '1'):
        api_path = f'https://{Client.URL}/{Client.API_PATH}/v{version}/{resource.value}/'
        return api_path

    def build_websocket_route(self, job_id: int):
        subsciber_id_qt = urllib.parse.quote(self.subscriber_id)
        websocket_url = f'wss://{Client.URL}/{Client.WEBSOCKET_API_PATH}/{subsciber_id_qt}/{job_id}/'
        return websocket_url

    async def _submit_job_async(self,
                                resource: AIDepot.Resources,
                                job: dict,
                                version: str = '1') -> Tuple[int, Optional[dict], dict]:

        job_submittal_status, job_submittal_response = await self.start_job_async(resource, job, version)

        if job_submittal_status >= 400:
            return (job_submittal_status, None, job_submittal_response)

        # Retrieve the job id from the submission response,
        # and open a websocket to listen for the finished job's response
        job_id = job_submittal_response['job_id']
        response_code, result = await self.connect_and_listen_for_status_async(job_id)

        return response_code, result, job_submittal_response

    async def _submit_http_request_async(self, resource: AIDepot.Resources, job: dict, version: str):
        api_path = self.build_http_route(resource, version)

        if self.session is None:
            await self._create_session()

        async with self.session.post(api_path, json=job, headers=self.headers) as response:
            job_submittal_status = response.status
            try:
                job_submittal_response = await response.json()
            except ContentTypeError as ex:
                # When it is text, that indicates an error, put this in a dict using key 'error'
                job_submittal_response = await response.text()
                job_submittal_response = {
                    'error': job_submittal_response
                }
        return job_submittal_status, job_submittal_response

    async def _create_session(self):
        if self.session is None:
            self.session = await aiohttp.ClientSession().__aenter__()

    async def _destroy_session(self):
        if self.session is not None:
            await self.session.close()

    @staticmethod
    def _parse_dict(d, local_timezone) -> Any:
        if isinstance(d, dict):
            n = {}
            for key, value in d.items():
                if isinstance(key, str) and isinstance(value, str):
                    n[key] = Client._parse_str(key, value, local_timezone)
                else:
                    n[key] = Client._parse_dict(value, local_timezone)
            return n
        elif isinstance(d, list):
            v = []
            for x in d:
                v.append(Client._parse_dict(x, local_timezone))
            return v
        else:
            return d

    @staticmethod
    def _parse_str(key: str, value: str, local_timezone) -> any:
        if key.endswith('timestamp'):
            return datetime.fromisoformat(value).astimezone(local_timezone)
        else:
            return value
