import rumax

class GetMyGifSet:
    async def get_my_gif_set(
            self: "rumax.Client"
    ) -> rumax.types.Update:
        """
        Gets the user's personal GIF set.

        Returns:
            rumax.types.Update: Information about the user's GIF set.
        """
        return await self.builder('getMyGifSet')
