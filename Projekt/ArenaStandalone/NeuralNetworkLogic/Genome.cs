using System;
using System.Collections.Generic;
using MathNet.Numerics.LinearAlgebra;

using System.IO;
using Newtonsoft.Json;
using System.Runtime.InteropServices;

/*
    Exception because it's gonna bug A LOT :c
*/
[System.Serializable]
public class GenomeException : System.Exception
{
    public GenomeException() { }
    public GenomeException(string message) : base(message) { }
    public GenomeException(string message, System.Exception inner) : base(message, inner) { }
    protected GenomeException(
        System.Runtime.Serialization.SerializationInfo info,
        System.Runtime.Serialization.StreamingContext context) : base(info, context) { }
}


/*
    The genome represents the shape and form of the model. It also stores the weights of
    each edge. Its only purpouse is to store weights of the neural network
    We can save and load genomes from files, there is also an interface for crossover algorithm for genomes 
*/

public class Genome
{

    [Serializable]
    private class SerializableGenome
    {
        public List<float[,]> Weights;
        public List<float[]> Biases;
    }

    public int LayerCount
    {
        get
        {
            return Weights.Count + 1;
        }
    }
    public List<Matrix<float>> Weights;  // Each Matrix is a layer's weights
    public List<Vector<float>> Biases;  // Each Vector is a layer's bias

    public Genome(List<Matrix<float>> weights, List<Vector<float>> biases)
    {
        this.Weights = weights;
        this.Biases = biases;
    }
    /* This function creates a new genome with random initialized weights */
    public static Genome CreateNew(List<int> shape)
    {
        List<int> architecture = new List<int>
        {
            AlgorithmConfig.input_size
        };
        architecture.AddRange(shape);
        architecture.Add(AlgorithmConfig.output_size);

        int n = architecture.Count - 1;  // Number of layers
        List<Matrix<float>> weights = new List<Matrix<float>>(n);
        List<Vector<float>> biases = new List<Vector<float>>(n);

        for (int i = 0; i < n; i++)
        {
            int inputDim = architecture[i];
            int outputDim = architecture[i + 1];

            Matrix<float> w = Matrix<float>.Build.Dense(outputDim, inputDim);
            Vector<float> b = Vector<float>.Build.Dense(outputDim);

            // He standard deviation
            float stddev = (float)Math.Sqrt(2.0 / inputDim);

            for (int y = 0; y < outputDim; y++)
            {
                for (int x = 0; x < inputDim; x++)
                {
                    w[y, x] = RandomUtils.NextGaussian(0f, stddev);
                }
                b[y] = RandomUtils.NextGaussian(0f, stddev); // Biases typically start at 0, i tried adding some noise for different results
            }

            weights.Add(w);
            biases.Add(b);
        }

        return new Genome(weights, biases);
    }
    /*
        This function is used to save current Genome to file (using JsonSerializer from Newtonsoft)
    */
    public void Save(string fileName)
    {
        var serializable = new SerializableGenome
        {
            Weights = new List<float[,]>(),
            Biases = new List<float[]>()
        };

        foreach (var w in Weights)
            serializable.Weights.Add(w.ToArray());

        foreach (var b in Biases)
            serializable.Biases.Add(b.ToArray());

        string toSave = JsonConvert.SerializeObject(serializable);
        System.IO.File.WriteAllText(fileName, toSave);
    }
    /*
        This function retrieves genome from previously saved file (using JsonDeserializer from Newtonsoft)
    */
    public static Genome Load(string fileName)
    {
        string s = System.IO.File.ReadAllText(fileName);
        SerializableGenome loaded = JsonConvert.DeserializeObject<SerializableGenome>(s);
        List<Matrix<float>> w = new List<Matrix<float>>();
        List<Vector<float>> b = new List<Vector<float>>();
        foreach (var e in loaded.Weights)
            w.Add(Matrix<float>.Build.DenseOfArray(e));
        foreach (var f in loaded.Biases)
            b.Add(Vector<float>.Build.DenseOfArray(f));
        return new Genome
        (w, b);

    }

