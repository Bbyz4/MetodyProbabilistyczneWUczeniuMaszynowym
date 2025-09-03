/*
    This file will be responsible for testing genoms, picking best instances,
    combining genotypes and mutating the genes and so on and so on...
    All the learning will be done here, not in the neural networks (they will only
    be used for evaluation)

    Sample learning algorithm::

    genomes = { random genomes }
    for(int i = 0; i < iterations_count; i++) {
        foreach (genome in genomes) {
            * play match
            * evaluate (maybe by comparing genomes by playing games between them)
        }
        * select best genome(s) based on results
        * do something, mutate and fill genomes table
    }
*/
using System;
using System.Collections.Generic;
using System.Linq;


/* Here is a sketch of how a factory might look like */

public class ModelFactory
{
    /* Here are the parameters of the factory: */

    /* Determines the architecture of models */
    public List<int> Shape { get; set; } = new List<int> { 16, 8 };
    /* How many generations should Train train? */
    public int GenerationCount { get; set; } = 1000;
    /* How many models in a generation? */
    public int PopulationSize { get; set; } = 32;
    /* How many models should an evaluated model play? */
    public int TournamentSize { get; set; } = 5;
    /* What percent of models are the one we train new population on? 
        How many top performes to select? */
    public double ElitismRate { get; set; } = 0.125;

    private List<Genome> currentPopulation;

    /* Perform TrainOne() multiple times */
    public void Train()
    {
        for (int generation = 0; generation < GenerationCount; generation++)
        {
            TrainOne();
        }
    }
    /* Create a new population based on existing one */
    public void TrainOne()
    {
        if (currentPopulation == null || currentPopulation.Count == 0)
        {
            currentPopulation = new List<Genome>();
            for (int i = 0; i < PopulationSize; i++)
            {
                currentPopulation.Add(Genome.CreateNew(Shape));
            }
        }


        // Step 1: Make models play against each other, assign scores
        Dictionary<Genome, double> fitnessScores
        = EvaluateFitness(currentPopulation);

        // Step 2: Select elites for the new population
        var sorted = fitnessScores.OrderByDescending(kv => kv.Value).Select(kv => kv.Key).ToList();
        int eliteCount = (int)(ElitismRate * PopulationSize);
        List<Genome> new_population = sorted.Take(eliteCount).ToList();

        /* Step 3: Generate new genomes via crossover
            We need to think of strategy to select parents to train on
            We also might want to add completely random models to the population?
        */
        while (new_population.Count < PopulationSize)
        {
            var parent1 = SelectForBreeding(fitnessScores);
            var parent2 = SelectForBreeding(fitnessScores);

            var child = Genome.Crossover(parent1, parent2);

            // Maybe now we should mutate the child?

            new_population.Add(child);
        }

        /* We can think of a way to store previous populations */
        currentPopulation = new_population;

    }

    /* This function determines how good the models perform. */

    private Dictionary<Genome, double> EvaluateFitness(List<Genome> population)
    {
        var scores = new Dictionary<Genome, double>();
        foreach (var genome in population)
        {
            scores[genome] = 0;
        }
        Random rnd = new Random();
        //Match each genome with TournamentSize random opponents
        foreach (var genome in population)
        {
            for (int i = 0; i < TournamentSize;)
            {
                var opponent = population[rnd.Next(population.Count)];
                if (opponent == genome) continue;

                int result = 0; // result = play(genome, opponent); 
                scores[genome] += result;
                i++;
            }
        }

        return scores;
    }

    /* Select one of parents for breeding */
    private Genome SelectForBreeding(Dictionary<Genome, double> fitnessScores)
    {
        return null;
    }
}
