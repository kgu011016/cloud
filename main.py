# sudo yum install python3
# pip install boto3
# https://github.com/kgu011016/cloud.git

import boto3

ec2 = None

def init():
    global ec2
    try:
        session = boto3.Session(profile_name='rootkim')
        ec2 = session.client('ec2', region_name='us-east-2')
    except Exception as e:
        raise Exception(f"Error initializing AWS client: {e}")

def list_instances():
    print("Listing instances....")
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print(
                    f"[id] {instance['InstanceId']}, "
                    f"[AMI] {instance['ImageId']}, "
                    f"[type] {instance['InstanceType']}, "
                    f"[state] {instance['State']['Name']}, "
                    f"[monitoring state] {instance['Monitoring']['State']}"
                )
        print()
    except Exception as e:
        print(f"Error listing instances: {e}")

def available_zones():
    print("Available zones....")
    try:
        response = ec2.describe_availability_zones()
        for zone in response['AvailabilityZones']:
            print(f"[id] {zone['ZoneId']}, [region] {zone['RegionName']}, [zone] {zone['ZoneName']}")
        print(f"You have access to {len(response['AvailabilityZones'])} Availability Zones.")
    except Exception as e:
        print(f"Error getting available zones: {e}")

def start_instance(instance_id):
    try:
        print(f"Starting .... {instance_id}")
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Successfully started instance {instance_id}")
    except Exception as e:
        print(f"Error starting instance: {e}")

def available_regions():
    print("Available regions ....")
    try:
        regions_response = ec2.describe_regions()
        for region in regions_response['Regions']:
            print(
                f"[region] {region['RegionName']}, "
                f"[endpoint] {region['Endpoint']}"
            )
    except Exception as e:
        print(f"Error getting available regions: {e}")

def stop_instance(instance_id):
    try:
        print(f"Stopping .... {instance_id}")
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Successfully stopped instance {instance_id}")
    except Exception as e:
        print(f"Error stopping instance: {e}")

def create_instance(ami_id):
    try:
        print(f"Creating instance with AMI .... {ami_id}")
        run_request = {
            'ImageId': ami_id,
            'InstanceType': 't2.micro',
            'MinCount': 1,
            'MaxCount': 1
        }
        run_response = ec2.run_instances(**run_request)

        reservation_id = run_response['Instances'][0]['InstanceId']

        print(
            f"Successfully started EC2 instance {reservation_id} based on AMI {ami_id}"
        )
    except Exception as e:
        print(f"Error creating instance: {e}")

def reboot_instance(instance_id):
    try:
        print(f"Rebooting .... {instance_id}")
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Successfully rebooted instance {instance_id}")
    except Exception as e:
        print(f"Error rebooting instance: {e}")

def list_images():
    print("Listing images....")
    try:
        request = {
            'Filters': [
                {'Name': 'name', 'Values': ['htcondor-slave-image']}
            ]
        }
        results = ec2.describe_images(**request)

        for image in results['Images']:
            print(
                f"[ImageID] {image['ImageId']}, "
                f"[Name] {image['Name']}, "
                f"[Owner] {image['OwnerId']}"
            )
    except Exception as e:
        print(f"Error listing images: {e}")

def main():
    init()

    while True:
        print("                                                            ")
        print("                                                            ")
        print("------------------------------------------------------------")
        print("           Amazon AWS Control Panel using SDK               ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("                                 99. quit                   ")
        print("------------------------------------------------------------")

        number = int(input("Enter an integer: "))
        if number == 99:
            print("bye!")
            break

        instance_id = ""

        if number == 1:
            list_instances()
        elif number == 2:
            available_zones()
        elif number == 3:
            instance_id = input("Enter instance id: ")
            if instance_id.strip():
                start_instance(instance_id)
        elif number == 4:
            available_regions()
        elif number == 5:
            instance_id = input("Enter instance id: ")
            if instance_id.strip():
                stop_instance(instance_id)
        elif number == 6:
            ami_id = input("Enter ami id: ")
            if ami_id.strip():
                create_instance(ami_id)
        elif number == 7:
            instance_id = input("Enter instance id: ")
            if instance_id.strip():
                reboot_instance(instance_id)
        elif number == 8:
            list_images()
        else:
            print("Invalid input! Please try again.")

if __name__ == "__main__":
    main()
