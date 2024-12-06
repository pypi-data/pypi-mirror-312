import rumax
from rumax.types import Update

class DeleteFolder:
    """
    Provides a method to delete a folder.

    Methods:
    - delete_folder: Delete a folder.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def delete_folder(
            self: "rumax.Client",
            folder_id: str,
    ) -> Update:
        """
        Delete a folder.

        Parameters:
        - folder_id (str): The ID of the folder to be deleted.

        Returns:
        - rumax.types.Update: Result of the delete folder operation.
        """
        return await self.builder(name='deleteFolder',
                                  input={'folder_id': str(folder_id)})  # type: ignore
