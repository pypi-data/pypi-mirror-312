from time import time
from typing import Optional, Union
import rumax

class GetContactsUpdates:
    async def get_contacts_updates(
            self: "rumax.Client",
            state: Optional[Union[str, int]] = round(time()) - 150,
    ) -> rumax.types.Update:
        """
        Get updates related to contacts.

        Args:
            self (rumax.Client): The rumax client.
            state (Optional[Union[str, int]], optional):
                The state parameter to filter updates. Defaults to `round(time()) - 150`.

        Returns:
            rumax.types.Update: The update related to contacts.
        """
        return await self.builder(name='getContactsUpdates',
                                  input={'state': int(state)})
