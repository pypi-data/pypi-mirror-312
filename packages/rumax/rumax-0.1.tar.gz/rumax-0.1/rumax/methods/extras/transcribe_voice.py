import rumax

class TranscribeVoice:
    async def transcribe_voice(
            self: "rumax.Client",
            object_guid: str,
            message_id: str,
    ) -> rumax.types.Update:
        """
        Transcribes voice messages.

        Parameters:
            - object_guid (str): The GUID of the object (chat, channel, or group) containing the voice message.
            - message_id (str): The ID of the voice message.

        Returns:
            rumax.types.Update: The transcription result.
        """
        return await self.builder(
            name='transcribeVoice',
            input=dict(object_guid=object_guid, message_id=message_id)
        )
