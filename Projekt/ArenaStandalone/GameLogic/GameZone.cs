using System;

public class GameZone
{
    public int ID { get; private set; }
    public Pair position { get; private set; }
    public int currentConquerrors { get; private set; } //Who is currently in this zones area? 0 - no players, 1 - only player1, 2 - only player2, 3 - both players
    
    public int advantageousPlayer { get; private set; } //Who has the advantage in this zone
    public int advantageTicks { get; private set; }

    public bool isCaptured { get; private set; }

    public GameZone(int myID, Pair startingPosition)
    {
        ID = myID;
        position = startingPosition;
        StartZone();
    }

    public void StartZone()
    {
        currentConquerrors = 0;
        advantageousPlayer = 0;
        advantageTicks = 0;
        isCaptured = false;
    }

    public void CheckPlayersInZone(GamePlayer player1, GamePlayer player2)
    {
        currentConquerrors = 0;

        if(GameUtility.DoCirclesOverlap(player1.position, GameConfig.PLAYER_RADIUS, position, GameConfig.ZONE_RADIUS) && !player1.isDead)
        {
            currentConquerrors += 1;
        }

        if(GameUtility.DoCirclesOverlap(player2.position, GameConfig.PLAYER_RADIUS, position, GameConfig.ZONE_RADIUS) && !player2.isDead)
        {
            currentConquerrors += 2;
        }
    }

    public void Update()
    {
        if(!isCaptured && currentConquerrors != 0 && currentConquerrors != 3)
        {
            if(advantageTicks == 0)
            {
                advantageousPlayer = currentConquerrors;
                advantageTicks = 1;
            }
            else if(advantageousPlayer == currentConquerrors)
            {
                advantageTicks++;
            }
            else
            {
                advantageTicks--;
            }

            if(advantageTicks == 0)
            {
                advantageousPlayer = 0;
            }

            if(advantageTicks == GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE)
            {
                isCaptured = true;
            }
        }
    }

}
