from api2ch import Api2ch

api = Api2ch()

resp = api.threads('vg')
for t in resp.threads[:3]:
    print(f'— {t.subject}, {t.posts_count} 💬, {t.views} 👁')
