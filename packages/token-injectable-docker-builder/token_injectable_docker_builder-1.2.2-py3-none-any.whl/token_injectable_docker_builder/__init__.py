r'''
# TokenInjectableDockerBuilder

The `TokenInjectableDockerBuilder` is a flexible AWS CDK construct that enables the usage of AWS CDK tokens in the building, pushing, and deployment of Docker images to Amazon Elastic Container Registry (ECR). It leverages AWS CodeBuild and Lambda custom resources.

---


## Why?

AWS CDK already provides mechanisms for creating deployable assets using Docker, such as [DockerImageAsset](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ecr_assets.DockerImageAsset.html) and [DockerImageCode](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.DockerImageCode.html), but these constructs are limited because they cannot accept CDK tokens as build-args. The `TokenInjectableDockerBuilder` allows injecting CDK tokens as build-time arguments into Docker-based assets, enabling more dynamic dependency relationships.

For example, a Next.js frontend Docker image may require an API Gateway URL as an argument to create a reference from the UI to the associated API in a given deployment. With this construct, you can deploy the API Gateway first, then pass its URL as a build-time argument to the Next.js Docker image. As a result, your Next.js frontend can dynamically fetch data from the API Gateway without hardcoding the URL, or needing mutliple sepereate Stacks.

---


## Features

* **Build and Push Docker Images**: Automatically builds and pushes Docker images to ECR.
* **Token Support**: Supports custom build arguments for Docker builds, including CDK tokens resolved at deployment time.
* **Custom Install and Pre-Build Commands**: Allows specifying custom commands to run during the `install` and `pre_build` phases of the CodeBuild build process.
* **VPC Configuration**: Supports deploying the CodeBuild project within a VPC, with customizable security groups and subnet selection.
* **Docker Login**: Supports Docker login using credentials stored in AWS Secrets Manager.
* **ECR Repository Management**: Creates an ECR repository with lifecycle rules and encryption.
* **Integration with ECS and Lambda**: Provides outputs for use in AWS ECS and AWS Lambda.

---


## Installation

### For NPM

Install the construct using NPM:

```bash
npm install token-injectable-docker-builder
```

### For Python

Install the construct using pip:

```bash
pip install token-injectable-docker-builder
```

---


## Constructor

### `TokenInjectableDockerBuilder`

#### Parameters

* **`scope`**: The construct's parent scope.
* **`id`**: The construct ID.
* **`props`**: Configuration properties.

#### Properties in `TokenInjectableDockerBuilderProps`

| Property                 | Type                        | Required | Description                                                                                                                                                           |
|--------------------------|-----------------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `path`                   | `string`                    | Yes      | The file path to the Dockerfile or source code directory.                                                                                                             |
| `buildArgs`              | `{ [key: string]: string }` | No       | Build arguments to pass to the Docker build process. These are transformed into `--build-arg` flags. To use in Dockerfile, leverage the `ARG` keyword. For more details, please see the [official Docker docs](https://docs.docker.com/build/building/variables/).                                                                  |
| `dockerLoginSecretArn`   | `string`                    | No       | ARN of an AWS Secrets Manager secret for Docker credentials. Skips login if not provided.                                                                              |
| `vpc`                    | `IVpc`                      | No       | The VPC in which the CodeBuild project will be deployed. If provided, the CodeBuild project will be launched within the specified VPC.                                 |
| `securityGroups`         | `ISecurityGroup[]`          | No       | The security groups to attach to the CodeBuild project. These should define the network access rules for the CodeBuild project.                                        |
| `subnetSelection`        | `SubnetSelection`           | No       | The subnet selection to specify which subnets to use within the VPC. Allows the user to select private, public, or isolated subnets.                                   |
| `installCommands`        | `string[]`                  | No       | Custom commands to run during the `install` phase of the CodeBuild build process. Will be executed before Docker image is built. Useful for installing necessary dependencies for running pre-build scripts.                                                                                   |
| `preBuildCommands`       | `string[]`                  | No       | Custom commands to run during the `pre_build` phase of the CodeBuild build process. Will be executed before Docker image is built. Useful for running pre-build scripts, such as to fetch configs.                                                                                   |

---


## Usage Examples

### Simple Usage Example

This example demonstrates the most basic usage of the `TokenInjectableDockerBuilder`, where you specify the path to your Docker context and provide simple build arguments.

#### TypeScript/NPM Example

```python
import * as cdk from 'aws-cdk-lib';
import { TokenInjectableDockerBuilder } from 'token-injectable-docker-builder';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class SimpleStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const dockerBuilder = new TokenInjectableDockerBuilder(this, 'SimpleDockerBuilder', {
      path: './docker', // Path to your Dockerfile or Docker context
      buildArgs: {
        ENV: 'production', // Simple build argument
      },
    });

    // Use in ECS
    new ecs.ContainerDefinition(this, 'SimpleContainer', {
      image: dockerBuilder.containerImage,
      // ... other container properties ...
    });

    // Use in Lambda
    new lambda.Function(this, 'SimpleDockerLambdaFunction', {
      runtime: lambda.Runtime.FROM_IMAGE,
      code: dockerBuilder.dockerImageCode,
      handler: lambda.Handler.FROM_IMAGE,
    });
  }
}
```

#### Python Example

```python
from aws_cdk import (
    aws_ecs as ecs,
    aws_lambda as lambda_,
    core as cdk,
)
from token_injectable_docker_builder import TokenInjectableDockerBuilder

class SimpleStack(cdk.Stack):

    def __init__(self, scope: cdk.App, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        docker_builder = TokenInjectableDockerBuilder(self, "SimpleDockerBuilder",
            path="./docker",  # Path to your Dockerfile or Docker context
            build_args={
                "ENV": "production",  # Simple build argument
            },
        )

        # Use in ECS
        ecs.ContainerDefinition(self, "SimpleContainer",
            image=docker_builder.container_image,
            # ... other container properties ...
        )

        # Use in Lambda
        lambda_.Function(self, "SimpleDockerLambdaFunction",
            runtime=lambda_.Runtime.FROM_IMAGE,
            code=docker_builder.docker_image_code,
            handler=lambda_.Handler.FROM_IMAGE
        )
```

---


### Advanced Usage Example

This example demonstrates more advanced usage, including using CDK tokens as build arguments, specifying custom install and pre-build commands, and configuring VPC settings.

#### TypeScript/NPM Example

```python
import * as cdk from 'aws-cdk-lib';
import { TokenInjectableDockerBuilder } from 'token-injectable-docker-builder';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class MyStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Example VPC and security group (optional)
    const vpc = new ec2.Vpc(this, 'MyVpc');
    const securityGroup = new ec2.SecurityGroup(this, 'MySecurityGroup', {
      vpc,
    });

    // Example of using CDK tokens as build arguments
    const myApiGateway = /* ... create or import your API Gateway ... */;

    const dockerBuilder = new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', {
      path: './docker',
      buildArgs: {
        API_URL: myApiGateway.url, // Using CDK token
        ENV: 'production',
      },
      dockerLoginSecretArn: 'arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret',
      vpc,
      securityGroups: [securityGroup],
      subnetSelection: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      installCommands: [
        'echo "Updating package lists..."',
        'apt-get update -y',
        'echo "Installing required packages..."',
        'apt-get install -y curl dnsutils',
      ],
      preBuildCommands: [
        'echo "Fetching configuration from private API..."',
        'curl -o config.json https://api.example.com/config',
      ],
    });

    // Use in ECS
    new ecs.ContainerDefinition(this, 'MyContainer', {
      image: dockerBuilder.containerImage,
      // ... other container properties ...
    });

    // Use in Lambda
    new lambda.Function(this, 'DockerLambdaFunction', {
      runtime: lambda.Runtime.FROM_IMAGE,
      code: dockerBuilder.dockerImageCode,
      handler: lambda.Handler.FROM_IMAGE,
    });
  }
}
```

#### Python Example

```python
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_lambda as lambda_,
    core as cdk,
)
from token_injectable_docker_builder import TokenInjectableDockerBuilder

class MyStack(cdk.Stack):

    def __init__(self, scope: cdk.App, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Example VPC and security group (optional)
        vpc = ec2.Vpc(self, "MyVpc")
        security_group = ec2.SecurityGroup(self, "MySecurityGroup", vpc=vpc)

        # Example of using CDK tokens as build arguments
        my_api_gateway = # ... create or import your API Gateway ...

        docker_builder = TokenInjectableDockerBuilder(self, "MyDockerBuilder",
            path="./docker",
            build_args={
                "API_URL": my_api_gateway.url,  # Using CDK token
                "ENV": "production"
            },
            docker_login_secret_arn="arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret",
            vpc=vpc,
            security_groups=[security_group],
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            install_commands=[
                'echo "Updating package lists..."',
                'apt-get update -y',
                'echo "Installing required packages..."',
                'apt-get install -y curl dnsutils',
            ],
            pre_build_commands=[
                'echo "Fetching configuration from private API..."',
                'curl -o config.json https://api.example.com/config',
            ],
        )

        # Use in ECS
        ecs.ContainerDefinition(self, "MyContainer",
            image=docker_builder.container_image,
            # ... other container properties ...
        )

        # Use in Lambda
        lambda_.Function(self, "DockerLambdaFunction",
            runtime=lambda_.Runtime.FROM_IMAGE,
            code=docker_builder.docker_image_code,
            handler=lambda_.Handler.FROM_IMAGE
        )
```

---


## How It Works

1. **Docker Source**: Packages the source code or Dockerfile specified in the `path` property as an S3 asset.
2. **CodeBuild Project**:

   * Uses the packaged asset and `buildArgs` to build the Docker image.
   * Executes any custom `installCommands` and `preBuildCommands` during the build process.
   * Pushes the image to an ECR repository.
3. **Custom Resource**:

   * Triggers the build process using a Lambda function (`onEvent`).
   * Monitors the build status using another Lambda function (`isComplete`).
4. **Outputs**:

   * `.containerImage`: Returns the Docker image for ECS.
   * `.dockerImageCode`: Returns the Docker image code for Lambda.

---


## IAM Permissions

The construct automatically grants permissions for:

* **CodeBuild**:

  * Pull and push images to ECR.
  * Access to AWS Secrets Manager if `dockerLoginSecretArn` is provided.
  * Access to the KMS key for encryption.
* **Lambda Functions**:

  * Start and monitor CodeBuild builds.
  * Access CloudWatch Logs.
  * Access to the KMS key for encryption.
  * Pull and push images to ECR.

---


## Notes

* **Build Arguments**: Pass custom arguments via `buildArgs` as `--build-arg` flags. CDK tokens can be used to inject dynamic values resolved at deployment time.
* **Custom Commands**: Use `installCommands` and `preBuildCommands` to run custom shell commands during the build process. This can be useful for installing dependencies or fetching configuration files.
* **VPC Configuration**: If your build process requires access to resources within a VPC, you can specify the VPC, security groups, and subnet selection.
* **Docker Login**: If you need to log in to a private Docker registry before building the image, provide the ARN of a secret in AWS Secrets Manager containing the Docker credentials.
* **ECR Repository**: Automatically creates an ECR repository with lifecycle rules to manage image retention, encryption with a KMS key, and image scanning on push.

---


## Troubleshooting

1. **Build Errors**: Check the CodeBuild logs in CloudWatch Logs for detailed error messages.
2. **Lambda Errors**: Check the `onEvent` and `isComplete` Lambda function logs in CloudWatch Logs.
3. **Permissions**: Ensure IAM roles have the required permissions for CodeBuild, ECR, Secrets Manager, and KMS if applicable.
4. **Network Access**: If the build requires network access (e.g., to download dependencies), ensure that the VPC configuration allows outbound internet access, or use a NAT gateway if in private subnets.

---


## Support

For issues or feature requests, please open an issue on [GitHub](https://github.com/AlexTech314/TokenInjectableDockerBuilder).

---


## Reference Links

[![View on Construct Hub](https://constructs.dev/badge?package=token-injectable-docker-builder)](https://constructs.dev/packages/token-injectable-docker-builder)

---


# License

This project is licensed under the terms of the MIT license.

---


# Acknowledgements

* Inspired by the need for more dynamic Docker asset management in AWS CDK.
* Thanks to the AWS CDK community for their continuous support and contributions.

---


Feel free to reach out if you have any questions or need further assistance!
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class TokenInjectableDockerBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="token-injectable-docker-builder.TokenInjectableDockerBuilder",
):
    '''A CDK construct to build and push Docker images to an ECR repository using CodeBuild and Lambda custom resources.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        path: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_login_secret_arn: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param path: The path to the directory containing the Dockerfile or source code.
        :param build_args: Build arguments to pass to the Docker build process. These are transformed into ``--build-arg`` flags.
        :param docker_login_secret_arn: The ARN of the AWS Secrets Manager secret containing Docker login credentials. This secret should store a JSON object with the following structure:: { "username": "my-docker-username", "password": "my-docker-password" } If not provided, the construct will skip Docker login during the build process.
        :param install_commands: Custom commands to run during the install phase. **Example Usage:*:: new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', { path: path.resolve(__dirname, '../app'), installCommands: [ 'echo "Updating package lists..."', 'apt-get update -y', 'echo "Installing required packages..."', 'apt-get install -y curl dnsutils', ], // ... other properties ... }); *This example demonstrates how to install the ``curl`` and ``dnsutils`` packages during the install phase using ``apt-get``, the package manager for Ubuntu-based CodeBuild environments.* Default: - No additional install commands.
        :param pre_build_commands: Custom commands to run during the pre_build phase. **Example Usage:*:: new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', { path: path.resolve(__dirname, '../app'), preBuildCommands: [ 'echo "Fetching configuration from private API..."', 'curl -o config.json https://api.example.com/config', ], // ... other properties ... }); *In this example, the builder fetches a configuration file from a private API before starting the Docker build. This config file will be available in the same directory as your Dockerfile during CDK deployment.* Default: - No additional pre-build commands.
        :param security_groups: The security groups to attach to the CodeBuild project. These should define the network access rules for the CodeBuild project. Default: No security groups are attached.
        :param subnet_selection: The subnet selection to specify which subnets to use within the VPC. Allows the user to select private, public, or isolated subnets. Default: All subnets in the VPC are used.
        :param vpc: The VPC in which the CodeBuild project will be deployed. If provided, the CodeBuild project will be launched within the specified VPC. Default: No VPC is attached, and the CodeBuild project will use public internet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab459e7d115d1d8742a5a5096b6fc8a04c58d19c7ae560c4cfa28a2a885351e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TokenInjectableDockerBuilderProps(
            path=path,
            build_args=build_args,
            docker_login_secret_arn=docker_login_secret_arn,
            install_commands=install_commands,
            pre_build_commands=pre_build_commands,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="dockerImageCode")
    def docker_image_code(self) -> _aws_cdk_aws_lambda_ceddda9d.DockerImageCode:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.DockerImageCode, jsii.get(self, "dockerImageCode"))


