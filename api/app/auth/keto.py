import requests


class AccessControl:
    def __init__(self, keto_write_url, keto_read_url):
        self.keto_write_url = keto_write_url
        self.keto_read_url = keto_read_url

    def is_allowed(self, namespace, obj, relation, subject_id):
        return self.check_permissions(namespace, obj, relation, subject_id)

    def check_permissions(self, namespace, obj, relation, subject_id) -> bool:
        r = requests.get(
            f"{self.keto_read_url}/relation-tuples/check",
            data={
                "object": obj,
                "relation": relation,
                "subject_id": subject_id,
                "namespace": namespace,
            },
        )
        data = r.json()
        return data.get('allowed')

    def add_permissions(self, namespace, obj, relation, subject_id):
        r = requests.put(
            f"{self.keto_write_url}/relation-tuples",
            data={"object": obj, "relation": relation, "subject_id": subject_id, "namespace": namespace},
        )
        r.json()
