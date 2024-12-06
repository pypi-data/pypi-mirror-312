import rumax
from rumax.types import Update

class DeleteAvatar:
    async def delete_avatar(
            self: "rumax.Client",
            object_guid: str,
            avatar_id: str,
    ) -> Update:
        """
        Delete an avatar.

        Parameters:
        - object_guid (str): The unique identifier of the object (e.g., user, chat) that owns the avatar.
        - avatar_id (str): The identifier of the avatar to be deleted.

        Returns:
        rumax.types.Update: The result of the API call.
        """
        return await self.builder('deleteAvatar',
                                  input={
                                      'object_guid': object_guid,
                                      'avatar_id': avatar_id,
                                  })
