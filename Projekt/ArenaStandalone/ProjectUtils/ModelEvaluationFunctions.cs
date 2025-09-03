using System;


//These are designed to take 2 models, run a game, collect necessary data and return their score
public class ModelEvaluationFunctions
{
    //Evaluated 2 models based on how good they are in not falling out of the arena
    //Staying near zones is rewarded, falling out of the arena is heavily punished
    public static List<float> ArenaFocusedExperiment(GamePlayerController player1, GamePlayerController player2)
    {
        List<float> results = new List<float> { 0f, 0f };

        foreach (int player1side in new int[2] { 1, 2 })
        {
            GameMain gameInstance = new GameMain();
            gameInstance.ChangeController(player1side, player1);
            gameInstance.ChangeController(3 - player1side, player2);
            gameInstance.StartGame();

            List<Pair> zonePositions = new List<Pair>();
            List<GameZone> GZ = new List<GameZone>();

            foreach (GameZone gz in gameInstance.activeZones)
            {
                zonePositions.Add(gz.position);
                GZ.Add(gz);
            }

            while (gameInstance.gameState == 0)
            {
                List<GameZone> toRemove = new List<GameZone>();

                foreach (GameZone gz in GZ)
                {
                    if (gz.isCaptured)
                    {
                        zonePositions.Remove(gz.position);
                        toRemove.Add(gz);
                    }
                }

                foreach (GameZone gz in toRemove)
                {
                    GZ.Remove(gz);
                }

                if (!gameInstance.player1.isDead)
                {
                    float D = zonePositions.Min(zonePos => (zonePos - gameInstance.player1.position).Magnitude()) - GameConfig.ZONE_RADIUS;

                    if (D < 0)
                    {
                        results[player1side - 1] += 1f;
                    }
                    else
                    {
                        results[player1side - 1] += 1f / (float)Math.Log(Math.E + D);
                    }
                }

                if (!gameInstance.player2.isDead)
                {
                    float D = zonePositions.Min(zonePos => (zonePos - gameInstance.player2.position).Magnitude()) - GameConfig.ZONE_RADIUS;

                    if (D < 0)
                    {
                        results[2 - player1side] += 1f;
                    }
                    else
                    {
                        results[2 - player1side] += 1f / (float)Math.Log(Math.E + D);
                    }
                }

                gameInstance.Update();
            }

            results[player1side - 1] -= 1f * gameInstance.gameTimeInTicks * gameInstance.player2kills;
            results[2 - player1side] -= 1f * gameInstance.gameTimeInTicks * gameInstance.player1kills;
        }

        return results;
    }

    public static List<float> BulletFocusedExperiment(GamePlayerController player1, GamePlayerController player2)
    {
        List<float> results = new List<float> { 0f, 0f };

        foreach (int player1side in new int[2] { 1, 2 })
        {
            GameMain gameInstance = new GameMain();
            gameInstance.ChangeController(player1side, player1);
            gameInstance.ChangeController(3 - player1side, player2);
            gameInstance.StartGame();

            List<Pair> zonePositions = new List<Pair>();
            List<GameZone> GZ = new List<GameZone>();

            foreach (GameZone gz in gameInstance.activeZones)
            {
                zonePositions.Add(gz.position);
                GZ.Add(gz);
            }

            while (gameInstance.gameState == 0)
            {
                List<GameZone> toRemove = new List<GameZone>();

                foreach (GameZone gz in GZ)
                {
                    if (gz.isCaptured)
                    {
                        zonePositions.Remove(gz.position);
                        toRemove.Add(gz);
                    }
                }

                foreach (GameZone gz in toRemove)
                {
                    GZ.Remove(gz);
                }

                foreach (GameBullet gb in gameInstance.activeBullets)
                {
                    if (!gameInstance.player1.isDead)
                    {
                        Pair toPlayer = gameInstance.player1.position - gb.position;
                        float distance = toPlayer.Magnitude();

                        Pair vBullet = gb.speed;
                        vBullet.Normalize(1);

                        Pair vToPlayer = gameInstance.player1.position - gb.position;
                        vToPlayer.Normalize(1);

                        float alignment = Pair.DotProduct(vBullet, vToPlayer);

                        if (distance < GameConfig.ZONE_RADIUS)
                        {
                            float score = alignment / (distance + 1);
                            results[2 - player1side] += score;
                        }
                    }

                    if (!gameInstance.player2.isDead)
                    {
                        Pair toPlayer = gameInstance.player2.position - gb.position;
                        float distance = toPlayer.Magnitude();

                        Pair vBullet = gb.speed;
                        vBullet.Normalize(1);

                        Pair vToPlayer = gameInstance.player2.position - gb.position;
                        vToPlayer.Normalize(1);

                        float alignment = Pair.DotProduct(vBullet, vToPlayer);

                        if (distance < GameConfig.ZONE_RADIUS)
                        {
                            float score = alignment / (distance + 1);
                            results[player1side - 1] += score;
                        }
                    }
                }

                gameInstance.Update();
            }

            results[player1side - 1] -= 1f * gameInstance.gameTimeInTicks * gameInstance.player2kills;
            results[2 - player1side] -= 1f * gameInstance.gameTimeInTicks * gameInstance.player1kills;
        }

        return results;
    }

