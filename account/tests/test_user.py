from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import User
import random, string
from core.models import Role, Section, WorkGroup


class UserTests(APITestCase):
    
    def setUp(self) -> None:
        self.section = Section.objects.create(title=self.random_lower_string())
        self.role = Role.objects.create(section=self.section, title=self.random_lower_string())
        self.work_group = WorkGroup.objects.create(title=self.random_lower_string(), daily=0, overtime=0)
        self.user = User.objects.create_user(**self.get_data(through_orm=True))
    
    
    def test_create_user(self) -> None:
        """ Ensure we can create a new user """
        
        access_token = self.get_access_token()
        
        url = reverse("api:account:user-list")
        
        user_count = User.objects.count()
        
        self.client.force_authenticate(user=self.user, token=access_token)
        data = self.get_data()
        response = self.client.post(url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_count + 1, User.objects.count())
        
        
    def test_retrieve_users(self) -> None:
        """ Test retrieving all users """
        
        access_token = self.get_access_token()
        
        url = reverse("api:account:user-list")
        self.client.force_authenticate(user=self.user, token=access_token)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_retrieve_user(self) -> None:
        """ Test retrieve a user """
        
        access_token = self.get_access_token()
                
        data = self.get_data(through_orm=True)
        user = User.objects.create(**data)
        url = reverse("api:account:user-detail", kwargs={"username": user.username})
        self.client.force_authenticate(user=self.user, token=access_token)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["username"], user.username)
        
    
    def get_access_token(self) -> str:
        """ Get access token for forcing authentication """
        
        obtain_token_url = reverse("api:account:user-token_obtain_pair")
        user_data = {
            "username": self.user.username,
            "password": "12345600aa",
        }
        token_response = self.client.post(obtain_token_url, user_data, format="json")
        
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(token_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        access_token = token_response.json()["access"]
        return access_token


    def random_lower_string(self) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=16))
    
    def random_numeric_string(self) -> str:
        return "".join(random.choices(string.digits, k=16))
    
    def random_email(self) -> str:
        return f"{self.random_lower_string()}@{self.random_lower_string()}.com"
    
    def get_data(self, through_orm=False) -> dict:
        
        if through_orm:
            section = self.section
            role = self.role
            work_group = self.work_group
        else:
            section = self.section.id
            role = self.role.id
            work_group = self.work_group.id
        
        return {
            "password": "12345600aa",
            "last_login": "2021-07-07T16:02:20.900Z",
            "is_superuser": True,
            "username": self.random_lower_string(),
            "first_name": self.random_lower_string(),
            "last_name": self.random_lower_string(),
            "is_staff": True,
            "is_active": True,
            "date_joined": "2021-07-07T16:02:20.900Z",
            "father": self.random_lower_string(),
            "father_job": self.random_lower_string(),
            "father_mobile": self.random_lower_string(),
            "child": 0,
            "meli": self.random_numeric_string()[:9],
            "id_number": self.random_numeric_string()[:9],
            "id_place": self.random_lower_string(),
            "card_number": self.random_numeric_string(),
            "account_number": self.random_numeric_string(),
            "shaba_number": self.random_numeric_string(),
            "branch_code": self.random_numeric_string(),
            "insurance_number": self.random_numeric_string(),
            "phone_number": self.random_numeric_string(),
            "tel": self.random_numeric_string(),
            "emergency_mobile": self.random_numeric_string(),
            "email": self.random_email(),
            "marriage": 1,
            "education_level": 1,
            "sex": 1,
            "military_service": 1,
            "status": 1,
            "postal_code": self.random_numeric_string(),
            "birth_place": self.random_lower_string(),
            "address": self.random_lower_string(),
            "birth_date": "2021-07-07",
            "start_work": "2020-07-07",
            "section": section,
            "role": role,
            "work_group": work_group,
        }
 