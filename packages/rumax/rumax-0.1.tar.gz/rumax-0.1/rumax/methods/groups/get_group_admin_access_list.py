import rumax

class GetGroupAdminAccessList:
    async def get_group_admin_access_list(
            self: "rumax.Client",
            group_guid: str,
            member_guid: str,
    ) -> rumax.types.Update:
        """
        Get the admin access list for a member in a group.

        Args:
        - group_guid (str): The GUID of the group.
        - member_guid (str): The GUID of the member for whom admin access is being checked.

        Returns:
        - rumax.types.Update: The result of the API call.
        """
        return await self.builder('getGroupAdminAccessList',
                                  input={
                                      'group_guid': group_guid,
                                      'member_guid': member_guid,
                                  })
