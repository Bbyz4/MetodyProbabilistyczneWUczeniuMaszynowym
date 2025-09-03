using System.Collections;
using System.Collections.Generic;

public class SimpleBot0 : GamePlayerController
{
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        result[0] = 0f;
        result[1] = 0f;
        result[2] = 0f;
        result[3] = 0f;

        return result;
    }
}

