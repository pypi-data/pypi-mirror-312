import rumax
from typing import Optional, Union

class GetContacts:
    async def get_contacts(
            self: "rumax.Client",
            start_id: Optional[Union[str, int]] = None,
    ) -> rumax.types.Update:
        """
        Get a list of contacts.

        Args:
            self ("rumax.Client"): The rumax client.
            start_id (Optional[Union[str, int]], optional): Start ID for pagination. Defaults to None.

        Returns:
            rumax.types.Update: The result of the API call.
        """
        return self.builder(name='getContacts', input={'start_id': str(start_id)})
