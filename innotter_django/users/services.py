from pages.serializers import PageSerializer, PageSimpleSerializer
from pages.models import Page
from users.models import User


class ModeratorService:
    def block_page(self, data, user_pk):
        unblock_date = data.get('unblock_date', 'missed_date')
        page = Page.objects.get(pk=user_pk)
        page.unblock_date = unblock_date
        data = PageSimpleSerializer(page).data
        serialized_page = PageSimpleSerializer(instance=page, data=data)
        if serialized_page.is_valid(raise_exception=True):
            serialized_page.save()
            return serialized_page


class AdminService(ModeratorService):
    def block_user(self, user_pk):
        user = User.objects.get(pk=user_pk)
        user.is_blocked = True
        user.save()
        return user
