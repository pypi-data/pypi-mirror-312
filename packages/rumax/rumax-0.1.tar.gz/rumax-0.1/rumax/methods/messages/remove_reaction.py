import rumax

class RemoveReaction:
    """
    Provides a method to remove a reaction from a specific message.

    Methods:
    - remove_reaction: Remove a reaction from a specific message.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def remove_reaction(
            self: "rumax.Client",
            object_guid: str,
            message_id: str,
            reaction_id: int,
    ) -> rumax.types.Update:
        """
        Remove a reaction from a specific message.

        Parameters:
        - object_guid (str): The GUID of the object associated with the message.
        - message_id (str): The ID of the message from which the reaction will be removed.
        - reaction_id (int): The ID of the reaction to be removed.

        Returns:
        - rumax.types.Update: The update indicating the success of removing the reaction.
        """
        return await self.action_on_message_reaction(
            object_guid=object_guid,
            message_id=message_id,
            action='Remove',
            reaction_id=reaction_id,
        )
