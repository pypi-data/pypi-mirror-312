import rumax
from rumax.types import Update

class GetBlockedUsers:
    """
    Provides a method to get a list of blocked users.

    Methods:
    - get_blocked_users: Get a list of blocked users.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_blocked_users(
            self: "rumax.Client"
    ) -> Update:
        """
        Get a list of blocked users.

        Returns:
        - rumax.types.Update: List of blocked users.
        """
        return await self.builder('getBlockedUsers')  # type: ignore
