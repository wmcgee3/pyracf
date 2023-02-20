import json

from pyracf.genprof.ResourceAdmin import ResourceAdmin


def main():
    profile_admin = ResourceAdmin()

    resourcename = "BIKINI.BOTTOM.KRUSKRAB"
    classname = "FACILITY"

    result = profile_admin.delete(resourcename, classname)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
