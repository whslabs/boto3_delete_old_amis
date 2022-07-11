import boto3

ec2 = boto3.resource("ec2")


def delete_tail(name):
    _, *tail = ec2.images.filter(
        Filters=[{"Name": "name", "Values": [name]}], Owners=["self"]
    )

    for image in tail:
        get_snapshot_id = lambda: [
            d["Ebs"]["SnapshotId"] for d in image.block_device_mappings if "Ebs" in d
        ][0]

        image_name = image.name
        snapshot_id = get_snapshot_id()

        image.deregister()
        print(image_name + " deregistered")

        ec2.Snapshot(snapshot_id).delete()
        print(snapshot_id + " deleted")
