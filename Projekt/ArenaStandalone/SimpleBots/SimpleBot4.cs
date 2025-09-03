using System.Collections;
using System.Collections.Generic;

public class SimpleBot4 : GamePlayerController
{
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        List<float> result = new List<float>(new float[4]);

        Pair myPos = (whoAmI == 1) ? gameInstance.player1.position : gameInstance.player2.position;
        Pair enemyPos = (whoAmI == 1) ? gameInstance.player2.position : gameInstance.player1.position;
        bool enemyDead = (whoAmI == 1) ? gameInstance.player2.isDead : gameInstance.player1.isDead;
        float myEnergy = (whoAmI == 1) ? gameInstance.player1.energy : gameInstance.player2.energy;

        float distanceToEnemy = (myPos - enemyPos).Magnitude();

        // Default: move toward enemy
        float moveX = (myPos.X < enemyPos.X ? 1f : -1f);
        float moveY = (myPos.Y < enemyPos.Y ? 1f : -1f);

        bool zoneAvailable = false;
        GameZone targetZone = null;

        foreach (GameZone gz in gameInstance.activeZones)
        {
            if (!gz.isCaptured)
            {
                targetZone = gz;
                zoneAvailable = true;
                break;
            }
        }

        // Decision logic
        if (enemyDead)
        {
            // If enemy is dead, go to nearest uncaptured zone
            if (zoneAvailable)
            {
                moveX = (targetZone.position.X > myPos.X ? 1f : -1f);
                moveY = (targetZone.position.Y > myPos.Y ? 1f : -1f);
                result[2] = 0f;
                result[3] = 1f; // capture mode
            }
            else
            {
                moveX = moveY = 0f;
                result[2] = 0f;
                result[3] = 0f;
            }
        }
        else if (distanceToEnemy < 300f && myEnergy >= GameConfig.SHOOTING_ENERGY_COST)
        {
            // In range and can shoot: aggressive
            Pair shootDir = enemyPos - myPos;
            result[0] = shootDir.X;
            result[1] = shootDir.Y;
            result[2] = 1f; // dash if close
            result[3] = 1f; // shoot
            return result;
        }
        else if (zoneAvailable && distanceToEnemy >= 300f)
        {
            // Safe to capture zone
            moveX = (targetZone.position.X > myPos.X ? 1f : -1f);
            moveY = (targetZone.position.Y > myPos.Y ? 1f : -1f);
            result[2] = 0f;
            result[3] = 1f;
        }
        else
        {
            // Default behavior: close gap
            result[2] = (distanceToEnemy < 200f) ? 1f : 0f;
            result[3] = 0f;
        }

        result[0] = moveX;
        result[1] = moveY;
        return result;
    }

}
