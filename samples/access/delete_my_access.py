"""Remove as id's access to a resource."""

import json

from pyracf.access.access_admin import AccessAdmin


def main():
    """Entrypoint."""
    access_admin = AccessAdmin()

    traits = {
        "resourcename": "ESWIFT.TESTING.PROFILE",
        "classname": "ELIJTEST",
        "id": "ESWIFT"
    }

    result = access_admin.delete(traits)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
