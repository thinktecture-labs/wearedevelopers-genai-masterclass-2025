using OpenAI.Chat;


var apiKey = System.Environment.GetEnvironmentVariable("OPENAI_API_KEY");
if (String.IsNullOrEmpty(apiKey))
{
	Console.Error.WriteLine("OPENAI_API_KEY environment variable is not set");
	return;
}

var model = "gpt-4";
var client = new ChatClient(model, apiKey);

var messages = new List<ChatMessage>([
		new SystemChatMessage("You are a friendly, helpful chat assistant."),
	]);

var completed = false;

Console.CancelKeyPress += (sender, eventArgs) =>
{
	eventArgs.Cancel = true;
	completed = true;
};

while (!completed)
{
	Console.Write("Your input: ");
	var input = Console.ReadLine();

	if (String.IsNullOrEmpty(input)) continue;

	messages.Add(new UserChatMessage(input));

	var response = await client.CompleteChatAsync(messages);
	var answer = response.Value;

	messages.Add(new AssistantChatMessage(answer));
	Console.WriteLine($"AI output: {answer.Content[0].Text}");
}
