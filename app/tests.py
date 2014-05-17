from django.core.urlresolvers import reverse
from django.test import TestCase


class IndexViewTests(TestCase):
    def test_index_view_http_response(self):
        """
        Expect the index view to return a 200 response status code.
        """
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_with_no_quotes(self):
        """
        Expect a message to be displayed if no quotes have been submitted.
        """
        response = self.client.get(reverse('app:index'))
        self.assertContains(response, 'No quotes have been submitted.')
        self.assertQuerysetEqual(response.context['quote_list'], [])
