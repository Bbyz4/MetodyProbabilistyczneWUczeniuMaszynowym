//A custom Pair structure made to hold some functionalities of Unity's Vector2

using System;

public struct Pair
{
    public float X {get; set; }
    public float Y {get; set; }

    public Pair(float x = 0, float y = 0)
    {
        X = x;
        Y = y;
    }

    public static Pair operator +(Pair p1, Pair p2)
    {
        return new Pair(p1.X + p2.X, p1.Y + p2.Y);
    }

    public static Pair operator -(Pair p1, Pair p2)
    {
        return new Pair(p1.X - p2.X, p1.Y - p2.Y);
    }

    public static float DotProduct(Pair p1, Pair p2)
    {
        return p1.X * p2.X + p1.Y * p2.Y;
    }

    public float Magnitude()
    {
        return (float)Math.Sqrt(X * X + Y * Y);
    }

    public void Normalize(float newMagnitude)
    {
        float currentMagnitude = Magnitude();

        if(currentMagnitude == 0)
        {
            return;
        }

        X *= (newMagnitude / currentMagnitude);
        Y *= (newMagnitude / currentMagnitude);
    }
}
