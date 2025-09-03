using System;
using System.Collections.Generic;

public class GameMain
{
    public GamePlayer player1 { get; private set; }
    public GamePlayer player2 { get; private set; }

    private GamePlayerController player1Controller;
    private GamePlayerController player2Controller;

    public List<GameZone> activeZones { get; private set; }
    public List<GameBullet> activeBullets { get; private set; } 

    //game data
    public int gameState { get; private set; } // 0 - running, 1 - player1 won, 2 - player2 won, 3 - draw
    public int gameTimeInTicks { get; private set; }

    //stats
    public int player1kills { get; private set; }
    public int player2kills { get; private set; }

    public bool playersAreColliding { get; private set; }

    public void ChangeController(int playerNumber, GamePlayerController newController)
    {
        if (playerNumber == 1)
        {
            player1Controller = newController;
        }
        if (playerNumber == 2)
        {
            player2Controller = newController;
        }
    }

    public void StartGame()
    {
        player1 = new GamePlayer(1);
        player2 = new GamePlayer(2);



        activeZones = new List<GameZone>();

        for(int i=0; i<GameConfig.ZONE_AMOUNT; i++)
        {
            GameZone gz = new GameZone(i+1, GameConfig.ZONE_POSITIONS[i]);
            activeZones.Add(gz);
        }

        activeBullets = new List<GameBullet>();

        gameState = 0;
        gameTimeInTicks = 0;
        playersAreColliding = false;

        ResetStats();
    }

    private void ResetStats()
    {
        player1kills = 0;
        player2kills = 0;
    }

