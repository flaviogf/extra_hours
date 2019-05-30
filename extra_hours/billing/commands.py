from collections import namedtuple

CreateBillingCommand = namedtuple('CreateBillingCommand', ['user_id',
                                                           'title',
                                                           'description',
                                                           'value',
                                                           'work_date'])

ConfirmReceiveBillingCommand = namedtuple('ConfirmReceiveBillingCommand', ['user_id', 'billing_id'])

CancelReceiveBillingCommand = namedtuple('CancelReceiveBillingCommand', ['user_id', 'billing_id'])

UpdateBillingCommand = namedtuple('UpdateBillingCommand', ['user_id',
                                                           'billing_id',
                                                           'title',
                                                           'description',
                                                           'value',
                                                           'work_date'])
