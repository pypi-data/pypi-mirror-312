import base64
import json
import os

import requests

AUTH = os.getenv("DAKIYA_AUTH", "local_dev_key")
APP_NAME = os.getenv("DAKIYA_APPNAME", "GLOBAL")

HOST = "https://dakiya.nitrocommerce.ai"
if os.getenv("MODE", "") == "DEVELOPMENT":
    HOST = os.getenv("DAKIYA_HOST", "http://localhost:10400")


def _json_handler(obj):
    print(obj.__class__)
    if obj.__class__.__name__ in [
        "SourceFileLoader",
        "module",
        "function",
        "type",
        "Transmitter",
    ]:
        return str(obj)
    return json.JSONEncoder.default(json.JSONEncoder, obj)


class TransmitterException(Exception):
    pass


class Transmitter:
    def send_x(self, what, template, *k, **kw):
        assert what in ["email", "sms", "whatsapp", "telegram"]
        assert template.endswith(".html")

        encoded_attachements = []
        if "attachments" in kw:
            all_attachments = kw["attachments"]
            if not isinstance(all_attachments, list):
                all_attachments = [all_attachments]

            for attachment in all_attachments:
                size = os.fstat(attachment.fileno()).st_size
                name = os.path.basename(attachment.name)

                if size > 25 * 1024 * 1024:
                    raise TransmitterException(
                        2, "Cannot size file of size more than 25MB"
                    )

                fcontents = None
                try:
                    fcontents = attachment.read()
                except:
                    pass
                if not fcontents:
                    raise TransmitterException(
                        3,
                        "Cannot read attachment, make sure you open file in rb+ mode.",
                    )

                encoded = base64.encodebytes(fcontents)
                encoded_attachements.append(
                    [
                        {
                            "filename": name,
                            "size": size,
                            "base64_encoded_data": encoded.decode(),
                        }
                    ]
                )

            kw["attachments"] = encoded_attachements

        res = None

        payload = json.dumps(kw, default=lambda o: o.__dict__)
        try:
            res = requests.post(
                f"{HOST}/relay/{what}/{template}",
                json=kw,
                headers={
                    "Authorization": f"S2S {AUTH}",
                    "X-App": APP_NAME,
                    "Content-Type": "application/json",
                },
            )
        except requests.exceptions.ConnectionError:
            import traceback

            traceback.print_exc()

        if res is None:
            raise TransmitterException(0, "Connection Error")

        if res.ok:
            res = res.json()
            return res

        try:
            res = res.json()
        except Exception as e:
            print("Exception in JSON.load", e)
            pass

        if res is not None:
            raise TransmitterException(res["code"], res["message"])

        raise TransmitterException(0, "JSON Decode Error from Downstream")

    def __getattr__(self, name):
        name = name.split("_")[1]

        def fn(template, *k, **kw):
            return self.send_x(name, template, *k, **kw)

        return fn


transmitter = Transmitter()


if __name__ == "__main__":
    var = {
        "who": "Shamail",
        "time": "1:10",
    }
    result = transmitter.send_email(
        "nitrox/welcome.html",
        to="tayyab.shamail@gmail.com",
        subject="Hello World!",
        **var,
    )
    print(result)
