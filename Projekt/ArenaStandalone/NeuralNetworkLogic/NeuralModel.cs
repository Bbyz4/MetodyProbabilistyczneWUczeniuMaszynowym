using System;
using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra;

/*
    This is an instance of a genome, which will be evaluated based on its score during
    the game. 
    I think it should be players' responsibility to consult the neural model and factory's
    responsibility to instantiate the game and load players with NeuralModels and their 
    genoms
*/
public class NeuralModel
{
    public static float ReLU(float x) => Math.Max(0f, x);
    public static float Sigmoid(float x) => 1f / (1f + (float)Math.Exp(-x));

    /*
        The genome argument sets all the weights in the neural network model.
    */
    private Genome genome;
    public NeuralModel(Genome genome)
    {
        this.genome = genome;
    }
    /*
        This function evaluates next input based on game state. For each output it evaluates how likely
    */
    public Vector<float> Forward(Vector<float> game_state) {
        Dictionary<int, Vector<float>> layer = new()
        {
            [0] = game_state
        };
        int last_layer = genome.LayerCount - 2;
        for (int i = 0; i < genome.LayerCount - 1; i++)
        {
            layer[i + 1] = genome.Weights[i] * layer[i] + genome.Biases[i];
            for (int j = 0; j < layer[i + 1].Count; j++)
                if (i != last_layer)
                    layer[i + 1][j] = ReLU(layer[i + 1][j]);
                else layer[i + 1][j] = Sigmoid(layer[i + 1][j]);
        }
        Vector<float> pressed = Vector<float>.Build.Dense(AlgorithmConfig.output_size);
        for (int i = 0; i < AlgorithmConfig.output_size; i++)
        {
            pressed[i] = layer[genome.LayerCount - 1][i];
        }

        return pressed;
    }
}