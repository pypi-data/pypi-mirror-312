import rumax

class LeaveGroup:
    async def leave_group(
            self: "rumax.Client",
            group_guid: str,
    ) -> rumax.types.Update:
        """
        Leave a group.

        Args:
        - group_guid (str): The GUID of the group.

        Returns:
        - rumax.types.Update: Update object confirming the leave group action.
        """
        return await self.builder('leaveGroup', input={'group_guid': group_guid})
