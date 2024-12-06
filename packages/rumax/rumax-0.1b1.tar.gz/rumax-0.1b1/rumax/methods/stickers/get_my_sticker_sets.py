import rumax

class GetMyStickerSets:
    """
    Provides a method to get the sticker sets owned by the user.

    Methods:
    - get_my_sticker_sets: Get the sticker sets owned by the user.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_my_sticker_sets(self: "rumax.Client") -> "rumax.types.Update":
        """
        Get the sticker sets owned by the user.

        Returns:
        - The sticker sets owned by the user.
        """
        return await self.builder('getMyStickerSets')
