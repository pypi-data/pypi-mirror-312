import rumax


class CreateJoinLink:
    async def create_join_link(
            self: "rumax.Client",
            object_guid: str,
            expire_time: int = None,
            request_needed: bool = False,
            title: str = None,
            usage_limit: int = 0,
    ):

        data = dict(
            object_guid=object_guid,
            request_needed=request_needed,
            usage_limit=usage_limit,
        )

        if expire_time is not None and isinstance(expire_time, int):
            data['expire_time'] = expire_time
        
        if title is not None and isinstance(title, str):
            data['title'] = title

        if not isinstance(request_needed, bool):
            raise ValueError('`request_needed` must be of boolean type only')

        return await self.builder('createJoinLink', input=data)