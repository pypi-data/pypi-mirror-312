import rumax
from typing import Union

class SetGroupDefaultAccess:
    async def set_group_default_access(
            self: "rumax.Client",
            group_guid: str,
            access_list: Union[str, list],
    ) -> rumax.types.Update:
        """
        Set default access for a group.

        Args:
        - group_guid (str): The GUID of the group.
        - access_list (Union[str, list]): List of allowed actions.

        Returns:
        - rumax.types.Update: Update object confirming the change in default access.
        """
        if isinstance(access_list, str):
            access_list = [access_list]

        return await self.builder('setGroupDefaultAccess',
                                  input={
                                      'group_guid': group_guid,
                                      'access_list': access_list,
                                  })
