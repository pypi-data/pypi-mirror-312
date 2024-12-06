import rumax

class GetStickerSetByID:
    """
    Provides a method to get a sticker set by its ID.

    Methods:
    - get_sticker_set_by_id: Get a sticker set by its ID.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_sticker_set_by_id(
            self: "rumax.Client",
            sticker_set_id: str,
    ) -> "rumax.types.Update":
        """
        Get a sticker set by its ID.

        Parameters:
        - sticker_set_id (str): The ID of the sticker set.

        Returns:
        - The sticker set corresponding to the provided ID.
        """
        return await self.builder(
            name='getStickerSetByID',
            input={'sticker_set_id': str(sticker_set_id)}
        )
