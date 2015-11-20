from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication,permissions


from .tasks import add_product,check_results
from .models import ShopOrders
import logging
import json

class ShoppingCartApi(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    permissions_classes = (permissions.IsAuthenticated,)
    def submit_product(self,site_name,user_name,password,product_id,quantity):
         res = ShopOrders.objects.create(
            shop_name=site_name,
            product_id=product_id,
            password=password,
            task_status='P',
            user_name=user_name,
            quantity=quantity)

         add_product.apply_async((site_name,user_name,password,product_id,quantity),link=check_results.s(res.task_id))

    def get(self,request):
        pending = ShopOrders.objects.filter(task_status='P').count()
        done = ShopOrders.objects.filter(task_status='D').count()
        failed = ShopOrders.objects.filter(task_status='F').count()
        return JsonResponse({'pending':pending,'done':done,'failed':failed})

    def post(self,request):
        if not request.user.is_authenticated():
            data = request.data.items()
            try:
                parsed_data = json.loads(data[0][0])
                user_name = parsed_data['username']
                password = parsed_data['password']
                site_name = parsed_data['site_name']
                product_id = parsed_data['product_id']
                if isinstance(product_id,list):
                    for product in product_id:
                        self.submit_product(site_name,user_name,password,product['id'],product['quantity'])
                else:
                    quantity = parsed_data['quantity']
                    self.submit_product(site_name,user_name,password,product_id,quantity)
                return Response(data=parsed_data)

            except:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()

