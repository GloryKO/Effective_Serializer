from .models import *
from rest_framework import serializers

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
        
        #to deserialize data
        def to_internal_values(self,data):
            resource_data = data['resource']
            return super().to_internal_values(resource_data)
        