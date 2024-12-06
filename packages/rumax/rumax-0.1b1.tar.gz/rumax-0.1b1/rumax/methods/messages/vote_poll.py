from typing import Union
import rumax

class VotePoll:
    async def vote_poll(
            self: "rumax.Client",
            poll_id: str,
            selection_index: Union[str, int],
    ) -> rumax.types.Update:
        """
        Vote on a poll option.

        Args:
            poll_id (str): The ID of the poll.
            selection_index (Union[str, int]): The index of the option to vote for.

        Returns:
            rumax.types.Update: The update indicating the success of the vote.
        """
        return await self.builder('votePoll',
                                  input={
                                      'poll_id': poll_id,
                                      'selection_index': int(selection_index),
                                  })
