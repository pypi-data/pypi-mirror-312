import rumax
from rumax.types import Update

class GetPrivacySetting:
    """
    Provides a method to get the current user's privacy setting.

    Methods:
    - get_privacy_setting: Get the current user's privacy setting.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def get_privacy_setting(
            self: "rumax.Client"
    ) -> Update:
        """
        Get the current user's privacy setting.

        Returns:
        - rumax.types.Update: The current user's privacy setting.
        """
        return await self.builder('getPrivacySetting')  # type: ignore
