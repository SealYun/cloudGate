#!/bin/sh

#networks test set
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworksHandler_POST \
#NetworkTest.test_NetworksHandler_GET \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_PUT \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworkHandler_DELETE \
#NetworkTest.test_NetworkHandler_GET \
#NetworkTest.test_NetworksHandler_GET \

python httptest.py \
LoadBalanceTest.test_LoadbalancersHandler_GET \
LoadBalanceTest.test_LoadbalancersHandler_POST \
LoadBalanceTest.test_LbaasListenersHandler_GET \
LoadBalanceTest.test_LbaasListenersHandler_POST \
LoadBalanceTest.test_LbaasListenerHandler_GET \
LoadBalanceTest.test_LbaasListenerHandler_DELETE \
LoadBalanceTest.test_LbaasListenersHandler_GET \
LoadBalanceTest.test_LoadbalancerHandler_DELETE \
LoadBalanceTest.test_LoadbalancersHandler_GET \









