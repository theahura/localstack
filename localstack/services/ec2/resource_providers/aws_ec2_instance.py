# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)
from localstack.utils.strings import to_str


class EC2InstanceProperties(TypedDict):
    AdditionalInfo: Optional[str]
    Affinity: Optional[str]
    AvailabilityZone: Optional[str]
    BlockDeviceMappings: Optional[list[BlockDeviceMapping]]
    CpuOptions: Optional[CpuOptions]
    CreditSpecification: Optional[CreditSpecification]
    DisableApiTermination: Optional[bool]
    EbsOptimized: Optional[bool]
    ElasticGpuSpecifications: Optional[list[ElasticGpuSpecification]]
    ElasticInferenceAccelerators: Optional[list[ElasticInferenceAccelerator]]
    EnclaveOptions: Optional[EnclaveOptions]
    HibernationOptions: Optional[HibernationOptions]
    HostId: Optional[str]
    HostResourceGroupArn: Optional[str]
    IamInstanceProfile: Optional[str]
    Id: Optional[str]
    ImageId: Optional[str]
    InstanceInitiatedShutdownBehavior: Optional[str]
    InstanceType: Optional[str]
    Ipv6AddressCount: Optional[int]
    Ipv6Addresses: Optional[list[InstanceIpv6Address]]
    KernelId: Optional[str]
    KeyName: Optional[str]
    LaunchTemplate: Optional[LaunchTemplateSpecification]
    LicenseSpecifications: Optional[list[LicenseSpecification]]
    Monitoring: Optional[bool]
    NetworkInterfaces: Optional[list[NetworkInterface]]
    PlacementGroupName: Optional[str]
    PrivateDnsName: Optional[str]
    PrivateDnsNameOptions: Optional[PrivateDnsNameOptions]
    PrivateIp: Optional[str]
    PrivateIpAddress: Optional[str]
    PropagateTagsToVolumeOnCreation: Optional[bool]
    PublicDnsName: Optional[str]
    PublicIp: Optional[str]
    RamdiskId: Optional[str]
    SecurityGroupIds: Optional[list[str]]
    SecurityGroups: Optional[list[str]]
    SourceDestCheck: Optional[bool]
    SsmAssociations: Optional[list[SsmAssociation]]
    SubnetId: Optional[str]
    Tags: Optional[list[Tag]]
    Tenancy: Optional[str]
    UserData: Optional[str]
    Volumes: Optional[list[Volume]]


class Ebs(TypedDict):
    DeleteOnTermination: Optional[bool]
    Encrypted: Optional[bool]
    Iops: Optional[int]
    KmsKeyId: Optional[str]
    SnapshotId: Optional[str]
    VolumeSize: Optional[int]
    VolumeType: Optional[str]


class BlockDeviceMapping(TypedDict):
    DeviceName: Optional[str]
    Ebs: Optional[Ebs]
    NoDevice: Optional[dict]
    VirtualName: Optional[str]


class InstanceIpv6Address(TypedDict):
    Ipv6Address: Optional[str]


class ElasticGpuSpecification(TypedDict):
    Type: Optional[str]


class ElasticInferenceAccelerator(TypedDict):
    Type: Optional[str]
    Count: Optional[int]


class Volume(TypedDict):
    Device: Optional[str]
    VolumeId: Optional[str]


class LaunchTemplateSpecification(TypedDict):
    Version: Optional[str]
    LaunchTemplateId: Optional[str]
    LaunchTemplateName: Optional[str]


class EnclaveOptions(TypedDict):
    Enabled: Optional[bool]


class PrivateIpAddressSpecification(TypedDict):
    Primary: Optional[bool]
    PrivateIpAddress: Optional[str]


class NetworkInterface(TypedDict):
    DeviceIndex: Optional[str]
    AssociateCarrierIpAddress: Optional[bool]
    AssociatePublicIpAddress: Optional[bool]
    DeleteOnTermination: Optional[bool]
    Description: Optional[str]
    GroupSet: Optional[list[str]]
    Ipv6AddressCount: Optional[int]
    Ipv6Addresses: Optional[list[InstanceIpv6Address]]
    NetworkInterfaceId: Optional[str]
    PrivateIpAddress: Optional[str]
    PrivateIpAddresses: Optional[list[PrivateIpAddressSpecification]]
    SecondaryPrivateIpAddressCount: Optional[int]
    SubnetId: Optional[str]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


class HibernationOptions(TypedDict):
    Configured: Optional[bool]


class LicenseSpecification(TypedDict):
    LicenseConfigurationArn: Optional[str]


class CpuOptions(TypedDict):
    CoreCount: Optional[int]
    ThreadsPerCore: Optional[int]


class PrivateDnsNameOptions(TypedDict):
    EnableResourceNameDnsAAAARecord: Optional[bool]
    EnableResourceNameDnsARecord: Optional[bool]
    HostnameType: Optional[str]


class AssociationParameter(TypedDict):
    Key: Optional[str]
    Value: Optional[list[str]]


class SsmAssociation(TypedDict):
    DocumentName: Optional[str]
    AssociationParameters: Optional[list[AssociationParameter]]


class CreditSpecification(TypedDict):
    CPUCredits: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2InstanceProvider(ResourceProvider[EC2InstanceProperties]):
    TYPE = "AWS::EC2::Instance"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2InstanceProperties],
    ) -> ProgressEvent[EC2InstanceProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id



        Create-only properties:
          - /properties/ElasticGpuSpecifications
          - /properties/Ipv6Addresses
          - /properties/PlacementGroupName
          - /properties/HostResourceGroupArn
          - /properties/ImageId
          - /properties/CpuOptions
          - /properties/PrivateIpAddress
          - /properties/ElasticInferenceAccelerators
          - /properties/EnclaveOptions
          - /properties/HibernationOptions
          - /properties/KeyName
          - /properties/LicenseSpecifications
          - /properties/NetworkInterfaces
          - /properties/AvailabilityZone
          - /properties/SubnetId
          - /properties/LaunchTemplate
          - /properties/SecurityGroups
          - /properties/Ipv6AddressCount

        Read-only properties:
          - /properties/PublicIp
          - /properties/Id
          - /properties/PublicDnsName
          - /properties/PrivateDnsName
          - /properties/PrivateIp



        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        # TODO: validations

        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked
            # TODO: defaults
            # TODO: idempotency
            params = util.select_attributes(
                model,
                ["InstanceType", "SecurityGroups", "KeyName", "ImageId", "MaxCount", "MinCount"],
            )

            if model.get("UserData"):
                model["UserData"] = to_str(base64.b64decode(model["UserData"]))

            response = ec2.run_instances(**params)
            model["Id"] = response["Instances"][0]["InstanceId"]
            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        response = ec2.describe_instances(InstanceIds=[model["Id"]])
        instance = response["Reservations"][0]["Instances"][0]
        if instance["State"]["Name"] != "running":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        model["PublicIp"] = instance["PublicIpAddress"]
        model["PublicDnsName"] = instance["PublicDnsName"]
        model["PrivateIp"] = instance["PrivateIpAddress"]
        model["PrivateDnsName"] = instance["PrivateDnsName"]
        model["AvailabilityZone"] = instance["Placement"]["AvailabilityZone"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2InstanceProperties],
    ) -> ProgressEvent[EC2InstanceProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2InstanceProperties],
    ) -> ProgressEvent[EC2InstanceProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2
        ec2.terminate_instances(InstanceIds=[model["Id"]])
        # TODO add checking of ec2 instance state
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EC2InstanceProperties],
    ) -> ProgressEvent[EC2InstanceProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
