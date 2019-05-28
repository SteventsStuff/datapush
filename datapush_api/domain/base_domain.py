class BaseDomain:

    def __init__(self, url):
        self.url = url

    async def get_instances(self):
        pass

    async def get_instance_by_key(self):
        pass
