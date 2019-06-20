from collections import namedtuple

BillingListQueryResult = namedtuple('BillingListQueryResult', ['uid',
                                                               'title',
                                                               'description',
                                                               'value',
                                                               'work_date',
                                                               'received_date',
                                                               'user_uid'])