    //Points calculation:

    //Each frame: (games last a maximum of 10800 frames)
    //  +1 point for being in an uncaptured zone, 1/log(dist) for being further away
    //  +1 point for having a captured zone
    // +[0-0.5] points for having progress in a zone
    // -50 points if the player is dead (9000 total for a death)

    //On special events:
    // On a bullet shot, the shooter gains +360*scalar_vector(0-1) if the vector is above 0, and loses 120*scalar_vector(-1 - 0) if the vector is below 0
    // If the game ends before a time limit (zone victory or kills), the winner player gets his remaining zone points as if he would play until the end
    // If the game was won by zones, +5000 bonus to the winner
    public static List<float> OverallExperiment(GamePlayerController player1, GamePlayerController player2)
    {
        List<float> results = new List<float> { 0f, 0f };

        foreach (int player1side in new int[2] { 1, 2 })
        {
            GameMain gameInstance = new GameMain();
            gameInstance.ChangeController(player1side, player1);
            gameInstance.ChangeController(3 - player1side, player2);
            gameInstance.StartGame();

            List<Pair> zonePositions = new List<Pair>();
            List<GameZone> GZ = new List<GameZone>();

            int currentBullets = 0;

            foreach (GameZone gz in gameInstance.activeZones)
            {
                zonePositions.Add(gz.position);
                GZ.Add(gz);
            }

            while (gameInstance.gameState == 0)
            {
                List<GameZone> toRemove = new List<GameZone>();

                foreach (GameZone gz in GZ)
                {
                    if (gz.isCaptured)
                    {
                        zonePositions.Remove(gz.position);
                        toRemove.Add(gz);
                    }
                }

                foreach (GameZone gz in toRemove)
                {
                    GZ.Remove(gz);
                }

                //point calculation
                //  +1 point for being in an uncaptured zone, 1/log(dist) for being further away
                if (!gameInstance.player1.isDead)
                {
                    float D = zonePositions.Min(zonePos => (zonePos - gameInstance.player1.position).Magnitude()) - GameConfig.ZONE_RADIUS;

                    if (D < 0)
                    {
                        results[player1side - 1] += 1f;
                    }
                    else
                    {
                        results[player1side - 1] += 1f / (float)Math.Log(Math.E + D);
                    }
                }

                if (!gameInstance.player2.isDead)
                {
                    float D = zonePositions.Min(zonePos => (zonePos - gameInstance.player2.position).Magnitude()) - GameConfig.ZONE_RADIUS;

                    if (D < 0)
                    {
                        results[2 - player1side] += 1f;
                    }
                    else
                    {
                        results[2 - player1side] += 1f / (float)Math.Log(Math.E + D);
                    }
                }

                //  +1 point for having a captured zone
                // +[0-0.5] points for having progress in a zone
                foreach (GameZone zoone in gameInstance.activeZones)
                {
                    if (zoone.isCaptured)
                    {
                        results[zoone.advantageousPlayer - 1] += 1f;
                    }
                    else if (zoone.advantageousPlayer != 3 && zoone.advantageousPlayer != 0)
                    {
                        results[zoone.advantageousPlayer - 1] += 0.5f * (float)zoone.advantageTicks / GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE;
                    }
                }

                // -50 points if the player is dead (9000 total for a death)  
                if (gameInstance.player1.isDead)
                {
                    results[player1side - 1] -= 50f;
                }

                if (gameInstance.player2.isDead)
                {
                    results[2 - player1side] -= 50f;
                }

                if (gameInstance.activeBullets.Count < currentBullets)
                {
                    currentBullets = gameInstance.activeBullets.Count;
                }

                // On a bullet shot, the shooter gains +360*scalar_vector(0-1) if the vector is above 0, and loses 120*scalar_vector(-1 - 0) if the vector is below 0
                while (gameInstance.activeBullets.Count > currentBullets)
                {
                    GameBullet newBullet = gameInstance.activeBullets[currentBullets];

                    Pair p1p = gameInstance.player1.position - newBullet.position;
                    Pair p2p = gameInstance.player2.position - newBullet.position;

                    float p1bulletDist = p1p.Magnitude();
                    float p2bulletDist = p2p.Magnitude();

                    float p1Likeliness = Math.Abs(p1bulletDist - 130f);
                    float p2Likeliness = Math.Abs(p2bulletDist - 130f);

                    int shooterIndex = (p1Likeliness <= p2Likeliness) ? player1side - 1 : 2 - player1side;
                    int otherIndex = 1 - shooterIndex;

                    //---
                    Pair toPlayer = shooterIndex == 0 ? gameInstance.player2.position - newBullet.position : gameInstance.player1.position - newBullet.position;
                    float distance = toPlayer.Magnitude();

                    Pair vBullet = newBullet.speed;
                    vBullet.Normalize(1);

                    Pair vToPlayer = shooterIndex == 0 ? gameInstance.player2.position - newBullet.position : gameInstance.player1.position - newBullet.position;
                    vToPlayer.Normalize(1);

                    float alignment = Pair.DotProduct(vBullet, vToPlayer);

                    results[shooterIndex] += (alignment > 0) ? 360f * alignment : 120f * alignment;

                    currentBullets++;
                }

                gameInstance.Update();
            }

            int winner = gameInstance.gameState;

            // If the game ends before a time limit (zone victory or kills), the winner player gets his remaining zone points as if he would play until the end
            if (winner != 3 && gameInstance.gameTimeInTicks < GameConfig.MAX_GAME_TIME_IN_TICKS)
            {
                float gainPerTick = 0f;

                foreach (GameZone zoone in gameInstance.activeZones)
                {
                    if (zoone.advantageousPlayer == winner)
                    {
                        if (zoone.isCaptured)
                        {
                            gainPerTick += 1f;
                        }
                        else if (zoone.advantageousPlayer != 3)
                        {
                            gainPerTick += 0.5f * (float)zoone.advantageTicks / GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE;
                        }
                    }
                }

                results[winner - 1] += gainPerTick * (GameConfig.MAX_GAME_TIME_IN_TICKS - gameInstance.gameTimeInTicks);
            }

            int p1zones = 0;
            int p2zones = 0;

            // If the game was won by zones, +5000 bonus to the winner
            foreach (GameZone zoone in gameInstance.activeZones)
            {
                if (zoone.isCaptured)
                {
                    if (zoone.advantageousPlayer == 1)
                    {
                        p1zones++;
                    }
                    else
                    {
                        p2zones++;
                    }
                }
            }

            if (p1zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY || p2zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY)
            {
                results[winner - 1] += 5000f;
            }
        }

        return results;
    }

