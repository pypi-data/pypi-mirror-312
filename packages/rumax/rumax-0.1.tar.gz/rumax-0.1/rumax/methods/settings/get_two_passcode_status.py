import rumax
from rumax.types import Update

class GetTwoPasscodeStatus:
    """
    Provides a method to get the two-passcode status for the user.

    Methods:
    - get_two_passcode_status: Get the two-passcode status for the user.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_two_passcode_status(
            self: "rumax.Client"
    ) -> Update:
        """
        Get the two-passcode status for the user.

        Returns:
        - rumax.types.Update: The two-passcode status for the user.
        """
        return await self.builder('getTwoPasscodeStatus')  # type: ignore
