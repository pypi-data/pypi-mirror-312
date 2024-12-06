import rumax
from rumax.types import Update

class GetMySessions:
    """
    Provides a method to get information about the current user's sessions.

    Methods:
    - get_my_sessions: Get information about the current user's sessions.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_my_sessions(
            self: "rumax.Client"
    ) -> Update:
        """
        Get information about the current user's sessions.

        Returns:
        - rumax.types.Update: Information about the user's sessions.
        """
        return await self.builder('getMySessions', input={})  # type: ignore