@jsii.data_type(
    jsii_type="token-injectable-docker-builder.TokenInjectableDockerBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "build_args": "buildArgs",
        "docker_login_secret_arn": "dockerLoginSecretArn",
        "install_commands": "installCommands",
        "pre_build_commands": "preBuildCommands",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class TokenInjectableDockerBuilderProps:
    def __init__(
        self,
        *,
        path: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_login_secret_arn: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''Properties for the ``TokenInjectableDockerBuilder`` construct.

        :param path: The path to the directory containing the Dockerfile or source code.
        :param build_args: Build arguments to pass to the Docker build process. These are transformed into ``--build-arg`` flags.
        :param docker_login_secret_arn: The ARN of the AWS Secrets Manager secret containing Docker login credentials. This secret should store a JSON object with the following structure:: { "username": "my-docker-username", "password": "my-docker-password" } If not provided, the construct will skip Docker login during the build process.
        :param install_commands: Custom commands to run during the install phase. **Example Usage:*:: new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', { path: path.resolve(__dirname, '../app'), installCommands: [ 'echo "Updating package lists..."', 'apt-get update -y', 'echo "Installing required packages..."', 'apt-get install -y curl dnsutils', ], // ... other properties ... }); *This example demonstrates how to install the ``curl`` and ``dnsutils`` packages during the install phase using ``apt-get``, the package manager for Ubuntu-based CodeBuild environments.* Default: - No additional install commands.
        :param pre_build_commands: Custom commands to run during the pre_build phase. **Example Usage:*:: new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', { path: path.resolve(__dirname, '../app'), preBuildCommands: [ 'echo "Fetching configuration from private API..."', 'curl -o config.json https://api.example.com/config', ], // ... other properties ... }); *In this example, the builder fetches a configuration file from a private API before starting the Docker build. This config file will be available in the same directory as your Dockerfile during CDK deployment.* Default: - No additional pre-build commands.
        :param security_groups: The security groups to attach to the CodeBuild project. These should define the network access rules for the CodeBuild project. Default: No security groups are attached.
        :param subnet_selection: The subnet selection to specify which subnets to use within the VPC. Allows the user to select private, public, or isolated subnets. Default: All subnets in the VPC are used.
        :param vpc: The VPC in which the CodeBuild project will be deployed. If provided, the CodeBuild project will be launched within the specified VPC. Default: No VPC is attached, and the CodeBuild project will use public internet.
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__768a8fd54fa9d30e8a3c9ce21d38fb8896ac969a161df6469697e06a05864286)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument docker_login_secret_arn", value=docker_login_secret_arn, expected_type=type_hints["docker_login_secret_arn"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
            check_type(argname="argument pre_build_commands", value=pre_build_commands, expected_type=type_hints["pre_build_commands"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if docker_login_secret_arn is not None:
            self._values["docker_login_secret_arn"] = docker_login_secret_arn
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if pre_build_commands is not None:
            self._values["pre_build_commands"] = pre_build_commands
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def path(self) -> builtins.str:
        '''The path to the directory containing the Dockerfile or source code.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Build arguments to pass to the Docker build process.

        These are transformed into ``--build-arg`` flags.

        Example::

            {
              TOKEN: 'my-secret-token',
              ENV: 'production'
            }
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_login_secret_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Secrets Manager secret containing Docker login credentials.

        This secret should store a JSON object with the following structure::

           {
             "username": "my-docker-username",
             "password": "my-docker-password"
           }

        If not provided, the construct will skip Docker login during the build process.

        Example::

            'arn:aws:secretsmanager:us-east-1:123456789012:secret:DockerLoginSecret'
        '''
        result = self._values.get("docker_login_secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom commands to run during the install phase.

        **Example Usage:*::

           new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', {
             path: path.resolve(__dirname, '../app'),
             installCommands: [
               'echo "Updating package lists..."',
               'apt-get update -y',
               'echo "Installing required packages..."',
               'apt-get install -y curl dnsutils',
             ],
             // ... other properties ...
           });

        *This example demonstrates how to install the ``curl`` and ``dnsutils`` packages during the install phase using ``apt-get``, the package manager for Ubuntu-based CodeBuild environments.*

        :default: - No additional install commands.
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_build_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom commands to run during the pre_build phase.

        **Example Usage:*::

           new TokenInjectableDockerBuilder(this, 'MyDockerBuilder', {
             path: path.resolve(__dirname, '../app'),
             preBuildCommands: [
               'echo "Fetching configuration from private API..."',
               'curl -o config.json https://api.example.com/config',
             ],
             // ... other properties ...
           });

        *In this example, the builder fetches a configuration file from a private API before starting the Docker build. This config file will be available in the same directory as your Dockerfile during CDK deployment.*

        :default: - No additional pre-build commands.
        '''
        result = self._values.get("pre_build_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The security groups to attach to the CodeBuild project.

        These should define the network access rules for the CodeBuild project.

        :default: No security groups are attached.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The subnet selection to specify which subnets to use within the VPC.

        Allows the user to select private, public, or isolated subnets.

        :default: All subnets in the VPC are used.
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The VPC in which the CodeBuild project will be deployed.

        If provided, the CodeBuild project will be launched within the specified VPC.

        :default: No VPC is attached, and the CodeBuild project will use public internet.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenInjectableDockerBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TokenInjectableDockerBuilder",
    "TokenInjectableDockerBuilderProps",
]

publication.publish()

def _typecheckingstub__aab459e7d115d1d8742a5a5096b6fc8a04c58d19c7ae560c4cfa28a2a885351e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    path: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_login_secret_arn: typing.Optional[builtins.str] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__768a8fd54fa9d30e8a3c9ce21d38fb8896ac969a161df6469697e06a05864286(
    *,
    path: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_login_secret_arn: typing.Optional[builtins.str] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
