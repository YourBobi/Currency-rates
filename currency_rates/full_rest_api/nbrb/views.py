import datetime

import requests
from drf_spectacular.utils import extend_schema
from full_rest_api.nbrb import serializers
from full_rest_api.nbrb.filter_parameters import current_currency
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from currency_rates.settings import NBRB_DYNAMICS_API_URL, NBRB_RATES_API_URL


class CatalogCompanyLinkViewSet(
    viewsets.GenericViewSet,
):

    serializer_class = serializers.CatalogCompanyLinkStatisticSerializer
    queryset = ''

    @staticmethod
    def _get_dynamics_data(cur_id, end_date):
        if end_date.weekday() == 0:
            start_date = end_date - datetime.timedelta(days=3)
        elif end_date.weekday() == 6:
            start_date = end_date - datetime.timedelta(days=2)
        else:
            start_date = end_date - datetime.timedelta(days=1)
        # get dynamics from nbrb
        dynamics = requests.get(
            url=NBRB_DYNAMICS_API_URL.format(cur_id),
            params={
                "startdate": start_date.strftime('%Y-%m-%d'),
                "enddate": end_date.strftime('%Y-%m-%d'),
            },
        ).json()
        if dynamics:
            result = dynamics[-1].get('Cur_OfficialRate') - dynamics[0].get('Cur_OfficialRate')
            if result > 0:
                return f"The course was full on {round(result, 3)}"
            elif result < 0:
                return f"The rate fell by {round(result, 3)}"
            else:
                return "Уxchange rate unchanged"
        return "No information"

    def __normalize_data(self, data):
        end_date = datetime.datetime.fromisoformat(data.get('Date')).date()
        return {
            'cur_id': data.get('Cur_ID'),
            'current_name': data.get('Cur_Name'),
            'official_rate': data.get('Cur_OfficialRate'),
            'date': end_date.strftime('%Y-%m-%d'),
            'abbreviation': data.get('Cur_Abbreviation'),
            'dynamics': self._get_dynamics_data(
                cur_id=data.get('Cur_ID'),
                end_date=end_date,
            ),
        }

    def __check_api_request(self, response):
        if response.status_code == 404 or not self.request.query_params.get('currency_code'):
            return Response(
                {'error': 'Incorrect currency_code'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif response.status_code == 400:
            return Response(
                {'error': 'Incorrect date'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        description='Get a list.',
        tags=['NBRB'],
        parameters=[
            *current_currency,
        ]
    )
    @action(methods=['GET'], detail=False, url_path='current_currency')
    def get_current_currency(self, request, *args, **kwargs):
        nbrb_response = requests.get(
            url=NBRB_RATES_API_URL.format(request.query_params.get('currency_code', '')),
            params={
                "parammode": 2,
                "ondate": request.query_params.get('date', ''),
            },
        )

        if response := self.__check_api_request(nbrb_response):
            return response

        serializer = self.get_serializer(data=self.__normalize_data(nbrb_response.json()))
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
