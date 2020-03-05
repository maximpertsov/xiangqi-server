import json
from abc import ABC, abstractmethod

import jsonschema
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

# TODO: test this class!


class PayloadSchemaMixin(ABC):
    @cached_property
    def payload(self):
        try:
            result = json.loads(self.request.body.decode("utf-8"))
            jsonschema.validate(result, self.payload_schema)
            return result
        except json.JSONDecodeError:
            raise ValidationError("Error parsing request")
        except jsonschema.ValidationError as e:
            raise ValidationError(str(e))

    @property
    @abstractmethod
    def payload_schema(self):
        pass
