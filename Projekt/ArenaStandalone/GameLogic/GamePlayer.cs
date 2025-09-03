using System;
using System.Collections.Generic;

public class GamePlayer
{
    public int ID { get; private set; }
    public Pair position;
    public Pair speed;
    public Pair desiredSpeed;

    private List<float> receivedInput;

    public bool isBoosted { get; private set;  }
    public bool isDead { get; private set; }
    public int deathTickCounter { get; private set; }

    public float energy;

    public bool willingToShoot;

    public bool isOtherPlayerOnUpperHalf; //yeeeea...

    public int currentInvulnerabilityFrame;

    public GamePlayer(int myID)
    {
        ID = myID;
        isOtherPlayerOnUpperHalf = (ID == 1);
        receivedInput = new List<float>();
        Respawn();
    }

    public void Respawn()
    {
        isBoosted = false;
        isDead = false;
        energy = 0f;
        position = GameConfig.PLAYER_SPAWNPOINTS[isOtherPlayerOnUpperHalf ? 0 : 1];
        speed = new Pair(0, 0);
        desiredSpeed = new Pair(0, 0);
        willingToShoot = false;
        currentInvulnerabilityFrame = GameConfig.PLAYER_INVULNERABILITY_FRAMES;
    }

    public bool IsImmuneToBullets()
    {
        return (currentInvulnerabilityFrame > 0);
    }

    public void Die()
    {
        isDead = true;

        //just not to disturb any gameplay
        position.X = ID == 1 ? -0.01f : 0.01f;
        position.Y = ID == 1 ? -0.01f : 0.01f;

        deathTickCounter = -1;
    }

    public void ReceiveInput(List<float> newInput)
    {
        receivedInput = newInput;
    }

    public void Update()
    {
        if (isDead)
        {
            deathTickCounter++;
            if (deathTickCounter >= GameConfig.PLAYER_RESPAWN_TIME_IN_TICKS)
            {
                Respawn();
            }
        }
        else
        {
            currentInvulnerabilityFrame = Math.Max(currentInvulnerabilityFrame - 1, 0);

            if (receivedInput.Count < 4)
                {
                    return;
                }

            //desired speed is the speed that our input indicates normalized to MAX_SPEED
            //speed denotes the speed that we currently hold
            //we create a vector from current to desired and normalize it to P_ACCELERATION to find the speed change

            if (!isBoosted)
            {
                energy = Math.Min(energy + GameConfig.PLAYER_ENERGY_GAIN_PER_TICK, GameConfig.MAX_PLAYER_ENERGY);
            }
            else
            {
                energy = Math.Max(energy - GameConfig.BOOST_ENERGY_COST_PER_TICK, 0f);
            }

            if (receivedInput[2] == 1 && energy >= GameConfig.MINIMAL_ENERGY_TO_START_BOOST)
            {
                isBoosted = true;
            }

            if (energy <= 0f)
            {
                isBoosted = false;
            }

            if (receivedInput[3] == 1 && energy >= GameConfig.SHOOTING_ENERGY_COST)
            {
                //shooting has to be done with the help of GameMain
                willingToShoot = true;
            }

            float consideredMaxSpeed = (isBoosted ? GameConfig.MAX_BOOSTED_PLAYER_SPEED : GameConfig.MAX_PLAYER_SPEED);
            float consideredPlayerAcceleration = (isBoosted ? GameConfig.BOOSTED_PLAYER_ACCELERATION : GameConfig.PLAYER_ACCELERATION);

            desiredSpeed.X = receivedInput[0] * consideredMaxSpeed;
            desiredSpeed.Y = receivedInput[1] * consideredMaxSpeed;

            if (desiredSpeed.Magnitude() > consideredMaxSpeed)
            {
                desiredSpeed.Normalize(consideredMaxSpeed);
            }

            Pair speedChange = desiredSpeed - speed;

            if (speedChange.Magnitude() > consideredPlayerAcceleration)
            {
                speedChange.Normalize(consideredPlayerAcceleration);
            }

            speed = speed + speedChange;
            
            position.X += speed.X;
            position.Y += speed.Y;
        }
    }
}
