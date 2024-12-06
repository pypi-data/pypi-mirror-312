import rumax

class GetObjectByUsername:
    async def get_object_by_username(
            self: "rumax.Client",
            username: str,
    ) -> rumax.types.Update:
        """
        Get an object (user, group, or channel) by its username.

        Args:
            username (str): The username of the object.

        Returns:
            rumax.types.Update: The update containing information about the object.
        """
        username = username.replace('@', '')
        return await self.builder('getObjectByUsername',
                                  input={
                                      'username': username,
                                  })
