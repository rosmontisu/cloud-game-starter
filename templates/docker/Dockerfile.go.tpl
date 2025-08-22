# Multi-stage Build (alpine)

# 1. Build 
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
# go.mod 파일이 있는 디렉토리로 이동
WORKDIR /app/samples/go-echo
RUN go mod tidy && go build -o /server .

# 2. Final 
FROM alpine:latest
# 빌드 스테이지에서 컴파일된 실행 파일만 복사
COPY --from=builder /server /server
# 필요한 CA 인증서
RUN apk --no-cache add ca-certificates

EXPOSE 7777

# 컨테이너 시작 시 실행될 명령어(server)
CMD ["/server"]