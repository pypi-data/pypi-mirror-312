from typing import Union
import rumax

class RequestSendFile:
    """
    Provides a method to request sending a file.

    Methods:
    - request_send_file: Request sending a file.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def request_send_file(
            self: "rumax.Client",
            file_name: str,
            size: Union[str, int, float],
            mime: str = None,
    ) -> rumax.types.Update:
        """
        Request sending a file.

        Parameters:
        - file_name (str): The name of the file to be sent.
        - size (Union[str, int, float]): The size of the file to be sent.
        - mime (str, optional): The MIME type of the file. If None, it will be derived from the file name.

        Returns:
        - rumax.types.Update: The update indicating the success of the file sending request.
        """
        input = {
            'file_name': file_name,
            'size': int(size),
            'mime': file_name.split('.')[-1] if mime is None else mime
        }
        return await self.builder('requestSendFile', input=input)