    //main game loop
    public void Update()
    {
        if (gameState != 0)
        {
            return;
        }

        //update game time
        gameTimeInTicks++;

        //update hardcoded player information
        player1.isOtherPlayerOnUpperHalf = (player2.position.Y > 0);
        player2.isOtherPlayerOnUpperHalf = (player1.position.Y > 0);

        //get input data and handle
        List<float> player1Input = player1Controller.GetInputValues(this, 1);
        List<float> player2Input = player2Controller.GetInputValues(this, 2);

        player1.ReceiveInput(player1Input);
        player2.ReceiveInput(player2Input);

        //update zone coverages
        foreach(GameZone gz in activeZones)
        {
            gz.CheckPlayersInZone(player1, player2);
        }

        //check if the players fell outside of the arena
        if(!GameUtility.DoCirclesOverlap(player1.position, GameConfig.PLAYER_RADIUS, new Pair(0,0), GameConfig.ARENA_RADIUS) && !player1.isDead)
        {
            player1.Die();
            player2kills++;
        }

        if(!GameUtility.DoCirclesOverlap(player2.position, GameConfig.PLAYER_RADIUS, new Pair(0,0), GameConfig.ARENA_RADIUS) && !player2.isDead)
        {
            player2.Die();
            player1kills++;
        }

        //check if players collide with each other and resolve the collision if they do
        bool collisionDetected = !player1.isDead && !player2.isDead && GameUtility.DoCirclesOverlap(player1.position, GameConfig.PLAYER_RADIUS, player2.position, GameConfig.PLAYER_RADIUS);

        if (collisionDetected && !playersAreColliding)
        {
            playersAreColliding = true;
            while (GameUtility.DoCirclesOverlap(player1.position, GameConfig.PLAYER_RADIUS, player2.position, GameConfig.PLAYER_RADIUS))
            {
                if (player1.speed.X == 0 && player1.speed.Y == 0 && player2.speed.X == 0 && player2.speed.Y == 0)
                {
                    Pair resolveDir = player2.position - player1.position;
                    player1.speed = resolveDir;
                    player2.speed = new Pair(0f, 0f) - resolveDir;
                }
                else
                {
                    player1.position.X -= player1.speed.X * 0.1f;
                    player1.position.Y -= player1.speed.Y * 0.1f;
                    player2.position.X -= player2.speed.X * 0.1f;
                    player2.position.Y -= player2.speed.Y * 0.1f;
                }
            }

            Pair impactDir = player2.position - player1.position;
            impactDir.Normalize(1);
            Pair impactDirReversed = new Pair(-impactDir.X, -impactDir.Y);

            Pair p1velocity = player1.speed;
            float p1energy = p1velocity.Magnitude();
            p1velocity.Normalize(1);

            Pair p2velocity = player2.speed;
            float p2energy = p2velocity.Magnitude();
            p2velocity.Normalize(1);

            float p1energyTransfer = Pair.DotProduct(p1velocity, impactDir) * p1energy * GameConfig.PLAYER_COLLISION_FORCE;
            if (Math.Abs(p1energyTransfer) < GameConfig.PLAYER_COLLISION_MINIMAL_ENERGY_TRANSFER)
            {
                p1energyTransfer = GameConfig.PLAYER_COLLISION_MINIMAL_ENERGY_TRANSFER * Math.Sign(p1energyTransfer);
            }

            impactDir.Normalize(p1energyTransfer);
            player1.speed -= impactDir;
            player2.speed += impactDir;

            float p2energyTransfer = Pair.DotProduct(p2velocity, impactDirReversed) * p2energy * GameConfig.PLAYER_COLLISION_FORCE;
            if (Math.Abs(p2energyTransfer) < GameConfig.PLAYER_COLLISION_MINIMAL_ENERGY_TRANSFER)
            {
                p2energyTransfer = GameConfig.PLAYER_COLLISION_MINIMAL_ENERGY_TRANSFER * Math.Sign(p2energyTransfer);
            }

            impactDirReversed.Normalize(p2energyTransfer);
            player1.speed += impactDirReversed;
            player2.speed -= impactDirReversed;
        }
        else if (collisionDetected && playersAreColliding)
        {
            //keep the minimal distance between the players
            Pair playerDirVector = player2.position - player1.position;
            float playerDistance = playerDirVector.Magnitude() - (2 * GameConfig.PLAYER_RADIUS + 0.1f);

            if (playerDistance < 0)
            {
                playerDirVector.Normalize(-0.5f * playerDistance);
                player2.position += playerDirVector;
                player1.position -= playerDirVector;
            }
        }
        else if (!collisionDetected)
        {
            playersAreColliding = false;
        }

        //call Update on all present game objects + collect some data

        int player1zones = 0;
        int player2zones = 0;

        player1.Update();
        player2.Update();

        //check if the players want to shoot
        if (player1.willingToShoot && !player1.isDead)
        {
            player1.willingToShoot = false;

            player1.energy -= GameConfig.SHOOTING_ENERGY_COST;

            Pair player1lookDirection = player1.desiredSpeed; //TO DISCUSS: should this be speed or desired speed
            player1lookDirection.Normalize(GameConfig.PLAYER_RADIUS + (2 * GameConfig.BULLET_RADIUS));

            Pair bulletStartPosition = player1.position + player1lookDirection;

            player1lookDirection.Normalize(GameConfig.MAX_BULLET_SPEED);

            Pair bulletStartSpeed = player1lookDirection;

            GameBullet newBullet = new GameBullet(0);
            newBullet.SetParams(bulletStartPosition, bulletStartSpeed);

            activeBullets.Add(newBullet);
        }
        
        if (player2.willingToShoot && !player2.isDead)
        {
            player2.willingToShoot = false;

            player2.energy -= GameConfig.SHOOTING_ENERGY_COST;

            Pair player2lookDirection = player2.desiredSpeed; //TO DISCUSS: should this be speed or desired speed
            player2lookDirection.Normalize(GameConfig.PLAYER_RADIUS + (2 * GameConfig.BULLET_RADIUS));

            Pair bulletStartPosition = player2.position + player2lookDirection;

            player2lookDirection.Normalize(GameConfig.MAX_BULLET_SPEED);

            Pair bulletStartSpeed = player2lookDirection;

            GameBullet newBullet = new GameBullet(0);
            newBullet.SetParams(bulletStartPosition, bulletStartSpeed);

            activeBullets.Add(newBullet);
        }

        foreach (GameZone gz in activeZones)
        {
            gz.Update();

            if (gz.isCaptured)
            {
                if (gz.advantageousPlayer == 1)
                {
                    player1zones++;
                }
                else
                {
                    player2zones++;
                }
            }
        }

        foreach(GameBullet gb in activeBullets)
        {
            gb.Update();
        }

        //check if any bullets collided with a player
        foreach (GameBullet gb in activeBullets)
        {
            //player 1
            if (!player1.isDead && !player1.IsImmuneToBullets() && GameUtility.DoCirclesOverlap(gb.position, GameConfig.BULLET_RADIUS, player1.position, GameConfig.BULLET_RADIUS))
            {
                gb.hadCollided = true;

                Pair impactDir = gb.speed;
                impactDir.Normalize(1);

                float energyTransfer = GameConfig.MAX_BULLET_SPEED * GameConfig.BULLET_COLLISION_FORCE;
                impactDir.Normalize(energyTransfer);
                player1.speed = impactDir;
            }

            //player 2
            if (!player2.isDead && !player2.IsImmuneToBullets() && GameUtility.DoCirclesOverlap(gb.position, GameConfig.BULLET_RADIUS, player2.position, GameConfig.BULLET_RADIUS))
            {
                gb.hadCollided = true;

                Pair impactDir = gb.speed;
                impactDir.Normalize(1);

                float energyTransfer = GameConfig.MAX_BULLET_SPEED * GameConfig.BULLET_COLLISION_FORCE; //TO DISCUSS: should bullets be that deadly
                impactDir.Normalize(energyTransfer);
                player2.speed = impactDir;
            }
        }      

        //remove used bullets
        for (int i = activeBullets.Count - 1; i >= 0; i--)
        {
            if (activeBullets[i].hadCollided || !GameUtility.DoCirclesOverlap(activeBullets[i].position, GameConfig.BULLET_RADIUS, new Pair(0, 0), GameConfig.ARENA_RADIUS))
            {
                activeBullets.RemoveAt(i);
            }
        }

        //check if the game should end already

        bool player1won = player1zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY || player1kills >= GameConfig.KILLS_NEEDED_FOR_VICTORY;
        bool player2won = player2zones >= GameConfig.ZONES_NEEDED_FOR_VICTORY || player2kills >= GameConfig.KILLS_NEEDED_FOR_VICTORY;

        if(player1won && player2won) //rare case, but could happen
        {
            gameState = 3; //draw
        }
        else if(player1won)
        {
            gameState = 1;
        }
        else if(player2won)
        {
            gameState = 2;
        }
        else if(gameTimeInTicks >= GameConfig.MAX_GAME_TIME_IN_TICKS)
        {
            gameState = 3;
        }
    }
}
