from rireki.stores.aws import AmazonWebServices


class DigitalOcean(AmazonWebServices):
    NAME = 'digital-ocean'

    def _get_service_name(self):
        return 'Digital Ocean'

    def _get_endpoint_url(self):
        return 'https://%s.digitaloceanspaces.com' % self.region
