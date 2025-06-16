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
        pass
