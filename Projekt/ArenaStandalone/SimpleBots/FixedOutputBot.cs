using System.Collections;
using System.Collections.Generic;

public class FixedOutputBot : GamePlayerController
{
    private List<float> desiredOutput;

    public FixedOutputBot(List<float> desiredOutput = null)
    {
        if (desiredOutput == null)
        {
            this.desiredOutput = new List<float> { 0f, 0f, 0f, 0f };
        }
        else
        {
            this.desiredOutput = desiredOutput;
        }
    }

    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        for (int i = 0; i < 4; i++)
        {
            result[i] = desiredOutput[i];
        }

        return result;
    }
}