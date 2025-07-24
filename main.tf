# 1. provider 설정 (AWS 리전)
provider "aws" {
  region = "ap-northeast-2" # (ap-northeast-2 : 서울)
}

# 2. 보안 그룹 cgs_sg 생성
resource "aws_security_group" "cgs_sg" {
  name        = "cgs-server-sg"
  description = "Allow inbound traffic for CGS server"

  # ingress : 인바운드 트래픽을 허용하는 규칙
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"         # SSH 접속을 위한 규칙
    cidr_blocks = ["0.0.0.0/0"] # 주의! : 실제 서비스에서는 특정 IP만 허용해야 함
  }

  ingress {
    from_port   = 7777
    to_port     = 7777
    protocol    = "tcp" # CGS 서버가 사용하는 포트
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 외부로 나가는 모든 트래픽은 허용
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1은 모든 프로토콜을 의미
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 최신 AMI ID를 동적으로 서치 [amazon_linux_2 = data.aws_ami.amazon_linux_2.id] 
# 하드코딩 방지
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 3. EC2 인스턴스 생성 & sample server
variable "server_language" {
  type        = string
  description = "The language of the sample server to deploy (go or csharp)."
  default     = "go"
}

resource "aws_instance" "cgs_server" {
  # ami = "ami-<ID>" # Amazon Linux 2 AMI (ap-northeast-2)
  ami             = data.aws_ami.amazon_linux_2.id # 위에서 동적으로 찾은 AMI ID 사용
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.cgs_sg.name] # 위에서 생성한 보안 그룹을 적용

  key_name = "cgs-key" # EC2 인스턴스에 접근하기 위한 SSH 키 페어 이름 - pem 만들어오기

  # user_data : EC2 인스턴스가 시작될 때 실행되는 스크립트
  user_data = <<-EOF

        #!/bin/bash
        APP_DIR="/home/ec2-user/app"
        LOG_FILE="/home/ec2-user/server.log"

        # 공통 작업: 기본 패키지 업데이트, git 설치
        yum update -y
        yum install -y git

        # 공통 작업: git clone
        sudo -u ec2-user git clone https://github.com/rosmontisu/cloud-game-starter.git $APP_DIR

        # 공통 작업: 로그 파일 생성 및 권한 설정
        touch $LOG_FILE
        chown ec2-user:ec2-user $LOG_FILE

        ## 선택된 언어에 따라 다른 작업 수행

        # C# 서버 배포
        if [ "$${server_language}" == "csharp" ]; then # '$' -> '$$' (이스케이프)
          
          echo "Deploying C# server..." > $LOG_FILE
          rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm
          yum install -y dotnet-sdk-7.0 # .NET 7 SDK 설치 (Amazon Linux 2 기준)
          
          cd $APP_DIR/samples/csharp-echo
          # C# 서버를 백그라운드에서 실행
          sudo -u ec2-user nohup dotnet run > $LOG_FILE 2>&1 &

        # 기본값 (Go) 배포
        else
          echo "Deploying Go server..." > $LOG_FILE
          yum install -y golang

          cd $APP_DIR/samples/go-echo
          export GOCACHE=/tmp/gocache
          go build -o server .
          # Go 서버를 백그라운드에서 실행
          sudo -u ec2-user nohup ./server > $LOG_FILE 2>&1 &

    fi
    EOF

  tags = {
    Name = "CGS-GameServer"
  }
}

# 4. 배포된 서버의 퍼블릭 IP 주소 출력
output "server_public_ip" {
  value = aws_instance.cgs_server.public_ip
}