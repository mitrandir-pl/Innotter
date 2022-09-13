from datetime import datetime
from rest_framework import exceptions
from pages.serializers import PageSerializer, PageSimpleSerializer
from pages.models import Page
from users.models import User
from core.error_messages import WRONG_DATE_MESSAGE


class ModeratorService:
    def block_page(self, data: dict[str: str], user_pk: int):
        date = data.get('unblock_date', '')
        try:
            unblock_date_list = list(map(lambda x: int(x), date.split()))
            unblock_date = datetime(*unblock_date_list)
        except TypeError:
            raise exceptions.ValidationError(WRONG_DATE_MESSAGE)
        page = Page.objects.get(pk=user_pk)
        page.unblock_date = unblock_date
        data = PageSimpleSerializer(page).data
        serialized_page = PageSimpleSerializer(instance=page, data=data)
        if serialized_page.is_valid(raise_exception=True):
            serialized_page.save()
            return serialized_page


class AdminService(ModeratorService):
    def block_user(self, user_pk: int):
        user = User.objects.get(pk=user_pk)
        user.is_blocked = True
        user.save()
