import rumax
from typing import Literal


class ActionOnJoinRequest:
    async def action_on_join_request(self: "rumax.Client",
                                     object_guid: str,
                                     user_guid: str,
                                     action: Literal['Accept', 'Reject'] = 'Accept'):
        
        if action not in ('Accept', 'Reject'):
            raise ValueError('`action` can only be Accept or Reject.')

        data = dict(object_guid=object_guid,
                    object_type='Group' if object_guid.startswith('g0') else 'Channel',
                    user_guid=user_guid,
                    action=action)

        return await self.builder('actionOnJoinRequest', input=data)