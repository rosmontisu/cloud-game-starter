using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

class Server
{
    private static int connectionCount = 0;

    static async Task Main(string[] args)
    {
        var listener = new TcpListener(IPAddress.Any, 7777);
        listener.Start();
        Console.WriteLine("Server started on port 7777");

        while (true)
        {
            var client = await listener.AcceptTcpClientAsync();
            Interlocked.Increment(ref connectionCount);
            Console.WriteLine($"Client connected from {client.Client.RemoteEndPoint}. Total clients: {connectionCount}");
            _ = HandleClientAsync(client); // 비동기적으로 클라이언트 처리
        }
    }

    static async Task HandleClientAsync(TcpClient client)
    {
        var stream = client.GetStream();
        var buffer = new byte[1024];
        int bytesRead;

        try
        {
            while ((bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length)) != 0)
            {
                // Echo back to the client
                await stream.WriteAsync(buffer, 0, bytesRead);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error during echo: {ex.Message}");
        }
        finally
        {
            Interlocked.Decrement(ref connectionCount);
            Console.WriteLine($"Client disconnected from {client.Client.RemoteEndPoint}. Total clients: {connectionCount}");
            client.Close();
        }
    }
}