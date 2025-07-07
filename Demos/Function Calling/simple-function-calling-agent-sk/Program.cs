using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;

public class Program
{
    public static async Task Main(string[] args)
    {
        try
        {
            DotNetEnv.Env.Load();

            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
            var apiEndpoint =
                Environment.GetEnvironmentVariable("OPENAI_API_ENDPOINT")
                ?? "https://api.openai.com/v1";
            var modelName = Environment.GetEnvironmentVariable("OPENAI_MODEL") ?? "gpt-4.1";

            if (string.IsNullOrEmpty(apiKey))
            {
                Console.WriteLine("Error: OPENAI_API_KEY environment variable is not set.");
                Console.WriteLine("Please set it in the .env file or as an environment variable.");
                return;
            }

            var kernel = CreateKernel(apiKey, apiEndpoint, modelName);

            await RunChatLoopAsync(kernel);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"An error occurred: {ex.Message}");
        }
    }

    private static Kernel CreateKernel(string apiKey, string apiEndpoint, string modelName)
    {
        var httpClient = new HttpClient(
            new HttpClientHandler { Proxy = new LocalDebuggingProxy() }
        );

        var builder = Kernel.CreateBuilder();

        // Suppress experimental API warning
#pragma warning disable SKEXP0010
        builder.AddOpenAIChatCompletion(
            modelName,
            new Uri(apiEndpoint),
            apiKey,
            httpClient: httpClient
        );
#pragma warning restore SKEXP0010

        builder.Plugins.AddFromType<EmployeePlugin>("Employees");
        builder.Plugins.AddFromType<BookingPlugin>("Bookings");

        return builder.Build();
    }

    private static async Task RunChatLoopAsync(Kernel kernel)
    {
        Console.WriteLine("Welcome to our Helpful Agent.");
        Console.WriteLine("You can ask questions now.");
        Console.WriteLine("Type 'exit' to quit.");
        Console.WriteLine();

        var chatHistory = new ChatHistory();
        chatHistory.AddSystemMessage(
            @"You're a friendly, helpful chat assistant.
            Only answer questions that relate to your tools, functions, and plugins — no other questions!
            Only list and use the tools you are explicitly provided with as functions in the request."
        );
        chatHistory.AddSystemMessage($"Today is {DateTime.Now:D}.");

        var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

        while (true)
        {
            Console.Write("Your input: ");
            var input = Console.ReadLine();

            if (string.IsNullOrEmpty(input) || input.ToLower() == "exit")
            {
                break;
            }

            chatHistory.AddUserMessage(input);

            try
            {
                var response = await chatCompletionService.GetChatMessageContentAsync(
                    chatHistory,
                    new OpenAIPromptExecutionSettings
                    { 
                        ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions,
                        Temperature = 0,
                    },
                    kernel
                );

                chatHistory.AddAssistantMessage(response.Content ?? string.Empty);

                Console.WriteLine($"Agent output: {response.Content}");
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error: {ex.Message}");
            }
        }

        Console.WriteLine("Goodbye!");
    }
}
