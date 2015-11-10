from django.shortcuts import render
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication,permissions


from .tasks import add_product
from .models import ShopOrders
import logging
import json

class ShoppingCartApi(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        if not request.user.is_authenticated():
            data = request.data.items()
            try:
                parsed_data = json.loads(data[0][0])
                user_name = parsed_data['username']
                password = parsed_data['password']
                site_name = parsed_data['site_name']
                product_id = parsed_data['product_id']
                res = add_product.delay(site_name,user_name,password,product_id)

                ShopOrders.objects.get_or_create(
                    shop_name=site_name,
                    product_id = product_id,
                    password = password,
                    task_status = 'P',
                    user_name=user_name,
                    task_id = res.id
                )
                #TODO: Add status updates for processing tasks

                return Response(data=parsed_data)

            except ValueError:
                logging.error("Cant decode JSON")
        else:
            return HttpResponseForbidden()

