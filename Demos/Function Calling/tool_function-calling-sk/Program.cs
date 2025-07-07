
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using FunctionCallingWithSemanticKernel.Plugins;

var openAiApiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");

var kernel = GetKernel();

Console.WriteLine("Hello, I am an AI assistant that can answer simple math questions.");
Console.WriteLine("Please ask me questions like \"What is 2 x 2\" or \"What is square root of 3\" etc.");
Console.WriteLine("To quit, simply type quit.");
Console.WriteLine("");
Console.WriteLine("Now ask me a math question...");

do
{
    Console.Write("Your input please: ");
    var prompt = Console.ReadLine();

    if (!string.IsNullOrWhiteSpace(prompt))
    {
        if (prompt.ToLowerInvariant() == "quit")
        {
            Console.WriteLine("Bye.");
            break;
        }
        else
        {
            var result = await InvokeKernelFunctionAsync(prompt);
            Console.WriteLine($"RESULT: {result}");
        }
    }
} while (true);

async Task<string> InvokeKernelFunctionAsync(string prompt)
{
    try
    {
        var chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

        var chatHistory = new ChatHistory();
        chatHistory.AddUserMessage(prompt);

        var result = await chatCompletionService.GetChatMessageContentAsync(chatHistory,
            new OpenAIPromptExecutionSettings()
            {
                ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions,
                Temperature = 0
            }, kernel);

        return result.Content ?? "I'm sorry, but I couldn't generate a response.";
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.Message);
        Console.WriteLine(ex.StackTrace);
        return "An error occurred while processing your request.";
    }
}

Kernel GetKernel()
{
    var builder = Kernel.CreateBuilder()
        .AddOpenAIChatCompletion("gpt-4o", openAiApiKey);

    builder.Plugins.AddFromType<CalculatorPlugin>();

    return builder.Build();
}
