import boto3

from datetime import datetime
from datetime import timezone
from dateutil import parser

ec2 = boto3.resource("ec2")


def _filter(name):
    return ec2.images.filter(
        Filters=[{"Name": "name", "Values": [name]}], Owners=["self"]
    )


def _sorted(name):
    return sorted(_filter(name), key=lambda i: i.creation_date, reverse=True)


def _delete(images, dry_run):
    for c, i in enumerate(images, start=1):
        get_snapshot_id = lambda: [
            d["Ebs"]["SnapshotId"] for d in i.block_device_mappings if "Ebs" in d
        ][0]

        name = i.name
        snapshot_id = get_snapshot_id()

        print("Deleting %d/%d" % (c, len(images)))

        print("%s deregistering" % name)

        if not dry_run:
            i.deregister()
            print("%s deregistered" % name)

        print("%s deleting" % snapshot_id)

        if not dry_run:
            ec2.Snapshot(snapshot_id).delete()
            print("%s deleted" % snapshot_id)


def _list(name):
    for c, i in enumerate(images := _sorted(name), start=1):
        print("Remaining %d/%d" % (c, len(images)))

        print(i.name)


def delete_tail(name, dry_run):
    _, *tail = _sorted(name)

    _delete(tail, dry_run)

    _list(name)


def delete_days(name, days, dry_run):
    b, *images = _filter(name)

    def s(i):
        nonlocal b
        j, b = b, i
        return j

    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    dt = lambda i: parser.isoparse(i.creation_date)
    test = lambda i: (today - dt(i)).days >= days

    f = lambda i: s(i) if dt(i) > dt(b) else i  # if i is larger swap with bucket (b)

    _delete([j for i in images if test(j := f(i))], dry_run)

    _list(name)
