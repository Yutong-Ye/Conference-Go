from json import JSONEncoder

class ModelEncoder(JSONEncoder):
    encoders = {}

    def default(self, o):
        if isinstance(o, self.model):
            d = {}
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]()
                    value = encoder.default(value)
                d[property] = value
            d.update(self.get_extra_data(o))
            return d
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}