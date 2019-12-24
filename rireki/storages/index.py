from rireki.storages.aws import AmazonWebServices
from rireki.storages.digital_ocean import DigitalOcean
from rireki.storages.local import Local


storages = {
    AmazonWebServices.NAME: AmazonWebServices,
    DigitalOcean.NAME: DigitalOcean,
    Local.NAME: Local,
}
