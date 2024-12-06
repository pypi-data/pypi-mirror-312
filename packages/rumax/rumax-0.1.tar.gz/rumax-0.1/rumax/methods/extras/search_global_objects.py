import rumax

class SearchGlobalObjects:
    async def search_global_objects(
            self: "rumax.Client",
            search_text: str,
    ) -> rumax.types.Update:
        """
        Search for global objects (users, channels, etc.) based on the given search text.

        Args:
            search_text (str): The text to search for.

        Returns:
            rumax.types.Update: The update containing search results.
        """
        return await self.builder('searchGlobalObjects',
                                  input={
                                      'search_text': search_text,
                                  })
