from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import *
from tabs.models import Result
import json
from datetime import datetime, timedelta

# class PassValidTest(TestCase):

#     def test_count_validators(self):
#         validators = get_default_password_validators()
#         self.assertEqual(len(validators), 4)

#     def test_no_vaidation(self):
#         # This password is common and too short
#         self.assertIsNone(validate_password('admin', password_validators=[]))

#     def test_length_password(self):
#         self.assertIsNone(validate_password('passwordlongerthan8'))
#         with self.assertRaises(ValidationError) as context:
#             validate_password('short')
#         self.assertTrue('This password is too short. It must contain at least 8 characters.' in context.exception)

#     def test_numeric_password(self):
#         with self.assertRaises(ValidationError) as context:
#             validate_password('123456789')
#         self.assertTrue('This password is entirely numeric.' in context.exception)

#     def test_common_password(self):
#         with self.assertRaises(ValidationError) as context:
#             validate_password('password')
#         self.assertTrue('This password is too common.' in context.exception)

#     def test_similar_login_password(self):
#         user = User.objects.create(username='testpiotrek',
#                                    password='testpiotr')

#         with self.assertRaises(ValidationError) as context:
#             UserAttributeSimilarityValidator().validate('testpiotrek', user=user),
#         error = "The password is too similar to the username."
#         self.assertTrue(error in context.exception)

class ResultTest(TestCase):
    def setUp(self):
        self.credentials1 = {
            'username': 'User1',
            'password': 'edctgbujm'}
        self.credentials2 = {
            'username': 'User2',
            'password': 'edctgbujm'}
        self.credentials3 = {
            'username': 'User3',
            'password': 'edctgbujm'}
        self.user1 = User.objects.create_user(**self.credentials1)
        self.user2 = User.objects.create_user(**self.credentials2)
        self.user3 = User.objects.create_user(**self.credentials3)
        self.c = Client()

    def test_match_result_success(self):
        result = Result.objects.create(
            date=datetime.today() - timedelta(days=1),
            player_1=self.user1,
            player_2=self.user2,
            winner=self.user1
        )
        try:
            result.full_clean()
        except ExceptionType:
            self.fail("Full_clean() raised ExceptionType unexpectedly!")
        self.assertEqual(result.player_1, self.user1)
        self.assertEqual(result.player_2, self.user2)

    def test_match_result_fail_same_user(self):
        result = Result(
            date=datetime.today() - timedelta(days=1),
            player_1=self.user1,
            player_2=self.user1,
            winner=self.user1
        )   
        with self.assertRaises(ValidationError) as context:
            result.full_clean()
        self.assertIn('Player 1 and Player 2 are the same.', context.exception.messages)
    
    def test_match_result_fail_date(self):
        result = Result(
            date=datetime.today() + timedelta(days=1),
            player_1=self.user1,
            player_2=self.user2,
            winner=self.user1
        )   
        with self.assertRaises(ValidationError) as context:
            result.full_clean()
        self.assertIn('Seems like this match happened in future. Date of the match > current time ',
                      context.exception.messages)
    
    def test_match_result_fail_winner_not_played(self):
        result = Result(
            date=datetime.today(),
            player_1=self.user1,
            player_2=self.user2,
            winner=self.user3
        )   
        with self.assertRaises(ValidationError) as context:
            result.full_clean()
        self.assertIn('Winner didnt participate in this match.',
                      context.exception.messages)
