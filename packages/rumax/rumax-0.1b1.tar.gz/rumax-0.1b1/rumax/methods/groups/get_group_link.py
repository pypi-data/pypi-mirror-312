import rumax

class GetGroupLink:
    async def get_group_link(
            self,
            group_guid: str,
    ) -> rumax.types.Update:
        """
        Get the link associated with a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rumax.types.Update: Update object containing the group link.
        """
        return await self.builder('getGroupLink',
                                  input={
                                      'group_guid': group_guid,
                                  })
