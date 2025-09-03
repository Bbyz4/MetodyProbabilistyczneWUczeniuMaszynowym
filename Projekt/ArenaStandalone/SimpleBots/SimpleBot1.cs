using System.Collections;
using System.Collections.Generic;

public class SimpleBot1 : GamePlayerController
{
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        Pair p1Position = gameInstance.player1.position;
        Pair p2Position = gameInstance.player2.position;

        if (whoAmI == 1)
        {
            if (gameInstance.player2.isDead)
            {
                result[0] = 0f;
                result[1] = 0f;
            }
            else
            {
                result[0] = (p1Position.X < p2Position.X ? 1f : -1f);
                result[1] = (p1Position.Y < p2Position.Y ? 1f : -1f);
            }
        }
        else
        {
            if (gameInstance.player1.isDead)
            {
                result[0] = 0f;
                result[1] = 0f;
            }
            else
            {
                result[0] = (p1Position.X > p2Position.X ? 1f : -1f);
                result[1] = (p1Position.Y > p2Position.Y ? 1f : -1f);
            }
        }

        result[2] = 0f;
        result[3] = 1f;
        return result;
    }
}
