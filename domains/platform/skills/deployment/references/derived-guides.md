# Deployment — derived guides

Part of `platform:deployment`.

## Cloud Architect

<!-- source: Jeffallan/claude-skills skills/cloud-architect/SKILL.md#common-patterns-with-examples -->

### Common Patterns with Examples

#### Least-Privilege IAM (Zero-Trust)

Rather than broad policies, scope permissions to specific resources and actions:

```bash
# AWS: create a scoped role for an application
aws iam create-role \
  --role-name AppRole \
  --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy \
  --role-name AppRole \
  --policy-name AppInlinePolicy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    }]
  }'
```

```hcl
# Terraform equivalent
resource "aws_iam_role" "app_role" {
  name               = "AppRole"
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy" "app_policy" {
  role = aws_iam_role.app_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "${aws_s3_bucket.app.arn}/*"
    }]
  })
}
```

#### VPC with Public/Private Subnets (Terraform)

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "main", CostCenter = var.cost_center }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet("10.0.0.0/16", 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet("10.0.0.0/16", 8, count.index + 10)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
}
```

#### Auto-Scaling Group (Terraform)

```hcl
resource "aws_autoscaling_group" "app" {
  desired_capacity    = 2
  min_size            = 1
  max_size            = 10
  vpc_zone_identifier = aws_subnet.private[*].id

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "CostCenter"
    value               = var.cost_center
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "cpu_target" {
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60.0
  }
}
```

#### Cost Analysis CLI

```bash
# AWS: identify top cost drivers for the last 30 days
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[*].{Service:Keys[0],Cost:Metrics.UnblendedCost.Amount}' \
  --output table

# Azure: review spend by resource group
az consumption usage list \
  --start-date $(date -d '30 days ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --query "[].{ResourceGroup:resourceGroup,Cost:pretaxCost,Currency:currency}" \
  --output table
```

## Hybrid Cloud Networking

<!-- source: wshobson/agents plugins/cloud-infrastructure/skills/hybrid-cloud-networking/SKILL.md#connection-options -->

### Connection Options

#### AWS Connectivity

##### 1. Site-to-Site VPN

- IPSec VPN over internet
- Up to 1.25 Gbps per tunnel
- Cost-effective for moderate bandwidth
- Higher latency, internet-dependent

```hcl
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-vpn-gateway"
  }
}

resource "aws_customer_gateway" "main" {
  bgp_asn    = 65000
  ip_address = "203.0.113.1"
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = false
}
```

##### 2. AWS Direct Connect

- Dedicated network connection
- 1 Gbps to 100 Gbps
- Lower latency, consistent bandwidth
- More expensive, setup time required

**Reference:** See `references/direct-connect.md`

#### Azure Connectivity

##### 1. Site-to-Site VPN

```hcl
resource "azurerm_virtual_network_gateway" "vpn" {
  name                = "vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = "VpnGw1"

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

##### 2. Azure ExpressRoute

- Private connection via connectivity provider
- Up to 100 Gbps
- Low latency, high reliability
- Premium for global connectivity

#### GCP Connectivity

##### 1. Cloud VPN

- IPSec VPN (Classic or HA VPN)
- HA VPN: 99.99% SLA
- Up to 3 Gbps per tunnel

##### 2. Cloud Interconnect

- Dedicated (10 Gbps, 100 Gbps)
- Partner (50 Mbps to 50 Gbps)
- Lower latency than VPN

#### OCI Connectivity

##### 1. IPSec VPN Connect

- IPSec VPN with redundant tunnels
- Dynamic routing through DRG
- Good fit for branch offices and migration phases

##### 2. OCI FastConnect

- Private dedicated connectivity through Oracle or partner edge
- Suitable for predictable throughput and lower-latency hybrid traffic
- Commonly paired with DRG for hub-and-spoke designs

## Multi-Cloud Architecture

<!-- source: wshobson/agents plugins/cloud-infrastructure/skills/multi-cloud-architecture/SKILL.md#cloud-service-comparison -->

### Cloud Service Comparison

#### Compute Services

| AWS     | Azure               | GCP             | OCI                 | Use Case           |
| ------- | ------------------- | --------------- | ------------------- | ------------------ |
| EC2     | Virtual Machines    | Compute Engine  | Compute             | IaaS VMs           |
| ECS     | Container Instances | Cloud Run       | Container Instances | Containers         |
| EKS     | AKS                 | GKE             | OKE                 | Kubernetes         |
| Lambda  | Functions           | Cloud Functions | Functions           | Serverless         |
| Fargate | Container Apps      | Cloud Run       | Container Instances | Managed containers |

#### Storage Services

| AWS     | Azure           | GCP             | OCI            | Use Case       |
| ------- | --------------- | --------------- | -------------- | -------------- |
| S3      | Blob Storage    | Cloud Storage   | Object Storage | Object storage |
| EBS     | Managed Disks   | Persistent Disk | Block Volumes  | Block storage  |
| EFS     | Azure Files     | Filestore       | File Storage   | File storage   |
| Glacier | Archive Storage | Archive Storage | Archive Storage | Cold storage   |

#### Database Services

| AWS         | Azure            | GCP           | OCI                 | Use Case        |
| ----------- | ---------------- | ------------- | ------------------- | --------------- |
| RDS         | SQL Database     | Cloud SQL     | MySQL HeatWave      | Managed SQL     |
| DynamoDB    | Cosmos DB        | Firestore     | NoSQL Database      | NoSQL           |
| Aurora      | PostgreSQL/MySQL | Cloud Spanner | Autonomous Database | Distributed SQL |
| ElastiCache | Cache for Redis  | Memorystore   | OCI Cache           | Caching         |

**Reference:** See `references/service-comparison.md` for complete comparison

## Docker Expert

<!-- source: davila7/claude-code-templates cli-tool/components/skills/development/docker-expert/SKILL.md#common-issue-diagnostics -->

### Common Issue Diagnostics

#### Build Performance Issues
**Symptoms**: Slow builds (10+ minutes), frequent cache invalidation
**Root causes**: Poor layer ordering, large build context, no caching strategy
**Solutions**: Multi-stage builds, .dockerignore optimization, dependency caching

#### Security Vulnerabilities  
**Symptoms**: Security scan failures, exposed secrets, root execution
**Root causes**: Outdated base images, hardcoded secrets, default user
**Solutions**: Regular base updates, secrets management, non-root configuration

#### Image Size Problems
**Symptoms**: Images over 1GB, deployment slowness
**Root causes**: Unnecessary files, build tools in production, poor base selection
**Solutions**: Distroless images, multi-stage optimization, artifact selection

#### Networking Issues
**Symptoms**: Service communication failures, DNS resolution errors
**Root causes**: Missing networks, port conflicts, service naming
**Solutions**: Custom networks, health checks, proper service discovery

#### Development Workflow Problems
**Symptoms**: Hot reload failures, debugging difficulties, slow iteration
**Root causes**: Volume mounting issues, port configuration, environment mismatch
**Solutions**: Development-specific targets, proper volume strategy, debug configuration
