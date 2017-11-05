from requests import post, get, request

_ADD_TASK = "https://habitica.com/api/v3/tasks/user"
_GET_TAGS = "https://habitica.com/api/v3/tags"
_GET_TASK = "https://habitica.com/api/v3/tasks/{taskId}"
_DELETE_TASK_BY_ID = "https://habitica.com/api/v3/tasks/{taskId}"


class Habitica:
    def __init__(self, uid, apikey):
        self.uid = uid
        self.auth_head = {"x-api-user": uid,
                          "x-api-key": apikey}

    def add_todo(self, text, tags=[]):
        payload = self._make_task(text, "todo", tags)
        return post(_ADD_TASK, data=payload, headers=self.auth_head).json()

    def get_task(self, tid):
        return get(_GET_TASK.format(taskId=tid), headers=self.auth_head).json()

    def delete_task(self, tid):
        return request("DELETE",
                       _DELETE_TASK_BY_ID.format(taskId=tid),
                       headers=self.auth_head).json()

    @staticmethod
    def _make_task(text, typ, tags=[]):
        return {"text": text,
                "type": typ,
                "tags": tags
                }

    def _get_tags(self, name=None):
        """ get list of tag_objects(name, id)
            if name is given the first tag id of the name is returned"""
        tags = get(_GET_TAGS, headers=self.auth_head).json()["data"]
        if not name:
            return tags
        else:
            for tag in tags:
                if tag["name"] == name:
                    return tag["id"]
            raise NameError("tag name not found!")
