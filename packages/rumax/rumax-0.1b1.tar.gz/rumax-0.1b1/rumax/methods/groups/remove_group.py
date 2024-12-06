import rumax

class RemoveGroup:
    async def remove_group(
            self: "rumax.Client",
            group_guid: str,
    ) -> rumax.types.Update:
        """
        Remove a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rumax.types.Update: Update object confirming the removal of the group.
        """
        return await self.builder('removeGroup', input={'group_guid': group_guid})
