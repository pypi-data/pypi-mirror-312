import threading
import asyncio
import aiohttp
import aiofiles
import inspect
import rumax
import os

from .types import Update
from .crypto import Crypto
from . import exceptions


def capitalize(text: str):
    """
    Capitalize words in a snake_case string.

    Parameters:
    - text: Snake_case string.

    Returns:
    CamelCase string.
    """
    return ''.join([c.title() for c in text.split('_')])


class Network:
    HEADERS = {
        'origin': 'https://web.rubika.ir',
        'referer': 'https://web.rubika.ir/',
        'content-type': 'application/json',
        'connection': 'keep-alive'
    }

    def __init__(self, client: "rumax.Client") -> None:
        """
        Initialize the Network class.

        Parameters:
        - client (rumax.Client): instance.
        """
        self.client = client
        self.HEADERS['user-agent'] = self.client.user_agent
        if self.client.DEFAULT_PLATFORM['platform'] == 'Android':
            self.HEADERS.pop('origin')
            self.HEADERS.pop('referer')
            self.HEADERS['user-agent'] = 'okhttp/3.12.1'
            self.client.DEFAULT_PLATFORM['package'] = 'app.rbmain.a'
            self.client.DEFAULT_PLATFORM['app_version'] = '3.6.4'

        connector = aiohttp.TCPConnector(verify_ssl=False)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=self.HEADERS,
            timeout=aiohttp.ClientTimeout(client.timeout)
        )

        if client.bot_token is not None:
            self.bot_api_url = f'https://messengerg2b1.iranlms.ir/v3/{client.bot_token}/'

        self.api_url = None
        self.wss_url = None
        self.ws = None

    async def close(self):
        """
        Close the aiohttp ClientSession.
        """
        await self.session.close()

    async def get_dcs(self):
        """
        Retrieve API and WebSocket URLs.

        Returns:
        True if successful.
        """
        while True:
            try:
                response = await self.session.get('https://getdcmess.iranlms.ir/', proxy=self.client.proxy, verify_ssl=False)
                if response.ok is True:
                    response = (await response.json()).get('data')
                    self.api_url = response.get('API').get(response.get('default_api')) + '/'
                    self.wss_url = response.get('socket').get(response.get('default_socket'))
                    return True

            except Exception:
                continue

    async def request(self, url: str, data: dict):
        """
        Make an HTTP POST request.

        Parameters:
        - url: API endpoint URL.
        - data: Data to be sent in the request.

        Returns:
        JSON-decoded response.
        """
        for _ in range(3):
            try:
                response = await self.session.post(url=url, json=data, proxy=self.client.proxy, verify_ssl=False)
                if response.ok is True:
                    return await response.json()

            except Exception:
                continue

    async def send(self, **kwargs):
        """
        Send a request to the Rubika API.

        Parameters:
        - kwargs: Request parameters.

        Returns:
        JSON-decoded response.
        """
        api_version: str = str(kwargs.get('api_version', self.client.API_VERSION))
        auth: str = kwargs.get('auth', self.client.auth)
        client: dict = kwargs.get('client', self.client.DEFAULT_PLATFORM)
        input_data: dict = kwargs.get('input', {})
        method: str = kwargs.get('method', 'getUserInfo')
        encrypt: bool = kwargs.get('encrypt', True)
        tmp_session: bool = kwargs.get('tmp_session', False)
        url: str = kwargs.get('url', self.api_url)

        data = dict(api_version=api_version)

        data['tmp_session' if tmp_session is True else 'auth'] = auth if tmp_session is True else self.client.decode_auth

        if api_version == '6':
            data_enc = dict(client=client, method=method, input=input_data)

            if encrypt is True:
                data['data_enc'] = Crypto.encrypt(data_enc, key=self.client.key)

            if tmp_session is False:
                data['sign'] = Crypto.sign(self.client.import_key, data['data_enc'])

            return await self.request(url, data=data)

        elif api_version == '0':
            data['auth'] = auth
            data['client'] = client
            data['data'] = input_data
            data['method'] = method

        elif api_version == '4':
            data['client'] = client
            data['method'] = method

        elif api_version == 'bot':
            return await self.request(url=self.bot_api_url + method, data=input_data)

        return await self.request(url, data=data)

    async def handel_update(self, name, update):
        for func, handler in self.client.handlers.items():
            try:
                # if handler is empty filters
                if isinstance(handler, type):
                    handler = handler()

                if handler.__name__ != capitalize(name):
                    continue

                # analyze handlers
                if not await handler(update=update):
                    continue

                if not inspect.iscoroutinefunction(func):
                    threading.Thread(target=func, args=(Update(handler.original_update),)).start()

                else:
                    asyncio.create_task(func(Update(handler.original_update)))

            except exceptions.StopHandler:
                break

            except Exception:
                self.client.logger.error(
                    'handler raised an exception',
                    extra={'data': update}, exc_info=True)

    async def get_updates(self):
        """
        Receive updates from the Rubika WebSocket.
        """
        asyncio.create_task(self.keep_socket())
        while True:
            try:
                async with self.session.ws_connect(self.wss_url, verify_ssl=False, proxy=self.client.proxy, receive_timeout=5) as ws:
                    self.ws = ws
                    await ws.send_json(dict(method='handShake', auth=self.client.auth, api_version='6', data=''))

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            asyncio.create_task(self.handle_text_message(msg.json()))
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            break
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break

            except aiohttp.ServerTimeoutError:
                print("Websocket connection lost. Reconnecting...")
                await asyncio.sleep(5)  # wait before reconnecting

            except TimeoutError:
                print("Websocket connection lost. Reconnecting...")
                await asyncio.sleep(5)  # wait before reconnecting

            except aiohttp.ClientError:
                print("Websocket connection lost. Reconnecting...")
                await asyncio.sleep(5)  # wait before reconnecting

    async def keep_socket(self):
        while True:
            try:
                await asyncio.sleep(10)
                await self.ws.send_json({})
                await self.client.get_chats_updates()

            except Exception:
                continue

    async def handle_text_message(self, msg_data: dict):
        """
        Handle text messages received from the Rubika WebSocket.

        Parameters:
        - msg_data: Parsed JSON data from the WebSocket message.
        """
        try:
            if not msg_data.get('data_enc'):
                self.client.logger.debug(
                    'the data_enc key was not found',
                    extra={'data': msg_data})
                return

            decrypted_data = Crypto.decrypt(msg_data['data_enc'], key=self.client.key)
            user_guid = decrypted_data.pop('user_guid')

            tasks = []
            for name, package in decrypted_data.items():
                if not isinstance(package, list):
                    continue

                for update in package:
                    update['client'] = self.client
                    update['user_guid'] = user_guid
                    tasks.append(self.handel_update(name, update))

            await asyncio.gather(*tasks)

        except Exception:
            self.client.logger.error(
                'websocket raised an exception',
                extra={'data': self.wss_url}, exc_info=True)

    async def upload_file(self, file, mime: str = None, file_name: str = None, chunk: int = 1048576,
                          callback=None, *args, **kwargs):
        """
        Upload a file to Rubika.

        Parameters:
        - file: File path or bytes.
        - mime: MIME type of the file.
        - file_name: Name of the file.
        - chunk: Chunk size for uploading.
        - callback: Progress callback.

        Returns:
        - Results object.
        """
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('File not found in the given path')

            if file_name is None:
                file_name = os.path.basename(file)

            async with aiofiles.open(file, 'rb') as file:
                file = await file.read()

        elif not isinstance(file, bytes):
            raise TypeError('File argument must be a file path or bytes')

        if file_name is None:
            raise ValueError('File name is not set')

        if mime is None:
            mime = file_name.split('.')[-1]

        result = await self.client.request_send_file(file_name, len(file), mime)
        id = result.id
        index = 0
        dc_id = result.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        while index < total:
            data = file[index * chunk: index * chunk + chunk]
            try:
                result = await self.session.post(
                    url=upload_url,
                    headers={
                        'auth': self.client.auth,
                        'file-id': id,
                        'total-part': str(total),
                        'part-number': str(index + 1),
                        'chunk-size': str(len(data)),
                        'access-hash-send': access_hash_send
                    },
                    data=data,
                    proxy=self.client.proxy,
                )
                result = await result.json()
                self.client.logger.info(rf'UploadFile({file_name}) | Messenger | response={result}')

                if result.get('status') == 'ERROR_TRY_AGAIN':
                    result = await self.client.request_send_file(file_name, len(file), mime)
                    id = result.id
                    index = 0
                    dc_id = result.dc_id
                    total = int(len(file) / chunk + 1)
                    upload_url = result.upload_url
                    access_hash_send = result.access_hash_send
                    continue

                if callable(callback):
                    try:
                        if inspect.iscoroutinefunction(callback):
                            await callback(len(file), index * chunk)

                        else:
                            callback(len(file), index * chunk)

                    except exceptions.CancelledError:
                        return None

                    except Exception:
                        pass

                index += 1

            except asyncio.TimeoutError:
                continue

            except aiohttp.ContentTypeError:
                result = await self.client.request_send_file(file_name, len(file), mime)
                id = result.id
                index = 0
                dc_id = result.dc_id
                total = int(len(file) / chunk + 1)
                upload_url = result.upload_url
                access_hash_send = result.access_hash_send
                print('UploadError | Try Again...')
                await asyncio.sleep(5)

            except Exception:
                self.client.logger.error(
                    f'UploadFile({file_name}) | Messenger | raised an exception',
                    extra={'data': self.wss_url}, exc_info=True)

        status = result['status']
        status_det = result['status_det']

        if status == 'OK' and status_det == 'OK':
            result = {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            }

            return Update(result)

        raise exceptions(status_det)(result, request=result)

    async def download(
            self,
            dc_id: int,
            file_id: int,
            access_hash: str,
            size: int,
            chunk: int = 131072,
            callback=None,
            gather: bool = False
    ) -> bytes:
        """
        Download a file from Rubika.

        Parameters:
        - dc_id: Data center ID.
        - file_id: File ID.
        - access_hash: Access hash of the file.
        - size: Total size of the file.
        - chunk: Chunk size for downloading.
        - callback: Progress callback.
        - gather: Whether to use asyncio.gather for concurrent downloading.

        Returns:
        Downloaded file content.
        """
        headers = {
            'auth': self.client.auth,
            'access-hash-rec': access_hash,
            'file-id': str(file_id),
            'user-agent': self.client.user_agent
        }

        base_url = f'https://messenger{dc_id}.iranlms.ir'

        async def fetch_chunk(session, start_index, last_index):
            chunk_headers = headers.copy()
            chunk_headers.update({'start-index': str(start_index), 'last-index': str(last_index)})
            try:
                async with session.post('/GetFile.ashx', headers=chunk_headers, proxy=self.client.proxy) as response:
                    if response.status != 200:
                        self.client.logger.warning(f'Download failed with status {response.status}')
                        return b''
                    return await response.read()
            except Exception as e:
                self.client.logger.error('DownloadFile | Messenger | raised an exception',
                                        extra={'data': chunk_headers, 'exception': str(e)}, exc_info=True)
                return b''

        async with aiohttp.ClientSession(base_url=base_url, connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            if gather:
                tasks = []
                for start_index in range(0, size, chunk):
                    last_index = min(start_index + chunk, size) - 1
                    tasks.append(fetch_chunk(session, start_index, last_index))
                
                result = await asyncio.gather(*tasks)
                result = b''.join(result)

                if callable(callback):
                    if inspect.iscoroutinefunction(callback):
                        await callback(size, len(result))
                    else:
                        callback(size, len(result))
            else:
                result = b''
                start_index = 0
                while start_index < size:
                    last_index = min(start_index + chunk, size) - 1
                    data = await fetch_chunk(session, start_index, last_index)
                    if not data:
                        break

                    result += data
                    start_index = last_index + 1

                    if callable(callback):
                        if inspect.iscoroutinefunction(callback):
                            await callback(size, len(result))
                        else:
                            callback(size, len(result))

        return result
