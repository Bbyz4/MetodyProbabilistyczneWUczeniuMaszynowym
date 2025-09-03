using System.Collections;
using System.Collections.Generic;

public class SimpleBot2 : GamePlayerController
{
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        Pair p1Position = gameInstance.player1.position;
        Pair p2Position = gameInstance.player2.position;

        float playerDistance = (p1Position - p2Position).Magnitude();

        if (whoAmI == 1)
        {
            float otherDistFromMiddle = p2Position.Magnitude();

            if (otherDistFromMiddle > 500f) //play agressively
            {
                result[0] = (p1Position.X < p2Position.X ? 1f : -1f);
                result[1] = (p1Position.Y < p2Position.Y ? 1f : -1f);

                result[2] = (playerDistance < 200f ? 1f : 0f);
                result[3] = 0f;
            }
            else //capture zones
            {
                GameZone zone = null;
                foreach (GameZone gz in gameInstance.activeZones)
                {
                    if (!gz.isCaptured)
                    {
                        zone = gz;
                        break;
                    }
                }

                result[0] = (zone.position.X > p1Position.X ? 1f : -1f);
                result[1] = (zone.position.Y > p1Position.Y ? 1f : -1f);

                result[2] = 0f;
                result[3] = 1f;
            }   
        }
        else
        {
            float otherDistFromMiddle = p1Position.Magnitude();

            if (otherDistFromMiddle > 500f) //play agressively
            {
                result[0] = (p1Position.X > p2Position.X ? 1f : -1f);
                result[1] = (p1Position.Y > p2Position.Y ? 1f : -1f);

                result[2] = (playerDistance < 100f ? 1f : 0f);
                result[3] = 0f;
            }
            else //capture zones
            {
                GameZone zone = null;
                foreach (GameZone gz in gameInstance.activeZones)
                {
                    if (!gz.isCaptured)
                    {
                        zone = gz;
                        break;
                    }
                }

                result[0] = (zone.position.X > p2Position.X ? 1f : -1f);
                result[1] = (zone.position.Y > p2Position.Y ? 1f : -1f);

                result[2] = 0f;
                result[3] = 1f;
            }   
        }
        return result;
    }
}
