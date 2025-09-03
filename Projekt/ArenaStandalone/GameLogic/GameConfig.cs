using System.Collections.Generic;

public class GameConfig
{
    //Contains all parameters that define how the game works
    //Some assumed parameters:
    /*
        - Final playable game version runs at 60 ticks per second
        - Arena center is located at (0,0)
    */


    //PLAYER
    public const float PLAYER_RADIUS = 50f;
    public const float MAX_PLAYER_SPEED = 10f;
    public const float MAX_PLAYER_ENERGY = 3f;
    public const float PLAYER_ENERGY_GAIN_PER_TICK = 1f/180f;
    public const float PLAYER_ACCELERATION = 0.25f;
    public const float PLAYER_COLLISION_FORCE = 1f;
    public static readonly List<Pair> PLAYER_SPAWNPOINTS = new List<Pair>
    {
        new Pair(0, -800),
        new Pair(0, 800)
    };
    public const int PLAYER_RESPAWN_TIME_IN_TICKS = 180;
    public const int PLAYER_INVULNERABILITY_FRAMES = 90; //only immune to bullets


    public const float PLAYER_COLLISION_MINIMAL_ENERGY_TRANSFER = 0f;

    //BOOST
    public const float MAX_BOOSTED_PLAYER_SPEED = 15f;
    public const float BOOSTED_PLAYER_ACCELERATION = 0.5f;
    public const float BOOST_ENERGY_COST_PER_TICK = 1f/60f;
    public const float MINIMAL_ENERGY_TO_START_BOOST = 1f;

    //ARENA
    public const float ARENA_RADIUS = 1000f;

    //ZONES
    public const int ZONE_AMOUNT = 3;
    public static readonly List<Pair> ZONE_POSITIONS = new List<Pair>
    {
        new Pair(-750, 0),
        new Pair(0, 0),
        new Pair(750, 0)
    };
    public const float ZONE_RADIUS = 200f;
    public const int ZONE_TICKS_NEEDED_FOR_CAPTURE = 600; 

    //BULLETS AND SHOOTING
    public const float SHOOTING_ENERGY_COST = 2f;
    public const float BULLET_RADIUS = 25f;
    public const float MAX_BULLET_SPEED = 30f;
    public const float BULLET_COLLISION_FORCE = 0.65f;

    //WIN CONDITIONS
    public const int ZONES_NEEDED_FOR_VICTORY = 2;
    public const int KILLS_NEEDED_FOR_VICTORY = 3;
    public const int MAX_GAME_TIME_IN_TICKS = 10800;
}

