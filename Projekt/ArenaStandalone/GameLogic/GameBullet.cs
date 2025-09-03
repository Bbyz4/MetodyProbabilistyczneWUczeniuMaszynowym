using System;

public class GameBullet
{
    public int ID { get; private set; }
    public Pair position { get; private set; }
    public Pair speed { get; private set;  }
    public bool hadCollided;
    public GameBullet(int myID)
    {
        ID = myID;
        hadCollided = false;
    }

    public void SetParams(Pair myPos, Pair mySpeed)
    {
        position = myPos;
        speed = mySpeed;
    }

    public void Update()
    {
        position += speed;
    }
}
