import rumax

class GroupPreviewByJoinLink:
    async def group_preview_by_join_link(
            self: "rumax.Client",
            link: str,
    ) -> rumax.types.Update:
        """
        Get group preview by join link.

        Args:
        - link (str): The join link or hash link.

        Returns:
        - rumax.types.Update: Update object containing the group preview information.
        """
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('groupPreviewByJoinLink',
                                  input={
                                      'hash_link': link,
                                  })
