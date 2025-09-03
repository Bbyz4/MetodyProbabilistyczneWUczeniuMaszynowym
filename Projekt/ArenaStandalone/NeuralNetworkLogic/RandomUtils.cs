using System;

/* Gaussian Distribution, needed for example for weight initialization */
static class RandomUtils
{
    private static Random rand = new Random();

    public static float NextGaussian(float mean = 0f, float stdDev = 1f)
    {
        double u1 = 1.0 - rand.NextDouble(); // [0,1)
        double u2 = 1.0 - rand.NextDouble();
        double randStdNormal = Math.Sqrt(-2.0 * Math.Log(u1)) *
                               Math.Sin(2.0 * Math.PI * u2);
        return (float)(mean + stdDev * randStdNormal);
    }
}