from common import convert
from common import validate


def add_act_value_to_validate_dict():
    validator = {
        "dailyRecRate": {
            "firstInstall": {"actual": "", "compare": "num_equals", "expect": "1"},
            "free": {"actual": "","compare": "num_equals","expect": "0"},
            "free_paid": {"actual": "","compare": "num_equals","expect": "0"},
            "old": {"actual": "","compare": "num_equals","expect": "0"},
        },

        "promotionItems": [
            {
                "id": {"actual": "","compare": "num_equals","expect": "2"},
                "name": {"actual": "","compare": "equals","expect": "charge_present"}
            }
            ]
        }

    response = {
        "dailyRecRate": {
            "old": 0,
            "free_paid": 0,
            "free": 0,
            "firstInstall": 1
        },
        "promotionItems": [
            {
              "name": "charge_present",
              "id": 2,
            }
        ]
    }

    validate.run_validator(validator, response)


if __name__ == '__main__':
    from common import logger
    logger.Logging()
    add_act_value_to_validate_dict()