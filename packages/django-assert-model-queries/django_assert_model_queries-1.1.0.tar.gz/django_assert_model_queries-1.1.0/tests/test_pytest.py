import pytest
from _pytest.outcomes import Failed
from django.db.models import Count

from tests.testapp.models import Community


class TestPytestIntegration:
    @pytest.mark.django_db
    def test_assert_model_queries(self, assert_model_queries):
        with assert_model_queries({"testapp.Community": 1}):
            Community.objects.create(name="test")
        with assert_model_queries({"testapp.Community": 1}):
            Community.objects.update(name="new")
        with assert_model_queries({"testapp.Community": 1}):
            Community.objects.get(name="new")
        with assert_model_queries({"testapp.Community": 1}):
            Community.objects.aggregate(count=Count("id"))
        with assert_model_queries(
            {
                "testapp.Community": 2,
                "testapp.Chapter": 1,
                "testapp.Community_topics": 1,
            }
        ):
            Community.objects.all().delete()

    @pytest.mark.django_db
    def test_handle_assertion_fail(self, assert_model_queries):
        with pytest.raises(Failed):
            with assert_model_queries({"testapp.Community": 0}):
                Community.objects.create(name="test")
