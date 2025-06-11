# Cloud Game Starter

간단한 명령어로 클라우드에 게임 서버를 배포하는 오픈소스 CLI 툴입니다.

## Our Goal
- 누구나 쉽게 클라우드를 경험하게 합니다.
- 복잡한 인프라 설정 과정을 자동화합니다.
- '요금 폭탄' 걱정 없이 안전하게 테스트할 수 있는 환경을 제공합니다.

---
## Local Environment Setup
1. AWS CLI 설치 및 확인
- [AWS CLI 공식](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS CLI Window msi](https://awscli.amazonaws.com/AWSCLIV2.msi)

```bash
aws --version
```

2. Terraform 설치 및 확인
- [Terraform 공식](https://developer.hashicorp.com/terraform/install)
윈도우용 파일 다운 후 PATH에 추가

```bash
terraform --version
```

3. Python 설치 및 확인
- 현재 py 3.14 사용중
```py
python --version
```

---
## AWS Credential
> 로컬의 aws 및 terraform 명령어가 AWS 클라우스를 제어할 수 있도록 KEY를 발급하고 설정한다.

1. IAM 사용자 생성
- AWS Management Console 로그인
- IAM에서 사용자 생성
- `cgs-admin` 사용자 생성
- `Attach existing policies directly` 권한 설정
- `AdministratorAccess` 권한 정책 설정
    - 해당 권한은 프로젝트 기간 이후, 실제 서비스에서는 절대 사용하면 안됨
             
2. 엑세스 키 발급
- `cgs-admin` 설정으로
- `Create access key` 
- Use case `CLI` 선택
- `Access key` 발급
    - `Secret access key`는 이때 한 번만 확인 가능하므로, 꼭 메모해둘것

3. AWS CLI 설정
- 로컬 터미널에서 `aws configure` 명령을 실행, 발급받은 키를 입력
```bash
aws configure
AWS Access Key ID [None]: "Access key"
AWS Secret Access Key [None]: "Secret access key"
Default region name [None]: ap-northeast-2 # Seoul
Default output format [None]: # None
```

- `AWS STS`로 현재 설정된 자격 증명의 유효성을 확인하자
    - security token service는 임시 자격 증명을 생성/관리하는 서비스
```bash
aws sts get-caller-identity
```
- 아래와 같이 json형태로 잡히면 정상적으로 등록
```bash
{
    "UserId": "AIDAxxxxxxxxxxxxxxxx",
    "Account": "0000000000",
    "Arn": "arn:aws:iam::0000000000:user/cgs-admin"
}
```
- 혹은 `aws s3 ls`로 S3 버킷을 확인하는것도 가능
    - 버킷이 하나도 없다면, 에러 없이 빈 줄이 출력됨
```bash
aws s3 ls
```

