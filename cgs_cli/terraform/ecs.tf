# 2. ECS 클러스터, Tack Definition, Fargate 서비스 정의

variable "image_url" {
  type    = string
  description = "The full URL of the Docker image in ECR."
  default = ""
}

# ECS 클러스터 생성
resource "aws_ecs_cluster" "cgs_cluster" {
  name = "cgs-cluster"
}

# ECS Task Definition (컨테이너 설계도 -- 임시)
resource "aws_ecs_task_definition" "cgs_task" {
  family                   = "cgs-game-server-task"
  network_mode             = "awsvpc" # Fargate는 awsvpc 모드 필요
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"  # 0.25 vCPU
  memory                   = "512"  # 512MB

  container_definitions = jsonencode([
    {
      name      = "game-server-container"
      image     = var.image_url
      essential = true
      portMappings = [
        {
          containerPort = 7777
          hostPort      = 7777
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.cgs_logs.name
          "awslogs-region"        = "ap-northeast-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# ECS Service (컨테이너 관리자)
resource "aws_ecs_service" "cgs_service" {
  name            = "cgs-fargate-service"
  cluster         = aws_ecs_cluster.cgs_cluster.id
  task_definition = aws_ecs_task_definition.cgs_task.arn
  desired_count   = 1 # 항상 1개의 컨테이너를 실행
  launch_type     = "FARGATE"

  network_configuration {
    # 기존에 aws_security_group 재사용. 추후에 id참고하도록 수정해도 될듯
    security_groups = [aws_security_group.cgs_sg.id]
    # EC2 인스턴스가 생성될 VPC의 서브넷을 지정
    subnets = data.aws_subnets.default.ids
    assign_public_ip = true # 컨테이너에 공인 IP 할당
  }
}

# 기본 VPC 및 서브넷 정보를 가져오기 위한 데이터 소스
data "aws_vpc" "default" {
  default = true
}
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# CloudWatch 로그 그룹 생성
resource "aws_cloudwatch_log_group" "cgs_logs" {
  name = "/ecs/cgs-game-server"
}