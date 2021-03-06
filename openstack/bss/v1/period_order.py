# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

from openstack.bss import bss_service
from openstack import resource2

try:
    # Python3
    from urllib.parse import urlencode
except ImportError:
    # Python2
    from urllib import urlencode


# 支付包周期产品订单
class PayPeriodOrder(resource2.Resource):
    base_path = "%(domain_id)s/customer/order-mgr/order/pay"
    service = bss_service.BssService()
    allow_create = True

    # User domain ID
    domain_id = resource2.URI('domain_id')

    # request
    # Order ID.
    orderId = resource2.Body('orderId')
    # Payment account type.
    payAccountType = resource2.Body('payAccountType', type=int)
    # partner account ID
    bpId = resource2.Body('bpId')
    # This parameter is reserved.
    couponIds = resource2.Body('couponIds', type=list)

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # Payment sequence number corresponding to the order.
    tradeNo = resource2.Body('tradeNo')
    # Information about the resources whose quota or capacity is insufficient.
    quotaInfos = resource2.Body('quotaInfos', type=list)
    # Information about the enterprise project whose fund is insufficient.
    enterpriseProjectAuthResult = resource2.Body('enterpriseProjectAuthResult', type=list)


class UnsubscribePeriodOrder(resource2.Resource):
    base_path = "%(domain_id)s/customer/order-mgr/orders/%(order_id)s"
    service = bss_service.BssService()

    allow_delete = True

    # User domain ID
    domain_id = resource2.URI('domain_id')
    order_id = resource2.URI('order_id')

    # request
    unsub_type = resource2.Body('unsub_type')
    unsubscribe_reason_type = resource2.Body('unsubscribe_reason_type')
    unsubscribe_reason = resource2.Body('unsubscribe_reason')

    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # New order ID generated for the unsubscription.
    unsub_order_ids = resource2.Body('unsub_order_ids')

    def delete(self, session, params=None, has_body=True):
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        request = self._prepare_request(requires_id=False,
                                        prepend_key=True)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'unsub_type': self.unsub_type, 'unsubscribe_reason_type': xstr(self.unsubscribe_reason_type),
                      "unsubscribe_reason": xstr(self.unsubscribe_reason)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + '?' + query_str
        response = session.delete(url, endpoint_filter=self.service,
                                  microversion=service.microversion,
                                  endpoint_override=endpoint_override,
                                  headers=request.headers,
                                  params=params)
        self._translate_response(response)
        return self


class CancelOrder(resource2.Resource):
    base_path = "%(domain_id)s/customer/order-mgr/orders/actions?action_id=%(action_id)s"
    service = bss_service.BssService()
    allow_create = True
    put_create = True

    # User domain ID
    domain_id = resource2.URI('domain_id')
    action_id = resource2.URI('action_id')

    # request
    # Order ID.
    orderId = resource2.Body('orderId')
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')

    def create(self, session, prepend_key=True):
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        request = self._prepare_request(requires_id=False,
                                        prepend_key=prepend_key)
        response = session.put(request.uri, endpoint_filter=self.service,
                               endpoint_override=endpoint_override,
                               json=request.body, headers=request.headers,
                               microversion=service.microversion)
        self._translate_response(response)
        return self


class QueryOrderDetail(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/orders/%(order_id)s"
    service = bss_service.BssService()
    allow_get = True

    # request
    # User domain ID
    domain_id = resource2.URI('domain_id')
    order_id = resource2.URI('order_id')
    offset = resource2.Body('offset')
    limit = resource2.Body('limit')

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # Total number of records.
    count = resource2.Body('count')
    # Order details.
    orderInfo = resource2.Body('orderInfo')
    # ID of the primary order item mapping the order item.
    orderlineItems = resource2.Body('orderlineItems')

    def get(self, session, requires_id=False):
        request = self._prepare_request(requires_id=False)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'offset': xstr(self.offset), 'limit': xstr(self.limit)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + "?" + query_str
        response = session.get(url, endpoint_filter=self.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self


class QueryOrderList(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/orders/detail"
    service = bss_service.BssService()
    allow_get = True

    # request
    # User domain ID
    domain_id = resource2.URI('domain_id')
    order_id = resource2.Body('order_id')
    customer_id = resource2.Body('customer_id')
    create_time_begin = resource2.Body('create_time_begin')
    create_time_end = resource2.Body('create_time_end')
    service_type = resource2.Body('service_type')
    #  0: The account name, mobile number, or email address does not exist.
    #  1: The account name, mobile number, or email address already exists.
    status = resource2.Body('status')
    order_type = resource2.Body('order_type')
    page_size = resource2.Body('page_size')
    page_index = resource2.Body('page_index')
    sort = resource2.Body('sort')
    payment_time_begin = resource2.Body('payment_time_begin')
    payment_time_end = resource2.Body('payment_time_end')

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    data = resource2.Body('data')

    def get(self, session, requires_id=False):
        request = self._prepare_request(requires_id=False)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'order_id': xstr(self.order_id), 'customer_id': xstr(self.customer_id),
                      'create_time_begin': xstr(self.create_time_begin), 'create_time_end': xstr(self.create_time_end),
                      'status': xstr(self.status), 'order_type': xstr(self.order_type),
                      'service_type': xstr(self.service_type), 'page_size': xstr(self.page_size),
                      'page_index': xstr(self.page_index), 'sort': xstr(self.sort),
                      'payment_time_begin': xstr(self.payment_time_begin),
                      'payment_time_end': xstr(self.payment_time_end)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + "?" + query_str
        response = session.get(url, endpoint_filter=self.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self


class QueryRefundOrder(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/orders/refund-order"
    service = bss_service.BssService()
    allow_get = True

    # request
    # User domain ID
    domain_id = resource2.URI('domain_id')
    order_id = resource2.Body('order_id')

    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    resource_info_list = resource2.Body('resource_info_list', type=list)
    total_count = resource2.Body('total_count', type=int)

    def get(self, session, requires_id=False):
        request = self._prepare_request(requires_id=False)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'order_id': xstr(self.order_id)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + "?" + query_str
        response = session.get(url, endpoint_filter=self.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self


class QueryOrderResource(resource2.Resource):
    base_path = "%(domain_id)s/common/order-mgr/orders-resource/%(order_id)s"
    service = bss_service.BssService()
    allow_get = True

    # request
    # User domain ID
    domain_id = resource2.URI('domain_id')
    order_id = resource2.URI('order_id')
    offset = resource2.Body('offset')
    limit = resource2.Body('limit')

    # response
    #  Status code.
    error_code = resource2.Body('error_code')
    # Error description.
    error_msg = resource2.Body('error_msg')
    # Number of records that match the query conditions.
    totalSize = resource2.Body('totalSize')
    resources = resource2.Body('resources')

    def get(self, session, requires_id=False):
        request = self._prepare_request(requires_id=False)
        endpoint_override = self.service.get_endpoint_override()
        service = self.get_service_filter(self, session)
        xstr = lambda s: '' if s is None else str(s)
        query_dict = {'offset': xstr(self.offset), 'limit': xstr(self.limit)}
        query_str = urlencode(query_dict, doseq=True)
        url = request.uri + "?" + query_str
        response = session.get(url, endpoint_filter=self.service,
                               microversion=service.microversion,
                               endpoint_override=endpoint_override)
        self._translate_response(response)
        return self
