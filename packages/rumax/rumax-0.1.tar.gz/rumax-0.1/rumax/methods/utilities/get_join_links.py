import rumax


class GetJoinLinks:
    async def get_join_links(self: "rumax.Client", object_guid: str):
        return await self.builder('getJoinLinks', input=dict(object_guid=object_guid))