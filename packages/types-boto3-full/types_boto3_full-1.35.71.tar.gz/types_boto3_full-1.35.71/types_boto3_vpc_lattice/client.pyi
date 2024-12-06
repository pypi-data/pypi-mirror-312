"""
Type annotations for vpc-lattice service client.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_vpc_lattice.client import VPCLatticeClient

    session = Session()
    client: VPCLatticeClient = session.client("vpc-lattice")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListAccessLogSubscriptionsPaginator,
    ListListenersPaginator,
    ListRulesPaginator,
    ListServiceNetworkServiceAssociationsPaginator,
    ListServiceNetworksPaginator,
    ListServiceNetworkVpcAssociationsPaginator,
    ListServicesPaginator,
    ListTargetGroupsPaginator,
    ListTargetsPaginator,
)
from .type_defs import (
    BatchUpdateRuleRequestRequestTypeDef,
    BatchUpdateRuleResponseTypeDef,
    CreateAccessLogSubscriptionRequestRequestTypeDef,
    CreateAccessLogSubscriptionResponseTypeDef,
    CreateListenerRequestRequestTypeDef,
    CreateListenerResponseTypeDef,
    CreateRuleRequestRequestTypeDef,
    CreateRuleResponseTypeDef,
    CreateServiceNetworkRequestRequestTypeDef,
    CreateServiceNetworkResponseTypeDef,
    CreateServiceNetworkServiceAssociationRequestRequestTypeDef,
    CreateServiceNetworkServiceAssociationResponseTypeDef,
    CreateServiceNetworkVpcAssociationRequestRequestTypeDef,
    CreateServiceNetworkVpcAssociationResponseTypeDef,
    CreateServiceRequestRequestTypeDef,
    CreateServiceResponseTypeDef,
    CreateTargetGroupRequestRequestTypeDef,
    CreateTargetGroupResponseTypeDef,
    DeleteAccessLogSubscriptionRequestRequestTypeDef,
    DeleteAuthPolicyRequestRequestTypeDef,
    DeleteListenerRequestRequestTypeDef,
    DeleteResourcePolicyRequestRequestTypeDef,
    DeleteRuleRequestRequestTypeDef,
    DeleteServiceNetworkRequestRequestTypeDef,
    DeleteServiceNetworkServiceAssociationRequestRequestTypeDef,
    DeleteServiceNetworkServiceAssociationResponseTypeDef,
    DeleteServiceNetworkVpcAssociationRequestRequestTypeDef,
    DeleteServiceNetworkVpcAssociationResponseTypeDef,
    DeleteServiceRequestRequestTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteTargetGroupRequestRequestTypeDef,
    DeleteTargetGroupResponseTypeDef,
    DeregisterTargetsRequestRequestTypeDef,
    DeregisterTargetsResponseTypeDef,
    GetAccessLogSubscriptionRequestRequestTypeDef,
    GetAccessLogSubscriptionResponseTypeDef,
    GetAuthPolicyRequestRequestTypeDef,
    GetAuthPolicyResponseTypeDef,
    GetListenerRequestRequestTypeDef,
    GetListenerResponseTypeDef,
    GetResourcePolicyRequestRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetRuleRequestRequestTypeDef,
    GetRuleResponseTypeDef,
    GetServiceNetworkRequestRequestTypeDef,
    GetServiceNetworkResponseTypeDef,
    GetServiceNetworkServiceAssociationRequestRequestTypeDef,
    GetServiceNetworkServiceAssociationResponseTypeDef,
    GetServiceNetworkVpcAssociationRequestRequestTypeDef,
    GetServiceNetworkVpcAssociationResponseTypeDef,
    GetServiceRequestRequestTypeDef,
    GetServiceResponseTypeDef,
    GetTargetGroupRequestRequestTypeDef,
    GetTargetGroupResponseTypeDef,
    ListAccessLogSubscriptionsRequestRequestTypeDef,
    ListAccessLogSubscriptionsResponseTypeDef,
    ListListenersRequestRequestTypeDef,
    ListListenersResponseTypeDef,
    ListRulesRequestRequestTypeDef,
    ListRulesResponseTypeDef,
    ListServiceNetworkServiceAssociationsRequestRequestTypeDef,
    ListServiceNetworkServiceAssociationsResponseTypeDef,
    ListServiceNetworksRequestRequestTypeDef,
    ListServiceNetworksResponseTypeDef,
    ListServiceNetworkVpcAssociationsRequestRequestTypeDef,
    ListServiceNetworkVpcAssociationsResponseTypeDef,
    ListServicesRequestRequestTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetGroupsRequestRequestTypeDef,
    ListTargetGroupsResponseTypeDef,
    ListTargetsRequestRequestTypeDef,
    ListTargetsResponseTypeDef,
    PutAuthPolicyRequestRequestTypeDef,
    PutAuthPolicyResponseTypeDef,
    PutResourcePolicyRequestRequestTypeDef,
    RegisterTargetsRequestRequestTypeDef,
    RegisterTargetsResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessLogSubscriptionRequestRequestTypeDef,
    UpdateAccessLogSubscriptionResponseTypeDef,
    UpdateListenerRequestRequestTypeDef,
    UpdateListenerResponseTypeDef,
    UpdateRuleRequestRequestTypeDef,
    UpdateRuleResponseTypeDef,
    UpdateServiceNetworkRequestRequestTypeDef,
    UpdateServiceNetworkResponseTypeDef,
    UpdateServiceNetworkVpcAssociationRequestRequestTypeDef,
    UpdateServiceNetworkVpcAssociationResponseTypeDef,
    UpdateServiceRequestRequestTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateTargetGroupRequestRequestTypeDef,
    UpdateTargetGroupResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("VPCLatticeClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class VPCLatticeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        VPCLatticeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#generate_presigned_url)
        """

    def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/close.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#close)
        """

    def batch_update_rule(
        self, **kwargs: Unpack[BatchUpdateRuleRequestRequestTypeDef]
    ) -> BatchUpdateRuleResponseTypeDef:
        """
        Updates the listener rules in a batch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/batch_update_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#batch_update_rule)
        """

    def create_access_log_subscription(
        self, **kwargs: Unpack[CreateAccessLogSubscriptionRequestRequestTypeDef]
    ) -> CreateAccessLogSubscriptionResponseTypeDef:
        """
        Enables access logs to be sent to Amazon CloudWatch, Amazon S3, and Amazon
        Kinesis Data Firehose.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_access_log_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_access_log_subscription)
        """

    def create_listener(
        self, **kwargs: Unpack[CreateListenerRequestRequestTypeDef]
    ) -> CreateListenerResponseTypeDef:
        """
        Creates a listener for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_listener.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_listener)
        """

    def create_rule(
        self, **kwargs: Unpack[CreateRuleRequestRequestTypeDef]
    ) -> CreateRuleResponseTypeDef:
        """
        Creates a listener rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_rule)
        """

    def create_service(
        self, **kwargs: Unpack[CreateServiceRequestRequestTypeDef]
    ) -> CreateServiceResponseTypeDef:
        """
        Creates a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_service)
        """

    def create_service_network(
        self, **kwargs: Unpack[CreateServiceNetworkRequestRequestTypeDef]
    ) -> CreateServiceNetworkResponseTypeDef:
        """
        Creates a service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_service_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_service_network)
        """

    def create_service_network_service_association(
        self, **kwargs: Unpack[CreateServiceNetworkServiceAssociationRequestRequestTypeDef]
    ) -> CreateServiceNetworkServiceAssociationResponseTypeDef:
        """
        Associates a service with a service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_service_network_service_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_service_network_service_association)
        """

    def create_service_network_vpc_association(
        self, **kwargs: Unpack[CreateServiceNetworkVpcAssociationRequestRequestTypeDef]
    ) -> CreateServiceNetworkVpcAssociationResponseTypeDef:
        """
        Associates a VPC with a service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_service_network_vpc_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_service_network_vpc_association)
        """

    def create_target_group(
        self, **kwargs: Unpack[CreateTargetGroupRequestRequestTypeDef]
    ) -> CreateTargetGroupResponseTypeDef:
        """
        Creates a target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/create_target_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#create_target_group)
        """

    def delete_access_log_subscription(
        self, **kwargs: Unpack[DeleteAccessLogSubscriptionRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified access log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_access_log_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_access_log_subscription)
        """

    def delete_auth_policy(
        self, **kwargs: Unpack[DeleteAuthPolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified auth policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_auth_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_auth_policy)
        """

    def delete_listener(
        self, **kwargs: Unpack[DeleteListenerRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_listener.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_listener)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_resource_policy)
        """

    def delete_rule(self, **kwargs: Unpack[DeleteRuleRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a listener rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_rule)
        """

    def delete_service(
        self, **kwargs: Unpack[DeleteServiceRequestRequestTypeDef]
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_service)
        """

    def delete_service_network(
        self, **kwargs: Unpack[DeleteServiceNetworkRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_service_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_service_network)
        """

    def delete_service_network_service_association(
        self, **kwargs: Unpack[DeleteServiceNetworkServiceAssociationRequestRequestTypeDef]
    ) -> DeleteServiceNetworkServiceAssociationResponseTypeDef:
        """
        Deletes the association between a specified service and the specific service
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_service_network_service_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_service_network_service_association)
        """

    def delete_service_network_vpc_association(
        self, **kwargs: Unpack[DeleteServiceNetworkVpcAssociationRequestRequestTypeDef]
    ) -> DeleteServiceNetworkVpcAssociationResponseTypeDef:
        """
        Disassociates the VPC from the service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_service_network_vpc_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_service_network_vpc_association)
        """

    def delete_target_group(
        self, **kwargs: Unpack[DeleteTargetGroupRequestRequestTypeDef]
    ) -> DeleteTargetGroupResponseTypeDef:
        """
        Deletes a target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/delete_target_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#delete_target_group)
        """

    def deregister_targets(
        self, **kwargs: Unpack[DeregisterTargetsRequestRequestTypeDef]
    ) -> DeregisterTargetsResponseTypeDef:
        """
        Deregisters the specified targets from the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/deregister_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#deregister_targets)
        """

    def get_access_log_subscription(
        self, **kwargs: Unpack[GetAccessLogSubscriptionRequestRequestTypeDef]
    ) -> GetAccessLogSubscriptionResponseTypeDef:
        """
        Retrieves information about the specified access log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_access_log_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_access_log_subscription)
        """

    def get_auth_policy(
        self, **kwargs: Unpack[GetAuthPolicyRequestRequestTypeDef]
    ) -> GetAuthPolicyResponseTypeDef:
        """
        Retrieves information about the auth policy for the specified service or
        service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_auth_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_auth_policy)
        """

    def get_listener(
        self, **kwargs: Unpack[GetListenerRequestRequestTypeDef]
    ) -> GetListenerResponseTypeDef:
        """
        Retrieves information about the specified listener for the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_listener.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_listener)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves information about the resource policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_resource_policy)
        """

    def get_rule(self, **kwargs: Unpack[GetRuleRequestRequestTypeDef]) -> GetRuleResponseTypeDef:
        """
        Retrieves information about listener rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_rule)
        """

    def get_service(
        self, **kwargs: Unpack[GetServiceRequestRequestTypeDef]
    ) -> GetServiceResponseTypeDef:
        """
        Retrieves information about the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_service)
        """

    def get_service_network(
        self, **kwargs: Unpack[GetServiceNetworkRequestRequestTypeDef]
    ) -> GetServiceNetworkResponseTypeDef:
        """
        Retrieves information about the specified service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_service_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_service_network)
        """

    def get_service_network_service_association(
        self, **kwargs: Unpack[GetServiceNetworkServiceAssociationRequestRequestTypeDef]
    ) -> GetServiceNetworkServiceAssociationResponseTypeDef:
        """
        Retrieves information about the specified association between a service network
        and a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_service_network_service_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_service_network_service_association)
        """

    def get_service_network_vpc_association(
        self, **kwargs: Unpack[GetServiceNetworkVpcAssociationRequestRequestTypeDef]
    ) -> GetServiceNetworkVpcAssociationResponseTypeDef:
        """
        Retrieves information about the association between a service network and a VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_service_network_vpc_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_service_network_vpc_association)
        """

    def get_target_group(
        self, **kwargs: Unpack[GetTargetGroupRequestRequestTypeDef]
    ) -> GetTargetGroupResponseTypeDef:
        """
        Retrieves information about the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_target_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_target_group)
        """

    def list_access_log_subscriptions(
        self, **kwargs: Unpack[ListAccessLogSubscriptionsRequestRequestTypeDef]
    ) -> ListAccessLogSubscriptionsResponseTypeDef:
        """
        Lists all access log subscriptions for the specified service network or service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_access_log_subscriptions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_access_log_subscriptions)
        """

    def list_listeners(
        self, **kwargs: Unpack[ListListenersRequestRequestTypeDef]
    ) -> ListListenersResponseTypeDef:
        """
        Lists the listeners for the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_listeners.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_listeners)
        """

    def list_rules(
        self, **kwargs: Unpack[ListRulesRequestRequestTypeDef]
    ) -> ListRulesResponseTypeDef:
        """
        Lists the rules for the listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_rules)
        """

    def list_service_network_service_associations(
        self, **kwargs: Unpack[ListServiceNetworkServiceAssociationsRequestRequestTypeDef]
    ) -> ListServiceNetworkServiceAssociationsResponseTypeDef:
        """
        Lists the associations between the service network and the service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_service_network_service_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_service_network_service_associations)
        """

    def list_service_network_vpc_associations(
        self, **kwargs: Unpack[ListServiceNetworkVpcAssociationsRequestRequestTypeDef]
    ) -> ListServiceNetworkVpcAssociationsResponseTypeDef:
        """
        Lists the service network and VPC associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_service_network_vpc_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_service_network_vpc_associations)
        """

    def list_service_networks(
        self, **kwargs: Unpack[ListServiceNetworksRequestRequestTypeDef]
    ) -> ListServiceNetworksResponseTypeDef:
        """
        Lists the service networks owned by the caller account or shared with the
        caller account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_service_networks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_service_networks)
        """

    def list_services(
        self, **kwargs: Unpack[ListServicesRequestRequestTypeDef]
    ) -> ListServicesResponseTypeDef:
        """
        Lists the services owned by the caller account or shared with the caller
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_services.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_services)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_tags_for_resource)
        """

    def list_target_groups(
        self, **kwargs: Unpack[ListTargetGroupsRequestRequestTypeDef]
    ) -> ListTargetGroupsResponseTypeDef:
        """
        Lists your target groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_target_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_target_groups)
        """

    def list_targets(
        self, **kwargs: Unpack[ListTargetsRequestRequestTypeDef]
    ) -> ListTargetsResponseTypeDef:
        """
        Lists the targets for the target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/list_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#list_targets)
        """

    def put_auth_policy(
        self, **kwargs: Unpack[PutAuthPolicyRequestRequestTypeDef]
    ) -> PutAuthPolicyResponseTypeDef:
        """
        Creates or updates the auth policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/put_auth_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#put_auth_policy)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a resource-based permission policy to a service or service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#put_resource_policy)
        """

    def register_targets(
        self, **kwargs: Unpack[RegisterTargetsRequestRequestTypeDef]
    ) -> RegisterTargetsResponseTypeDef:
        """
        Registers the targets with the target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/register_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#register_targets)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#untag_resource)
        """

    def update_access_log_subscription(
        self, **kwargs: Unpack[UpdateAccessLogSubscriptionRequestRequestTypeDef]
    ) -> UpdateAccessLogSubscriptionResponseTypeDef:
        """
        Updates the specified access log subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_access_log_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_access_log_subscription)
        """

    def update_listener(
        self, **kwargs: Unpack[UpdateListenerRequestRequestTypeDef]
    ) -> UpdateListenerResponseTypeDef:
        """
        Updates the specified listener for the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_listener.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_listener)
        """

    def update_rule(
        self, **kwargs: Unpack[UpdateRuleRequestRequestTypeDef]
    ) -> UpdateRuleResponseTypeDef:
        """
        Updates a rule for the listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_rule)
        """

    def update_service(
        self, **kwargs: Unpack[UpdateServiceRequestRequestTypeDef]
    ) -> UpdateServiceResponseTypeDef:
        """
        Updates the specified service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_service.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_service)
        """

    def update_service_network(
        self, **kwargs: Unpack[UpdateServiceNetworkRequestRequestTypeDef]
    ) -> UpdateServiceNetworkResponseTypeDef:
        """
        Updates the specified service network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_service_network.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_service_network)
        """

    def update_service_network_vpc_association(
        self, **kwargs: Unpack[UpdateServiceNetworkVpcAssociationRequestRequestTypeDef]
    ) -> UpdateServiceNetworkVpcAssociationResponseTypeDef:
        """
        Updates the service network and VPC association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_service_network_vpc_association.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_service_network_vpc_association)
        """

    def update_target_group(
        self, **kwargs: Unpack[UpdateTargetGroupRequestRequestTypeDef]
    ) -> UpdateTargetGroupResponseTypeDef:
        """
        Updates the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/update_target_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#update_target_group)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_access_log_subscriptions"]
    ) -> ListAccessLogSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_listeners"]) -> ListListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_network_service_associations"]
    ) -> ListServiceNetworkServiceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_network_vpc_associations"]
    ) -> ListServiceNetworkVpcAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_networks"]
    ) -> ListServiceNetworksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_target_groups"]
    ) -> ListTargetGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_targets"]) -> ListTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_vpc_lattice/client/#get_paginator)
        """
