using OpenAI;
using OpenAI.Chat;

namespace SimpleLLMAgents;

public class ChatLlm
{
    private string _apiKey;
    private readonly string _model;
    private readonly float _temperature;

    public ChatLlm(string model = "gpt-4o", float temperature = 0.0f, string? apiKey = null)
    {
        _model = model;
        _temperature = temperature;
        _apiKey = apiKey ?? Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? string.Empty;
    }

    public void SetApiKey(string apiKey)
    {
        _apiKey = apiKey;
    }

    public async Task<string> Generate(string prompt, List<string>? stop = null)
    {
        var client = new ChatClient(_model, _apiKey);

        var chatCompletionOptions = new ChatCompletionOptions
        {
            Temperature = _temperature,
        };

        if (stop != null && stop.Count > 0)
        {
            chatCompletionOptions.StopSequences.Clear();
            foreach (var s in stop)
            {
                chatCompletionOptions.StopSequences.Add(s);
            }
        }

        var messages = new List<ChatMessage>
        {
            new UserChatMessage(prompt)
        };

        var response = await client.CompleteChatAsync(messages, chatCompletionOptions);
        
        if (response.Value.Content.Count == 0 || string.IsNullOrEmpty(response.Value.Content[0].Text))
        {
            throw new InvalidOperationException("No content returned from the API");
        }
        
        return response.Value.Content[0].Text;
    }
}
