from django.core import exceptions
from rest_framework.exceptions import NotFound
from users.models import User
from pages.models import Page


class BaseService:
    def get_user_by_id(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except exceptions.ObjectDoesNotExist:
            raise NotFound

    def get_page_by_id(self, pk):
        try:
            page = Page.objects.get(pk=pk)
            return page
        except exceptions.ObjectDoesNotExist:
            raise NotFound


class ModeratorService(BaseService):
    def block_page(self, data, user_pk):
        unblock_date = data.get('unblock_date', '')
        page = self.get_page_by_id(user_pk)
        page.unblock_date = unblock_date
        try:
            page.save()
        except exceptions.ValidationError:
            return None


class AdminService(ModeratorService):
    def block_user(self, user_pk):
        user = self.get_user_by_id(user_pk)
        if user:
            user.is_blocked = True
            user.save()
            return user
        else:
            return None
