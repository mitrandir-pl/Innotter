import pytest
from rest_framework.exceptions import NotFound
from users.services import BaseService


class TestUserServices:

    @pytest.mark.django_db
    def test_user_not_found_exception(self):
        base_service = BaseService()
        with pytest.raises(NotFound):
            base_service.get_user_by_id(1)

    @pytest.mark.django_db
    def test_page_not_found_exception(self):
        base_service = BaseService()
        with pytest.raises(NotFound):
            base_service.get_page_by_id(1)
