from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):

    cur_id = serializers.IntegerField
    current_name = serializers.CharField()
    official_rate = serializers.FloatField()
    date = serializers.DateField()
    abbreviation = serializers.CharField()
    dynamics = serializers.CharField()
