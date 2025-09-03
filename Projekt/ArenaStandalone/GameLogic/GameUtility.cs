using System;

public class GameUtility
{
    public static bool InCircleInsideAnotherCircle(Pair smallerCircleCenter, float smallerCircleRadius, Pair biggerCircleCenter, float biggerCircleRadius)
    {
        float dx = smallerCircleCenter.X - biggerCircleCenter.X;
        float dy = smallerCircleCenter.Y - biggerCircleCenter.Y;
        float distance = MathF.Sqrt(dx * dx + dy * dy);

        return distance + smallerCircleRadius <= biggerCircleRadius;
    }

    public static bool DoCirclesOverlap(Pair centerA, float radiusA, Pair centerB, float radiusB)
    {
        float dx = centerA.X - centerB.X;
        float dy = centerA.Y - centerB.Y;
        float distance = MathF.Sqrt(dx * dx + dy * dy);

        return distance < (radiusA + radiusB);
    }
}
