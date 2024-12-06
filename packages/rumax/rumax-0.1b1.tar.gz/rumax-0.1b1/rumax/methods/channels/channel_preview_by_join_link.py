import rumax
from rumax.types import Update

class ChannelPreviewByJoinLink:
    async def channel_preview_by_join_link(
        self: "rumax.Client",
        link: str,
    ) -> Update:
        """
        Get a preview of a channel using its join link.

        Parameters:
        - link (str): The join link or a link containing the channel's hash.

        Returns:
        rumax.types.Update: The result of the API call.
        """
        if '/' in link:
            link = link.split('/')[-1]

        return await self.builder('channelPreviewByJoinLink', input={'hash_link': link})
