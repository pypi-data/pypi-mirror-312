import rumax


class GetGroupOnlineCount:
    async def get_group_online_count(self: "rumax.Client", group_guid: str):
        return await self.builder('getGroupOnlineCount', input=dict(group_guid=group_guid))