    /*
        This function accepts two genomes and outputs one that is crossover of the two (with possible mutations)
    */

    public static Genome Crossover(Genome first, Genome second)
    {
        // 1. Validate that the genomes have the same architecture
        if (first.Weights.Count != second.Weights.Count || first.Biases.Count != second.Biases.Count)
        {
            throw new GenomeException("Cannot perform crossover: Genomes have different numbers of layers.");
        }

        List<Matrix<float>> childWeights = new List<Matrix<float>>(first.Weights.Count);
        List<Vector<float>> childBiases = new List<Vector<float>>(first.Biases.Count);

        // 2. Iterate through each layer's weights and biases
        for (int i = 0; i < first.Weights.Count; i++)
        {
            // Ensure dimensions match for the current layer
            if (first.Weights[i].RowCount != second.Weights[i].RowCount ||
                first.Weights[i].ColumnCount != second.Weights[i].ColumnCount)
            {
                throw new GenomeException($"Cannot perform crossover: Weight matrix dimensions mismatch at layer {i}.");
            }
            if (first.Biases[i].Count != second.Biases[i].Count)
            {
                throw new GenomeException($"Cannot perform crossover: Bias vector dimensions mismatch at layer {i}.");
            }

            // --- Crossover for Weights ---
            Matrix<float> wChild = Matrix<float>.Build.Dense(first.Weights[i].RowCount, first.Weights[i].ColumnCount);
            for (int r = 0; r < wChild.RowCount; r++)
            {
                for (int c = 0; c < wChild.ColumnCount; c++)
                {
                    // For each weight, randomly choose from first or second parent
                    if (RandomUtils.NextGaussian() < 0f) // 50% chance to inherit from first parent
                    {
                        wChild[r, c] = first.Weights[i][r, c];
                    }
                    else // 50% chance to inherit from second parent
                    {
                        wChild[r, c] = second.Weights[i][r, c];
                    }
                }
            }
            childWeights.Add(wChild);

            // --- Crossover for Biases ---
            Vector<float> bChild = Vector<float>.Build.Dense(first.Biases[i].Count);
            for (int j = 0; j < bChild.Count; j++)
            {
                // For each bias, randomly choose from first or second parent
                if (RandomUtils.NextGaussian() < 0f) // 50% chance to inherit from first parent
                {
                    bChild[j] = first.Biases[i][j];
                }
                else
                {
                    bChild[j] = second.Biases[i][j];
                }
            }
            childBiases.Add(bChild);
        }

        // 3. Return the newly created child genome
        return new Genome(childWeights, childBiases);
    }

    public Genome Clone()
    {
        List<Matrix<float>> clonedWeights = new List<Matrix<float>>();
        foreach (var w in Weights)
        {
            clonedWeights.Add(w.Clone()); // MathNet's Matrix has a Clone method
        }

        List<Vector<float>> clonedBiases = new List<Vector<float>>();
        foreach (var b in Biases)
        {
            clonedBiases.Add(b.Clone()); // MathNet's Vector has a Clone method
        }
        return new Genome(clonedWeights, clonedBiases);
    }

