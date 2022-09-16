from datetime import datetime
from rest_framework import exceptions
from pages.serializers import PageSerializer, PageSimpleSerializer
from pages.models import Page
from users.models import User
from core.error_messages import WRONG_DATE_MESSAGE


class ModeratorService:
    def block_page(self, data: dict[str: str], user_pk: int) -> PageSimpleSerializer:
        """
        Method gets page by pk, set an unblock_date.
        Check if date is valid with the serializer, and if it's okay,
        returns serialized page.
        """
        unblock_date = self.get_date(data)
        page = Page.objects.get(pk=user_pk)
        page.unblock_date = unblock_date
        data = PageSimpleSerializer(page).data
        serialized_page = PageSimpleSerializer(instance=page, data=data)
        if serialized_page.is_valid(raise_exception=True):
            serialized_page.save()
            return serialized_page

    def get_date(self, data: dict[str: str]) -> datetime:
        """
        Method takes a dict, get values
        (year, month, day and etc.), from it
        and returns it in datetime format.
        """
        year = data.get('year', 0)
        month = data.get('day', 0)
        day = data.get('day', 0)
        hour = data.get('hour', 0)
        minute = data.get('minute', 0)
        try:
            unblock_date_list = [year, month, day, hour, minute]
            unblock_date = datetime(*[int(i) for i in unblock_date_list])
            return unblock_date
        except TypeError:
            raise exceptions.ValidationError(WRONG_DATE_MESSAGE)


class AdminService(ModeratorService):
    def block_user(self, user_pk: int):
        user = User.objects.get(pk=user_pk)
        user.is_blocked = True
        user.save()
