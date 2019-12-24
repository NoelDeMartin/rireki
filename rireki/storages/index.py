from rireki.storages.digital_ocean import DigitalOcean
from rireki.storages.local import Local


storages = {
    DigitalOcean.NAME: DigitalOcean,
    Local.NAME: Local,
}
