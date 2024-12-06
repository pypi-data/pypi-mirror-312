import rumax

class GetUpdates:
    async def get_updates(self: "rumax.Client") -> "rumax.types.Update":
        """
        Get updates from the server.

        Returns:
        - rumax.types.Update: An Update object containing information about the updates.
        """

        return await self.connection.get_updates()
