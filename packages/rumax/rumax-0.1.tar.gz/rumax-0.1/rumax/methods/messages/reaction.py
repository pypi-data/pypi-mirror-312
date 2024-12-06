import rumax

class Reaction:
    """
    Provides a method to add a reaction to a specific message.

    Methods:
    - reaction: Add a reaction to a specific message.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def reaction(
            self: "rumax.Client",
            object_guid: str,
            message_id: str,
            reaction_id: int,
    ) -> rumax.types.Update:
        """
        Add a reaction to a specific message.

        Parameters:
        - object_guid (str): The GUID of the object associated with the message.
        - message_id (str): The ID of the message to which the reaction will be added.
        - reaction_id (int): The ID of the reaction to be added.

        Returns:
        - rumax.types.Update: The update indicating the success of adding the reaction.
        """
        return await self.action_on_message_reaction(
            object_guid=object_guid,
            message_id=message_id,
            action='Add',
            reaction_id=reaction_id,
        )
