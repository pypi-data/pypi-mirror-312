import rumax

class TerminateSession:
    """
    Provides a method to terminate a user session.

    Methods:
    - terminate_session: Terminate a user session.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def terminate_session(
            self: "rumax.Client",
            session_key: str,
    ) -> rumax.types.Update:
        """
        Terminate a user session.

        Parameters:
        - session_key (str): The session key of the session to be terminated.

        Returns:
        - rumax.types.Update: The updated user information after terminating the session.
        """
        return await self.builder('terminateSession',
                                  input={'session_key': session_key})  # type: ignore
