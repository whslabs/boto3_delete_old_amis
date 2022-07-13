import boto3

from datetime import datetime
from datetime import timezone
from dateutil import parser

ec2 = boto3.resource("ec2")


def _filter(name):
    return ec2.images.filter(
        Filters=[{"Name": "name", "Values": [name]}], Owners=["self"]
    )


def _delete(images):
    for i in images:
        get_snapshot_id = lambda: [
            d["Ebs"]["SnapshotId"] for d in i.block_device_mappings if "Ebs" in d
        ][0]

        name = i.name
        snapshot_id = get_snapshot_id()

        i.deregister()
        print(name + " deregistered")

        ec2.Snapshot(snapshot_id).delete()
        print(snapshot_id + " deleted")


def delete_tail(name):
    images = _filter(name)

    _, *tail = sorted(images, key=lambda i: i.creation_date, reverse=True)

    _delete(tail)


def delete_days(name, days):
    images = _filter(name)

    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    test = lambda i: (today - parser.isoparse(i.creation_date)).days >= days

    _delete([i for i in images if test(i)])
