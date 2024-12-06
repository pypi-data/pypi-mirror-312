import rumax

class GetPollStatus:
    """
    Provides a method to get the status of a specific poll.

    Methods:
    - get_poll_status: Get the status of a specific poll.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_poll_status(
            self: "rumax.Client",
            poll_id: str,
    ) -> rumax.types.Update:
        """
        Get the status of a specific poll.

        Parameters:
        - poll_id (str): The ID of the poll for which the status is requested.

        Returns:
        - rumax.types.Update: The status of the specified poll.
        """
        return self.builder(name='getPollStatus',
                            input={
                                'poll_id': poll_id,
                            })
