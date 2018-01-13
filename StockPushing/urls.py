#-*- coding: UTF-8 -*-
from . import StockPushingController
from . import AnalyzeStockPushing
from . import ManageStockPushingController
from . import StockPushing_Mongo_Controller
"""
StockPushing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getStockList', StockPushingController.getStockList),
    url(r'^showTest/$', StockPushingController.showTest),
    url(r'^ApiP_Proc/GetStockPushingList/$', StockPushingController.getStockPushing),
    url(r'^ApiP_Proc/GetStockPushingListWithAllData/$', StockPushingController.getStockPushingWithAllData),
    url(r'^ApiP_Proc/Get5DaysMinPicUrl/$', StockPushingController.Get5DaysMinPicUrl),
    url(r'^ApiP_Proc/GetMinTradForDate/$', StockPushingController.GetMinTradForDate),
    url(r'^ApiP_Proc/getMinPriceForStockOnDate/$', StockPushingController.getMinPriceForStockOnDate),
    url(r'^ApiP_Proc/getMinPriceForForFullSetDate/$', StockPushingController.getMinPriceForForFullSetDate),
    url(r'^ApiP_Proc/getMinPriceForForFullSetDateThruName/$', StockPushingController.getMinPriceForForFullSetDateThruName),
    url(r'^ApiP_Proc/AddStockPushing/$', StockPushingController.AddStockPushing),
    url(r'^ApiP_Proc/testCurlSuccess', StockPushingController.testCurlSuccess),
    url(r'^ApiP_Proc/testCurlFailed', StockPushingController.testCurlFailed),
    url(r'^getTodayMinPriceForForFullSetDate', StockPushingController.getTodayMinPriceForForFullSetDate),
    url(r'^GetStockCodeListForPushingDate', AnalyzeStockPushing.GetStockCodeListForPushingDate),
    url(r'^GetStockForAnalyzeInPeriod', AnalyzeStockPushing.getStockForAnalyzeInPeriod),

    url(r'^GetTheDateMinPriceForForFullSetDate/$', StockPushingController.getTheDateMinPriceForForFullSetDate),
    url(r'^GetMinPriceForFullSetDateForPushingDate/$', StockPushingController.getMinPriceForFullSetDateForPushingDate),
    url(r'^getMinPriceForStockOnDate/$', ManageStockPushingController.getMinPriceForStockOnDate),

    url(r'^Collect_stock_pushing_in_period', AnalyzeStockPushing.collect_stock_pushing_in_period),
    #用mongoDB后的api
    url(r'^MongoTestSave', StockPushing_Mongo_Controller.TestSave),
    url(r'^SaveRanking/$', StockPushing_Mongo_Controller.SaveRanking),
]
