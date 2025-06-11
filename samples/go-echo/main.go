package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"sync"
	"sync/atomic"
)

const (
	HOST = "0.0.0.0"
	PORT = "7777"
	TYPE = "tcp"
)

var connectionCount int32 // 클라이언트 커넥션 카운트 변수

func main() {
	listener, err := net.Listen(TYPE, HOST+":"+PORT)

	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}
	defer listener.Close() // main 종료 전 리스너 닫기


	// -- 서버 시작 메시지 출력 --
	log.Printf("Server started on %s:%s", HOST, PORT) 
	var wg sync.WaitGroup // WaitGroup : 커넥션 핸들링 완료 대기를 위한 그룹

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}
		atomic.AddInt32(&connectionCount, 1) // 커넥션 카운트 증가 (원자적 연산)
		log.Printf("Client connected from %s, Total clients: %d", 
		conn.RemoteAddr(), atomic.LoadInt32(&connectionCount)) 
		// ip:port, 총 커넥션 수 출력

		wg.Add(1) // WaitGroup에 추가 
		go handleRequest(conn, &wg)
	}
}

func handleRequest(conn net.Conn, wg *sync.WaitGroup) {
	defer func() {
		atomic.AddInt32(&connectionCount, -1) // 커넥션 카운트 감소
		log.Printf("Client disconnected from %s, Total clients: %d", 
		conn.RemoteAddr().String(), atomic.LoadInt32(&connectionCount))
		conn.Close()
		wg.Done() // WaitGroup 에서 제거
	}()

	// io.Copy 함수로 읽은 데이터를 다시 소켓에 작성해서 ECHO
	if _, err := io.Copy(conn, conn); err != nil {
		log.Printf("Error during echo: %v", err) 
	}
}
