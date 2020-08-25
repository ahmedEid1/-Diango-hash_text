from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import Hash
from django.core.exceptions import ValidationError

from time import sleep


class FunctionalTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter Hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn('3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392', self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        sleep(5)
        self.assertIn('3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCases(TestCase):

    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm({'text': 'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_work(self):
        text_hash = hashlib.sha3_256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual('3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392', text_hash)

    def save_hash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = '3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392'
        hash.save()
        return hash

    def test_hash_object(self):
        hash = self.save_hash()
        pulled_hash = Hash.objects.get(hash=hash.hash)
        self.assertEqual(pulled_hash.text, hash.text)

    def test_viewing_hash(self):
        hash = self.save_hash()
        response = self.client.get('/hash/3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = "3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392assdff"
            hash.full_clean()
        self.assertRaises(ValidationError, bad_hash)


