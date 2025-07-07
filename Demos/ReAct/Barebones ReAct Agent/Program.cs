﻿using SimpleLLMAgents;
using SimpleLLMAgents.Tools;

// Get API key from environment variable or prompt user to enter it
string apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? string.Empty;
if (string.IsNullOrEmpty(apiKey))
{
    Console.Write("Please enter your OpenAI API key: ");
    apiKey = Console.ReadLine() ?? string.Empty;
    if (string.IsNullOrEmpty(apiKey))
    {
        Console.WriteLine("No API key provided. Exiting...");
        return;
    }
}

var llm = new ChatLlm(apiKey: apiKey);

var agent = new ReActAgent(llm, new List<ITool> { new CalculatorTool() });
var response = await agent.Run("Calculate sqrt(3 + 5 / 7 * 9)");

Console.WriteLine("### " + response);
