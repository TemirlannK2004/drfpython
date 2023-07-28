from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from RepPro import settings
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
TutorUser  and ClientUser == get_user_model()


class ClientUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('id', 'email', 'username', 'password', 'avatar', 'age', 'gender', 'phone', 'rating')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = ClientUser.objects.create_user(**validated_data)
        return user







class TutorUserCreateSerializer(UserCreateSerializer):
    """ Tutor Sign Up using Djoser JWT """
    class Meta(UserCreateSerializer.Meta):
        model = TutorUser
        fields = ('id','email','first_name','last_name','phone_number','password')



class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Create Review for a Tutor """
    tutor = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = Review
        fields = '__all__'

class ReviewViewSerializer(serializers.ModelSerializer):
    """ Display All Tutor Reviews """    
    client_name = serializers.CharField(source='client.get_full_name', read_only=True)
    class Meta:
        model = Review
        fields = ('client_name','description','rating','created_at')

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class TutorUserProfile(serializers.ModelSerializer):

    """ Display Tutor Profile for Client """
    def get_average_rating(self, tutor):
        reviews = tutor.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(),2) if reviews.count() > 0 else 0.0
    average_rating = serializers.SerializerMethodField('get_average_rating')
    reviews = ReviewViewSerializer(many=True,read_only=True)

    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        return [course.name for course in obj.courses.all()]


    class Meta:
        model = TutorUser
        fields = ('first_name','last_name','email','phone_number','bio','avatar','files','date_of_birth','experience','education','degree','courses','yof','salary','link','average_rating','reviews')



class UpdateUserSerializer(serializers.ModelSerializer):
    """ Update Tutor Profile """
    tutor_user_model=get_user_model()
    def getEmail(self, tutor_user_model):
        return tutor_user_model.email
    def getFirstName(self, tutor_user_model):
        return tutor_user_model.first_name
    def getLastName(self, tutor_user_model):
        return tutor_user_model.last_name
    def getPhone(self, tutor_user_model):
        return tutor_user_model.phone_number
    

    email = serializers.SerializerMethodField("getEmail")
    first_name = serializers.SerializerMethodField("getFirstName")
    last_name = serializers.SerializerMethodField("getLastName")
    phone_num = serializers.SerializerMethodField("getPhone")



    class Meta:
        model = TutorUser
        fields = ('email','first_name','last_name','phone_num','bio','date_of_birth','experience','education','degree','yof','courses','salary','link','activate_post')

    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses')

        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
        
        for course_data in courses_data:
            course = Courses.objects.get_or_create(title=course_data['course']['name'])[0]
            TutorCourses.objects.get_or_create(tutor=instance, course=course)

        instance.bio = validated_data['bio']
        instance.date_of_birth = validated_data['date_of_birth']
        instance.experience =validated_data['experience']
        instance.education= validated_data['education']
        instance.degree = validated_data['degree']
        instance.yof = validated_data['yof']
        instance.salary = validated_data['salary']
        instance.link = validated_data['link']
        instance.activate_post = validated_data['activate_post']
        instance.save()
        return instance


class TutorListSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    def get_courses(self, obj):
        return [course.name for course in obj.courses.all()]
    """Display All Active Tutors """
    def get_average_rating(self, tutor):
        reviews = tutor.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(),2) if reviews.count() > 0 else 0.0
    average_rating = serializers.SerializerMethodField('get_average_rating')

    class Meta:
        model = TutorUser
        fields = ('id','first_name','last_name','bio','salary','avatar','average_rating','experience','courses')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom URL for SignIn Tutor JWT """
    def validate(self, attrs):
        data = super().validate(attrs)
        return data