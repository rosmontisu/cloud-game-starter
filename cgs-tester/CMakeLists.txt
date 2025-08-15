cmake_minimum_required(VERSION 3.15)
project(cgs-tester CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(cgs_tester main.cpp)

# Boost 라이브러리 찾기
find_package(Boost COMPONENTS system thread REQUIRED)
if(Boost_FOUND)
    target_link_libraries(cgs_tester PRIVATE Boost::system Boost::thread)
endif()

# Asio (헤더 전용 라이브러리) 경로 추가
find_package(asio REQUIRED)
if(asio_FOUND)
    # asio::headers 대신, asio_INCLUDE_DIRS 변수를 사용하여 헤더 경로를 직접 추가 -> 오류수정용
    target_include_directories(cgs_tester PRIVATE ${asio_INCLUDE_DIRS})
endif()

# Visual Studio에서 콘솔 창이 바로 닫히지 않도록 하는 설정
if(MSVC)
    target_compile_definitions(cgs_tester PRIVATE _CONSOLE)
endif()