import rumax
from rumax.types import Update

class GetSuggestedFolders:
    """
    Provides a method to get the suggested folders for the user.

    Methods:
    - get_suggested_folders: Get the suggested folders for the user.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_suggested_folders(
            self: "rumax.Client"
    ) -> Update:
        """
        Get the suggested folders for the user.

        Returns:
        - rumax.types.Update: The suggested folders for the user.
        """
        return await self.builder('getSuggestedFolders')  # type: ignore
