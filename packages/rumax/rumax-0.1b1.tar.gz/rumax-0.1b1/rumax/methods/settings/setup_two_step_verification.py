from typing import Union
import rumax

class SetupTwoStepVerification:
    """
    Provides a method to set up two-step verification for the user.

    Methods:
    - setup_two_step_verification: Set up two-step verification for the user.

    Attributes:
    - self (rumax.Client): The rumax client instance.
    """

    async def setup_two_step_verification(
            self: "rumax.Client",
            password: Union[int, str],
            hint: str = None,
            recovery_email: str = None,
    ) -> rumax.types.Update:
        """
        Set up two-step verification for the user.

        Parameters:
        - password (Union[int, str]): The current user password.
        - hint (str): A hint to help remember the password.
        - recovery_email (str): The recovery email for two-step verification.

        Returns:
        - rumax.types.Update: The updated user information after setting up two-step verification.
        """
        return await self.builder(name='setupTwoStepVerification',
                                  input={'password': str(password),
                                         'hint': hint,
                                         'recovery_email': recovery_email})  # type: ignore
