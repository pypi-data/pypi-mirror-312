import rumax

class GetRelatedObjects:
    async def get_related_objects(
            self: "rumax.Client",
            object_guid: str,
    ) -> rumax.types.Update:
        """
        Get related objects for a given object.

        Args:
            object_guid (str): The GUID of the object.

        Returns:
            rumax.types.Update: The update containing information about related objects.
        """
        return await self.builder(name='getRelatedObjects', input=dict(object_guid=object_guid))
