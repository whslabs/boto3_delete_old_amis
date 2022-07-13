import boto3

from datetime import datetime
from datetime import timezone
from dateutil import parser

ec2 = boto3.resource("ec2")


def _filter(name):
    return ec2.images.filter(
        Filters=[{"Name": "name", "Values": [name]}], Owners=["self"]
    )


def _delete(images, dry_run):
    for i in images:
        get_snapshot_id = lambda: [
            d["Ebs"]["SnapshotId"] for d in i.block_device_mappings if "Ebs" in d
        ][0]

        name = i.name
        snapshot_id = get_snapshot_id()

        print(name + " deregistering")

        if not dry_run:
            i.deregister()
            print(name + " deregistered")

        print(snapshot_id + " deleting")

        if not dry_run:
            ec2.Snapshot(snapshot_id).delete()
            print(snapshot_id + " deleted")


def delete_tail(name, dry_run):
    images = _filter(name)

    _, *tail = sorted(images, key=lambda i: i.creation_date, reverse=True)

    _delete(tail, dry_run)


def delete_days(name, days, dry_run):
    images = _filter(name)

    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    test = lambda i: (today - parser.isoparse(i.creation_date)).days >= days

    _delete([i for i in images if test(i)], dry_run)
