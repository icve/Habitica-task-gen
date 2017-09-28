from requests import post, get

_ADD_TASK = "https://habitica.com/api/v3/tasks/user"
_GET_TAGS = "https://habitica.com/api/v3/tags"


class Habitica:
    def __init__(self, uid, apikey):
        self.uid = uid
        self.auth_head = {"x-api-user": uid,
                          "x-api-key": apikey}

    def add_todo(self, text, tags=[]):
        payload = self._make_task(text, "todo", tags)
        print(payload)
        return post(_ADD_TASK, data=payload, headers=self.auth_head)

    @staticmethod
    def _make_task(text, typ, tags=[]):
        return {"text": text,
                "type": typ,
                "tags": tags
                }

    def _get_tags(self, name=None):
        """ get list of tag_objects(name, id)
            if name is passed in the first tag id associated with the name is returned"""
        tags = get(_GET_TAGS, headers=self.auth_head).json()["data"]
        if not name:
            return tags
        else:
            for tag in tags:
                if tag["name"] == name:
                    return tag["id"]
            raise NameError("tag name not found!")



