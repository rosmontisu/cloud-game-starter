#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <asio.hpp>

// 각 클라이언트 스레드가 실행할 작업
void client_task(const std::string& host, const std::string& port) 
{
    try 
    {
        asio::io_context io_context;
        asio::ip::tcp::socket socket(io_context);
        asio::ip::tcp::resolver resolver(io_context);

        // 서버 주소와 포트로 접속 시도
        asio::connect(socket, resolver.resolve(host, port));

        // 접속 성공 후, 간단한 메시지를 보내고 에코를 받아서 연결 확인
        std::string message = "Hello from client " + std::to_string(std::hash<std::thread::id>{}(std::this_thread::get_id())) + "\n";
        asio::write(socket, asio::buffer(message));
        
        char reply[1024];
        size_t reply_length = socket.read_some(asio::buffer(reply, 1024));

        // 서버와의 연결을 10분간 유지 (데모용)
        std::this_thread::sleep_for(std::chrono::minutes(10));

    } 
    catch (std::exception& e) 
    {
        // 접속 실패 또는 연결 중 에러 발생 시
        std::cerr << "Client thread error: " << e.what() << std::endl;
    }
}

int main() 
{
    std::string host;
    std::string port;
    int num_clients;

    std::cout << "===== CGS Load Tester =====" << std::endl;
    std::cout << "Enter Server IP: ";
    std::cin >> host;
    std::cout << "Enter Server Port (e.g., 7777): ";
    std::cin >> port;
    std::cout << "Enter number of concurrent clients: ";
    std::cin >> num_clients;

    if (num_clients <= 0) 
    {
        std::cerr << "Number of clients must be positive." << std::endl;
        return 1;
    }

    std::cout << "\nLaunching " << num_clients << " clients to " << host << ":" << port << "..." << std::endl;

    std::vector<std::thread> threads;
    for (int i = 0; i < num_clients; ++i) 
    {
        // 각 클라이언트를 별도의 스레드로 생성하여 실행
        threads.emplace_back(client_task, host, port);
        std::cout << "Launched client " << i + 1 << std::endl;
        // (선택사항) 너무 빠르게 접속하는 것을 방지하기 위해 약간의 딜레이
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    std::cout << "\nAll clients launched. They will stay connected for 10 minutes." << std::endl;
    std::cout << "Check the 'cgs logs' terminal to see the connections." << std::endl;
    
    // 모든 스레드가 끝날 때까지 대기
    for (auto& th : threads) 
    {
        th.join();
    }

    return 0;
}