    //Very similar to the previously defined method, but has a few differences:
    //Distance points are only awarded to the player, who is closer to the closest uncaptured zone now, the other player loses an equivalent amount (encourages the other player to actually fight for the zones)
    //It matter how close the player is to the middle of the zone, it's no longer the same amount of points for just existing there
    //Points assigned for zone victory scale down with time linearly from +5000 to 0, the losing player loses points as well (encourages both the winners to win games as well as the losers to fight for a longer time)
    public static List<float> ModifiedOverallExperiment(GamePlayerController player1, GamePlayerController player2)
    {
        List<float> results = new List<float> { 0f, 0f };

        foreach (int player1side in new int[2] { 1, 2 })
        {
            GameMain gameInstance = new GameMain();
            gameInstance.ChangeController(player1side, player1);
            gameInstance.ChangeController(3 - player1side, player2);
            gameInstance.StartGame();

            List<Pair> zonePositions = new List<Pair>();
            List<GameZone> GZ = new List<GameZone>();

            int currentBullets = 0;

            foreach (GameZone gz in gameInstance.activeZones)
            {
                zonePositions.Add(gz.position);
                GZ.Add(gz);
            }

            while (gameInstance.gameState == 0)
            {
                List<GameZone> toRemove = new List<GameZone>();

                foreach (GameZone gz in GZ)
                {
                    if (gz.isCaptured)
                    {
                        zonePositions.Remove(gz.position);
                        toRemove.Add(gz);
                    }
                }

                foreach (GameZone gz in toRemove)
                {
                    GZ.Remove(gz);
                }

                double D1 = -1.0;
                double D2 = -1.0;

                if (!gameInstance.player1.isDead)
                {
                    D1 = zonePositions.Min(zonePos => (zonePos - gameInstance.player1.position).Magnitude());
                }

                if (!gameInstance.player2.isDead)
                {
                    D2 = zonePositions.Min(zonePos => (zonePos - gameInstance.player2.position).Magnitude());
                }

                if (D1 == D2) //captures the case D1 == D2 == -1.0 (both players dead)
                {
                    if (D1 != -1.0)
                    {
                        results[player1side - 1] += 1f;
                        results[2 - player1side] += 1f;
                    }
                }
                else if (D1 == -1.0 && D2 != -1.0)
                {
                    results[2 - player1side] += 1f / (float)Math.Log(Math.E + D2);
                    results[player1side - 1] -= 1f / (float)Math.Log(Math.E + D2);
                }
                else if (D2 == -1.0 && D1 != -1.0)
                {
                    results[player1side - 1] += 1f / (float)Math.Log(Math.E + D1);
                    results[2 - player1side] -= 1f / (float)Math.Log(Math.E + D1);
                }
                else
                {
                    double Ddiff = Math.Abs(D1 - D2);

                    if (D1 > D2)
                    {
                        results[2 - player1side] += 1f / (float)Math.Log(Math.E + (2 * GameConfig.ARENA_RADIUS - Ddiff));
                        results[player1side - 1] -= 1f / (float)Math.Log(Math.E + (2 * GameConfig.ARENA_RADIUS - Ddiff));
                    }
                    else
                    {
                        results[player1side - 1] += 1f / (float)Math.Log(Math.E + (2 * GameConfig.ARENA_RADIUS - Ddiff));
                        results[2 - player1side] -= 1f / (float)Math.Log(Math.E + (2 * GameConfig.ARENA_RADIUS - Ddiff));
                    }
                }

                //  +1 point for having a captured zone
                // +[0-0.5] points for having progress in a zone
                foreach (GameZone zoone in gameInstance.activeZones)
                {
                    if (zoone.isCaptured)
                    {
                        results[zoone.advantageousPlayer - 1] += 1f;
                    }
                    else if (zoone.advantageousPlayer != 3 && zoone.advantageousPlayer != 0)
                    {
                        results[zoone.advantageousPlayer - 1] += 0.5f * (float)zoone.advantageTicks / GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE;
                    }
                }

                // -50 points if the player is dead (9000 total for a death)  
                if (gameInstance.player1.isDead)
                {
                    results[player1side - 1] -= 50f;
                }

                if (gameInstance.player2.isDead)
                {
                    results[2 - player1side] -= 50f;
                }

                if (gameInstance.activeBullets.Count < currentBullets)
                {
                    currentBullets = gameInstance.activeBullets.Count;
                }

                // On a bullet shot, the shooter gains +360*scalar_vector(0-1) if the vector is above 0, and loses 120*scalar_vector(-1 - 0) if the vector is below 0
                while (gameInstance.activeBullets.Count > currentBullets)
                {
                    GameBullet newBullet = gameInstance.activeBullets[currentBullets];

                    Pair p1p = gameInstance.player1.position - newBullet.position;
                    Pair p2p = gameInstance.player2.position - newBullet.position;

                    float p1bulletDist = p1p.Magnitude();
                    float p2bulletDist = p2p.Magnitude();

                    float p1Likeliness = Math.Abs(p1bulletDist - 130f);
                    float p2Likeliness = Math.Abs(p2bulletDist - 130f);

                    int shooterIndex = (p1Likeliness <= p2Likeliness) ? player1side - 1 : 2 - player1side;
                    int otherIndex = 1 - shooterIndex;

                    //---
                    Pair toPlayer = shooterIndex == 0 ? gameInstance.player2.position - newBullet.position : gameInstance.player1.position - newBullet.position;
                    float distance = toPlayer.Magnitude();

                    Pair vBullet = newBullet.speed;
                    vBullet.Normalize(1);

                    Pair vToPlayer = shooterIndex == 0 ? gameInstance.player2.position - newBullet.position : gameInstance.player1.position - newBullet.position;
                    vToPlayer.Normalize(1);

                    float alignment = Pair.DotProduct(vBullet, vToPlayer);

                    results[shooterIndex] += (alignment > 0) ? 360f * alignment : 120f * alignment;

                    currentBullets++;
                }

                gameInstance.Update();
            }

            int winner = gameInstance.gameState;

            // If the game ends before a time limit (zone victory or kills), the winner player gets his remaining zone points as if he would play until the end
            if (winner != 3 && gameInstance.gameTimeInTicks < GameConfig.MAX_GAME_TIME_IN_TICKS)
            {
                float gainPerTick = 0f;

                foreach (GameZone zoone in gameInstance.activeZones)
                {
                    if (zoone.advantageousPlayer == winner)
                    {
                        if (zoone.isCaptured)
                        {
                            gainPerTick += 1f;
                        }
                        else if (zoone.advantageousPlayer != 3)
                        {
                            gainPerTick += 0.5f * (float)zoone.advantageTicks / GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE;
                        }
                    }
                }

                results[winner - 1] += gainPerTick * (GameConfig.MAX_GAME_TIME_IN_TICKS - gameInstance.gameTimeInTicks);
            }

            int p1zones = 0;
            int p2zones = 0;

            // If the game was won by zones, +5000 bonus to the winner
            foreach (GameZone zoone in gameInstance.activeZones)
            {
                if (zoone.isCaptured)
                {
                    if (zoone.advantageousPlayer == 1)
                    {
                        p1zones++;
                    }
                    else
                    {
                        p2zones++;
                    }
                }
            }

            if (p1zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY || p2zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY)
            {
                results[winner - 1] += 5000f * (1f - ((float)gameInstance.gameTimeInTicks / (float)GameConfig.MAX_GAME_TIME_IN_TICKS));
                results[2 - winner] -= 5000f * (1f - ((float)gameInstance.gameTimeInTicks / (float)GameConfig.MAX_GAME_TIME_IN_TICKS));
            }
        }

        return results;
    }
}