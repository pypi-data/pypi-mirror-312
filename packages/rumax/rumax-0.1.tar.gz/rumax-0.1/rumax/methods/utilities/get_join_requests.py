import rumax


class GetJoinRequests:
    async def get_join_requests(self: "rumax.Client", object_guid: str):
        return await self.builder('getJoinRequests', input=dict(object_guid=object_guid))