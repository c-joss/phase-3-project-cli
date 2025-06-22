class Rate:
    def __init__(
        self,
        load_port,
        destination_port,
        container_type,
        freight_usd,
        othc_aud,
        doc_aud,
        cmr_aud,
        ams_usd,
        lss_usd,
        dthc,
        free_time,
    ):
        self.load_port = load_port
        self.destination_port = destination_port
        self.container_type = container_type
        self.freight_usd = freight_usd
        self.othc_aud = othc_aud
        self.doc_aud = doc_aud
        self.cmr_aud = cmr_aud
        self.ams_usd = ams_usd
        self.lss_usd = lss_usd
        self.dthc = dthc
        self.free_time = free_time

    def to_dict(self):
        return {
            "load_port": self.load_port,
            "destination_port": self.destination_port,
            "container_type": self.container_type,
            "freight_usd": self.freight_usd,
            "othc_aud": self.othc_aud,
            "doc_aud": self.doc_aud,
            "cmr_aud": self.cmr_aud,
            "ams_usd": self.ams_usd,
            "lss_usd": self.lss_usd,
            "dthc": self.dthc,
            "free_time": self.free_time,
        }

    def __str__(self):
        return (
            f"{self.load_port} {self.destination_port} | "
            f"FREIGHT: {self.freight_usd} USD | OTHC: {self.othc_aud} AUD | "
            f"DOC: {self.doc_aud} AUD | CMR: {self.cmr_aud} AUD | AMS: {self.ams_usd} USD | "
            f"LSS: {self.lss_usd} USD | DTHC: {self.dthc} | Free Time: {self.free_time}"
        )


class Customer:
    def __init__(self, name):
        self.name = name
        self.rates = []

    def add_rate(self, rate):
        self.rates.append(rate)

    def to_dict(self):
        return {"name": self.name, "rates": [rate.to_dict() for rate in self.rates]}

    def __str__(self):
        return f"Customer: {self.name} | {len(self.rates)} rates"


class TariffRate(Rate):
    def __init__(self, load_port, destination_port, container_type, tariff_values):
        super().__init__(
            load_port,
            destination_port,
            container_type,
            tariff_values["freight_usd"],
            tariff_values["othc_aud"],
            tariff_values["doc_aud"],
            tariff_values["cmr_aud"],
            tariff_values["ams_usd"],
            tariff_values["lss_usd"],
            tariff_values["dthc"],
            tariff_values["free_time"],
        )