    public static Genome Mutate(Genome originalGenome, float mutationStrength = 0.1f) // Increased default strength slightly for more impact
    {
        // Create a deep copy to avoid modifying the original genome
        Genome mutatedGenome = originalGenome.Clone();

        for (int i = 0; i < mutatedGenome.Weights.Count; i++)
        {
            // Mutate weights
            Matrix<float> currentWeights = mutatedGenome.Weights[i];
            for (int r = 0; r < currentWeights.RowCount; r++)
            {
                for (int c = 0; c < currentWeights.ColumnCount; c++)
                {
                    currentWeights[r, c] += RandomUtils.NextGaussian(0f, mutationStrength);
                }
            }

            // Mutate biases
            Vector<float> currentBiases = mutatedGenome.Biases[i];
            for (int j = 0; j < currentBiases.Count; j++)
            {
                currentBiases[j] += RandomUtils.NextGaussian(0f, mutationStrength);
            }
        }
        return mutatedGenome;
    }
    
public static Genome Extend(Genome genome, List<int> new_hidden_layer_sizes)
{
    // 1. Get the full current architecture for comparison
    List<int> current_architecture = new List<int> { AlgorithmConfig.input_size };
    for (int i = 0; i < genome.Biases.Count; i++) // Iterate through all bias layers (hidden + output)
    {
        current_architecture.Add(genome.Biases[i].Count);
    }
    // Now, current_architecture contains [input_size, hidden1_size, hidden2_size, ..., output_size]

    // 2. Construct the full new architecture (input, new_hidden_layer_sizes, output)
    List<int> new_full_architecture = new List<int> { AlgorithmConfig.input_size };
    new_full_architecture.AddRange(new_hidden_layer_sizes);
    new_full_architecture.Add(AlgorithmConfig.output_size);

    // 3. Validate the extension
    // Ensure the number of layers is not decreasing, and no existing layer is shrinking
    if (new_full_architecture.Count < current_architecture.Count)
    {
        throw new GenomeException("Cannot extend: New architecture has fewer layers than the original.");
    }

    for (int i = 0; i < current_architecture.Count; i++)
    {
        // For existing layers, ensure the new size is not smaller than the current size
        // This covers input, all hidden, and output layers
        if (i < new_full_architecture.Count && new_full_architecture[i] < current_architecture[i])
        {
            string layerName = "";
            if (i == 0) layerName = "Input";
            else if (i == current_architecture.Count - 1) layerName = "Output";
            else layerName = $"Hidden {i}";
            throw new GenomeException($"Cannot extend: {layerName} layer size ({new_full_architecture[i]}) is smaller than original ({current_architecture[i]}).");
        }
    }


    // 4. Create a new genome with the desired new_full_architecture, but with custom initialization
    // Instead of CreateNew (which initializes randomly), we'll build it to initialize to 0 first.
    int n = new_full_architecture.Count - 1; // Number of weight/bias matrices
    List<Matrix<float>> resultWeights = new List<Matrix<float>>(n);
    List<Vector<float>> resultBiases = new List<Vector<float>>(n);

    for (int i = 0; i < n; i++)
    {
        int inputDim = new_full_architecture[i];
        int outputDim = new_full_architecture[i + 1];
        resultWeights.Add(Matrix<float>.Build.Dense(outputDim, inputDim, 0f)); // Initialize all to 0
        resultBiases.Add(Vector<float>.Build.Dense(outputDim, 0f));          // Initialize all to 0
    }
    Genome result = new Genome(resultWeights, resultBiases);


    // 5. Copy existing weights and biases from the original genome
    // Iterate through layers that exist in the *original* genome
    for (int idx = 0; idx < genome.Weights.Count; idx++)
    {
        // Copy weights
        // Determine the smaller dimension for copying
        int copyRows = Math.Min(genome.Weights[idx].RowCount, result.Weights[idx].RowCount);
        int copyCols = Math.Min(genome.Weights[idx].ColumnCount, result.Weights[idx].ColumnCount);

        for (int r = 0; r < copyRows; r++)
        {
            for (int c = 0; c < copyCols; c++)
            {
                result.Weights[idx][r, c] = genome.Weights[idx][r, c];
            }
        }

        // Copy biases
        int copyBiasElements = Math.Min(genome.Biases[idx].Count, result.Biases[idx].Count);
        for (int b = 0; b < copyBiasElements; b++)
        {
            result.Biases[idx][b] = genome.Biases[idx][b];
        }
    }

    return result;
}
}
