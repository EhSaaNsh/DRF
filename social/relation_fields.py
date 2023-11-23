from rest_framework.serializers import RelatedField

class UserNameRelationField(RelatedField):
    def to_representation(self, value):
        return value.username