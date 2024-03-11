from .models import *
from rest_framework import serializers


# THIS WHOLE FILE DESCRIBES HOW WE CAN USE SERIALIZERS MORE EFFECTIVELY

# 1. CUSTOM VALIDATIONS FOR FIELDS

class MovieSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Movie
        fields ='__all__'

    #custom field validation(checking the values for the rating field in the movie model)
    def validate_rating(self,value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating has to be between 0 and 10')
        return value
    
    #object-level validation (comparing two fields in the model)
    def validate(self,data):
        if data['gross_us'] > data['worldwide_gross'] :
            raise serializers.ValidatioError('US gross cannot be greater than worldwide gross.')
        return data
    
#2. CUSTOM OUTPUTS(using to_representation for serializing data)
    
    class ResourceSeraializer(serializers.ModelSerializer):
        class Meta:
            model = Resource
            fields='__all__'

        #to_representation for serializing data
        def to_representation(self,instance):
            representation = super().to_representation(instance)
            representation['likes']=instance.liked_by.count()
            return representation
        
        #to deserialize data using the to_internal_values method
        def to_internal_values(self,data):
            resource_data = data['resource']
            return super().to_internal_values(resource_data)

#3. USING THE SOURCE KEYWORD
    class UserSerializer(serializers.ModelSerializer):
        active  = serializers.BooleanField(source='is_active') #this field replaces the "is_active" field in the user model
        class Meta:
            model =User
            fields = ['id', 'username', 'email', 'is_staff', 'active','fullname']
        
        #second use case 
        full_name = serializers.CharField(source='get_full_name') #uses the get_full_name method present in the user model

    
    class UserSerializer(serializers.ModelSerializer): # this also uses the "source" keyword. this is made possible because the userprofile model has a one to one relationship with the User profile
        bio = serializers.CharField(source='userprofile.bio')
        birth_date = serializers.DateField(source='userprofile.birth_date')

        class Meta:
            model = User
            fields = [
            'id', 'username', 'email', 'is_staff',
            'is_active', 'bio', 'birth_date'
        ] 
            
#4 . SerializerMethod field
    
    class UserSerializer(serializers.ModelSerializer):
        full_name = serializers.SerializerMethodField()

        class Meta:
          model = User
          fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
