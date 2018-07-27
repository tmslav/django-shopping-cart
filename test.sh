#!/bin/bash
for i in {1..10}
  do
    curl --data '{"username":"tmslav@gmail.com","password":"","site_name":"ah.nl","product_id":"wi737"}' localhost:8000/shop-api/
    printf "\n"
done
