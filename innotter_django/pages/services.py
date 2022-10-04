from pages.models import Page, Tag
from users.models import User
from users.serializers import UserSerializer


class PageService:

    def subscribe(self, user: User, page_pk: int) -> None:
        """
        Method gets user that made follow request
        And adds him into page followers if page is not private_page
        And in follow_requests if page is private
        """
        page = Page.objects.get(pk=page_pk)
        if page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)

    def get_follow_requests(self, page_pk: int) -> list[User]:
        """
        This method returns list of users, that
        made follow request for private page
        """
        page = Page.objects.get(pk=page_pk)
        if page.is_private:
            users = UserSerializer(page.follow_requests.all(), many=True)
            return users

    def allow_current_follow_request(self, data: dict[str: int], page_pk: int) -> None:
        """
        Method takes id of user and removes
        him from follow request to followers
        """
        page = Page.objects.get(pk=page_pk)
        follower_id = data.get('allow_following')
        follower = User.objects.get(pk=follower_id)
        page.followers.add(follower)
        page.follow_requests.remove(follower)

    def allow_all_follow_request(self, page_pk: int) -> None:
        """
        Method removes all users from follow requests to followers
        """
        page = Page.objects.get(pk=page_pk)
        for i in page.follow_requests.all():
            page.followers.add(i)
            page.follow_requests.remove(i)
