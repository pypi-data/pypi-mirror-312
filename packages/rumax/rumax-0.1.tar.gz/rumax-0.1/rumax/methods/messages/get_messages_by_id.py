from typing import Union
import rumax

class GetMessagesByID:
    """
    Provides a method to retrieve messages by their IDs.

    Methods:
    - get_messages_by_id: Retrieve messages by their IDs.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_messages_by_id(
            self: "rumax.Client",
            object_guid: str,
            message_ids: Union[str, list],
    ) -> rumax.types.Update:
        """
        Retrieve messages by their IDs.

        Parameters:
        - object_guid (str): The GUID of the object to which the messages belong.
        - message_ids (Union[str, list]): The ID or list of IDs of the messages to retrieve.

        Returns:
        - rumax.types.Update: The retrieved messages identified by their IDs.
        """
        if isinstance(message_ids, str):
            message_ids = [str(message_ids)]

        return await self.builder('getMessagesByID',
                                  input={
                                      'object_guid': object_guid,
                                      'message_ids': message_ids,
                                  })
