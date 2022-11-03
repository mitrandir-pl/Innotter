from datetime import datetime
from pages.serializers import PageSerializer, PageSimpleSerializer
from pages.models import Page
from users.models import User


class ModeratorService:
    def block_page(self, data: dict[str: str], user_pk: int) -> PageSimpleSerializer:
        """
        Method gets page by pk, set an unblock_date.
        Check if date is valid with the serializer, and if it's okay,
        returns serialized page.
        """
        unblock_date_str = data.get('unblock_date')
        unblock_date = datetime.strptime(unblock_date_str,
                                         '%Y-%m-%d %H:%M:%S')
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
