from rireki.stores.aws import AmazonWebServices
from rireki.stores.digital_ocean import DigitalOcean
from rireki.stores.local import Local


stores = {
    AmazonWebServices.NAME: AmazonWebServices,
    DigitalOcean.NAME: DigitalOcean,
    Local.NAME: Local,
}
