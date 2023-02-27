from __future__ import annotations


class QSClient:
    base_domain: str
    username: str
    password: str
    token: str

    auth_endpoint: str
    sensor_list_endpoint: str
    sensor_endpoint: str
    fdsn_dataselect_endpoint: str
    fdsn_station_endpoint: str
    data_product_endpoint: str
    measurement_endpoint: str

    def __init__(
        self,
        username: str,
        password: str,
        base_domain: str | None = "network.quakesaver.net",
    ):
        self.username = username
        self.password = password

        self.base_domain = base_domain

        self.auth_endpoint = f"https://api.{base_domain}/api/v1/user/get_token"
        self.sensor_list_endpoint = f"https://api.{base_domain}/api/v1/user/me/sensors"
        self.sensor_endpoint = (
            f"https://api.{base_domain}/api/v1/sensors/{{sensor_uid}}"
        )
        self.data_product_endpoint = (
            f"{self.sensor_endpoint}/data_products/{{data_product_name}}"
        )
        self.measurement_endpoint = f"{self.sensor_endpoint}/measurements"
