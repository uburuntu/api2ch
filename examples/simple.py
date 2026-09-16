from api2ch import Api2ch

with Api2ch() as api:
    for thread in api.threads("pr").sorted_by_views()[:3]:
        print(thread.num, thread.header, thread.views)
