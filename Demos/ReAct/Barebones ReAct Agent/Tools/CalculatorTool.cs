using System.Globalization;
using AngouriMath;

namespace SimpleLLMAgents.Tools;

public class CalculatorTool : ITool
{
    public string Name => "CalculatorTool";

    public string Description => "Calculator tool to do all kind of math operations. Always use this tool instead of calculating yourself.";

    public string Execute(string inputText)
    {
        Entity expr = inputText;

        return ((decimal)expr.EvalNumerical()).ToString(CultureInfo.InvariantCulture);
    }
}