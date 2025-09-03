using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using MathNet.Numerics.LinearAlgebra;

public class NNBot : GamePlayerController
{
    public NeuralModel Brain;
    public NNBot(Genome genome)
    {
        Brain = new NeuralModel(genome);
    }
    public List<float> GetInputValues(GameMain gameInstance, int whoAmI)
    {
        int myID = whoAmI - 1;
        Vector<float> game_state = Vector<float>.Build.Dense(AlgorithmConfig.input_size);
        Vector<float>[] player_data = new Vector<float>[2];

        //playerData
        //input should also be scaled to [0,1] !!
        foreach (int i in new int[] { 0, 1 })
        {
            player_data[i] = Vector<float>.Build.Dense(20);
            var player = (i == 0)
            ? gameInstance.player1 : gameInstance.player2;
            //position
            player_data[i][0] = !player.isDead ? (player.position.X + GameConfig.ARENA_RADIUS) / (2 * GameConfig.ARENA_RADIUS) : 0f;
            player_data[i][1] = !player.isDead ? (player.position.Y + GameConfig.ARENA_RADIUS) / (2 * GameConfig.ARENA_RADIUS) : 0f;

            //speed
            player_data[i][2] = !player.isDead ? (player.speed.X) / GameConfig.MAX_BOOSTED_PLAYER_SPEED : 0f;
            player_data[i][3] = !player.isDead ? (player.speed.Y) / GameConfig.MAX_BOOSTED_PLAYER_SPEED : 0f;

            //misc
            player_data[i][4] = player.isDead ? 1f : 0f;
            player_data[i][5] = !player.isDead ? (player.energy) / GameConfig.MAX_PLAYER_ENERGY : 0f;
            player_data[i][6] = player.isBoosted ? 1f : 0f;
            player_data[i][7] = (1f * player.currentInvulnerabilityFrame) / GameConfig.PLAYER_INVULNERABILITY_FRAMES;
        }
        for (int i = 0; i < 7; i++)
        {
            game_state[i] = player_data[myID][i];
            game_state[i + 8] = player_data[myID ^ 1][i];
        }


        //zoneData (assuming there are always 3 zones in known positions)

        int p1zoneCounter = 0;
        int p2zoneCounter = 0;

        for (int i = 0; i < GameConfig.ZONE_AMOUNT; i++)
        {
            game_state[2 * i + 16] = gameInstance.activeZones[i].isCaptured ? 1f : 0f;

            if (gameInstance.activeZones[i].isCaptured)
            {
                if (gameInstance.activeZones[i].advantageousPlayer == 1)
                {
                    p1zoneCounter++;
                }
                else
                {
                    p2zoneCounter++;
                }
            }

            float zoneAdvantage = (0.5f * gameInstance.activeZones[i].advantageTicks) / (GameConfig.ZONE_TICKS_NEEDED_FOR_CAPTURE); // [0, 0.5]
            float zoneState = 0.5f;

            if (gameInstance.activeZones[i].advantageousPlayer == whoAmI)
            {
                zoneState += zoneAdvantage;
            }
            else
            {
                zoneState -= zoneAdvantage;
            }

            game_state[2 * i + 17] = zoneState; //1 - jest nasze, 0 - jest przeciwnika, wszystko pomiedzy to wiadomo
        }

        //bulletData (assuming that the maximum possible amount of bullets existing at once is 4 (which is true with our game settings))
        for (int i = 0; i < 2; i++)
        {
            bool bulletExists = gameInstance.activeBullets.Count > i;
            GameBullet bullet = null;
            if (bulletExists)
            {
                bullet = gameInstance.activeBullets[i];
            }

            game_state[5 * i + 22] = bulletExists ? 1f : 0f;
            game_state[5 * i + 23] = bulletExists ? (bullet.position.X + GameConfig.ARENA_RADIUS) / (2 * GameConfig.ARENA_RADIUS) : 0f;
            game_state[5 * i + 24] = bulletExists ? (bullet.position.Y + GameConfig.ARENA_RADIUS) / (2 * GameConfig.ARENA_RADIUS) : 0f;
            game_state[5 * i + 25] = bulletExists ? (bullet.speed.X) / GameConfig.MAX_BULLET_SPEED : 0f;
            game_state[5 * i + 26] = bulletExists ? (bullet.speed.Y) / GameConfig.MAX_BULLET_SPEED : 0f;
        }

        //score data (some info might be redundant but that is ok)
        game_state[32] = 1f * gameInstance.gameTimeInTicks / GameConfig.MAX_GAME_TIME_IN_TICKS;
        game_state[33] = 1f * (whoAmI == 1 ? gameInstance.player1kills : gameInstance.player2kills) / GameConfig.KILLS_NEEDED_FOR_VICTORY;
        game_state[34] = 1f * (whoAmI == 1 ? gameInstance.player2kills : gameInstance.player1kills) / GameConfig.KILLS_NEEDED_FOR_VICTORY;
        game_state[35] = 1f * (whoAmI == 1 ? p1zoneCounter : p2zoneCounter) / GameConfig.ZONES_NEEDED_FOR_VICTORY;
        game_state[36] = 1f * (whoAmI == 1 ? p2zoneCounter : p1zoneCounter) / GameConfig.ZONES_NEEDED_FOR_VICTORY;

        //Console.WriteLine(string.Join("| ", game_state));

        var output = Brain.Forward(game_state).ToList();
        //Debug.Log(string.Join(", ", output));
        foreach (int i in new int[]{0, 1}) {
            output[i] = 2 * (output[i] - 0.5f);
        }
        foreach (int i in new int[] { 2, 3 })
        {
            if (output[i] >= 0.5f) output[i] = 1;
            else output[i] = 0;
        }
        return output;
    }
}
