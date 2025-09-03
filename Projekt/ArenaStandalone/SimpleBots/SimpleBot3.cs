using System.Collections;
using System.Collections.Generic;

public class SimpleBot3 : GamePlayerController
{
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        Pair p1Position = gameInstance.player1.position;
        Pair p2Position = gameInstance.player2.position;

        if (whoAmI == 1)
        {
            if (gameInstance.player1.energy >= GameConfig.SHOOTING_ENERGY_COST)
            {
                Pair shootDir = p2Position - p1Position;

                result[0] = shootDir.X;
                result[1] = shootDir.Y;

                result[3] = 1f;
            }
            else
            {
                result[0] = p1Position.X < 0f ? 1f : -1f;
                result[1] = p1Position.Y < 0f ? 1f : -1f;

                result[3] = 0f;
            }
        }
        else
        {
            if (gameInstance.player2.energy >= GameConfig.SHOOTING_ENERGY_COST)
            {
                Pair shootDir = p1Position - p2Position;

                result[0] = shootDir.X;
                result[1] = shootDir.Y;

                result[3] = 1f;
            }
            else
            {
                result[0] = p2Position.X < 0f ? 1f : -1f;
                result[1] = p2Position.Y < 0f ? 1f : -1f;

                result[3] = 0f;
            }
        }

        result[2] = 0f;
        return result;
    }
}
