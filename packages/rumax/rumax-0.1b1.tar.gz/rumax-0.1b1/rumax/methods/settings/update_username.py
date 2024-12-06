import rumax

class UpdateUsername:
    """
    Provides a method to update the username of the user.

    Methods:
    - update_username: Update the username of the user.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def update_username(
            self: "rumax.Client",
            username: str
    ) -> rumax.types.Update:
        """
        Update the username of the user.

        Parameters:
        - username (str): The new username for the user.

        Returns:
        - rumax.types.Update: The updated user information after the username update.
        """
        return await self.builder('updateUsername', input={'username': username.replace('@', '')})
