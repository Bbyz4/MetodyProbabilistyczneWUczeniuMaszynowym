using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.ComponentModel.DataAnnotations;

/*
This is meant to be run in complete separation from Unity
*/

public class ArenaRefereeStandalone
{
    private Random RANDOM;

    private bool isVisuallyRepresented = false;
    private int groupSize = 50;
    private int winnerGroupSize = 10; //bots that automatically advance to the next round
    private List<int> midLayerSizes = new List<int> {24,16,8};
    private int tournamentSelectionSize = 5;

    private float mutationStrength = 0.01f;
    private float crossoverRate = 0.5f;

    private List<Genome> currentWarriors;
    private List<float> currentPoints;
    private Queue<(int x, int y)> matchQueue;
    private int currentTournamentID;

    public ArenaRefereeStandalone()
    {
        RANDOM = new Random();

        currentWarriors = new List<Genome>(groupSize);
        currentPoints = new List<float>(groupSize);
        matchQueue = new Queue<(int x, int y)>();
        currentTournamentID = 1;

        TryLoadBestGenomes();

        Console.WriteLine($"PRELOADED {currentWarriors.Count} GENOMES!");

        while (currentWarriors.Count < groupSize)
        {
            currentWarriors.Add(Genome.CreateNew(midLayerSizes));
            currentPoints.Add(0f);
        }
    }

    private void TryLoadBestGenomes()
    {
        string bestGenomesDir = "./ArenaExperiment/BestGenomes";

        if (!Directory.Exists(bestGenomesDir))
            return;

        var files = Directory.GetFiles(bestGenomesDir, "Genome_*.json");

        if (files.Length == 0)
            return;

        // Sort files by the integer value after "Genome_"
        var topFiles = files
            .Select(f => new { File = f, Num = ExtractNumberFromFilename(f) })
            .OrderByDescending(f => f.Num)
            .Take(groupSize)
            .ToList();

        currentWarriors.Clear();

        foreach (var file in topFiles)
        {
            if (currentWarriors.Count < groupSize)
            {
                currentWarriors.Add(Genome.Load(file.File));
                currentPoints.Add(0f);
            }
        }

        while (currentWarriors.Count < groupSize)
        {
            currentWarriors.Add(Genome.CreateNew(midLayerSizes));
            currentPoints.Add(0f);
        }

        // Update the currentTournamentID to be one more than the highest found
        if (topFiles.Any())
        {
            currentTournamentID = topFiles.Max(f => f.Num) + 1;
        }
        else
        {
            currentTournamentID = 1;
        }
    }

    private int ExtractNumberFromFilename(string filename)
    {
        var name = Path.GetFileNameWithoutExtension(filename);
        var parts = name.Split('_');
        if (parts.Length < 2)
            return -1;

        if (int.TryParse(parts[1], out int number))
            return number;

        return -1;
    }

    private void InitializeQueue()
    {
        matchQueue.Clear();

        for (int i = 0; i < groupSize; i++)
        {
            for (int j = i + 1; j < groupSize; j++)
            {
                matchQueue.Enqueue((i, j));
                matchQueue.Enqueue((j, i));
            }
        }
    }
    
    private Genome SelectParent(List<KeyValuePair<Genome, float>> evaluatedGenomes)
    {
        Genome bestInTournament = null;
        float bestFitnessInTournament = float.NegativeInfinity;

        // Perform a tournament to select a parent
        for (int i = 0; i < tournamentSelectionSize; i++)
        {
            int randomIndex = RANDOM.Next(evaluatedGenomes.Count);
            var candidate = evaluatedGenomes[randomIndex];

            if (candidate.Value > bestFitnessInTournament)
            {
                bestFitnessInTournament = candidate.Value;
                bestInTournament = candidate.Key;
            }
        }
        return bestInTournament.Clone(); 
    }

    private void CreateNewGeneration()
    {
        Console.WriteLine($"TOURNAMENT {currentTournamentID} RESULTS: {string.Join("| ", currentPoints)}");

        List<KeyValuePair<Genome, float>> evaluatedGenomes =
        currentWarriors.Zip(currentPoints, (genome, points) =>
        new KeyValuePair<Genome, float>(genome, points))
                        .OrderByDescending(kvp => kvp.Value)
                        .ToList();

        string winnerSavePath = $"./ArenaExperiment/BestGenomes/Genome_{currentTournamentID}.json";
        evaluatedGenomes[0].Key.Save(winnerSavePath);

        //Zapisanie najlepszego zawodnika oraz jego wyniku w odpowiednich miejscach

        currentTournamentID++;

        List<Genome> nextGeneration = new List<Genome>();

        for (int i = 0; i < Math.Min(winnerGroupSize, evaluatedGenomes.Count); i++)
        {
            nextGeneration.Add(evaluatedGenomes[i].Key.Clone());
        }

        while (nextGeneration.Count < groupSize)
        {
            Genome parent1 = SelectParent(evaluatedGenomes);
            Genome parent2 = SelectParent(evaluatedGenomes);

            Genome offspring;

            if (RANDOM.NextDouble() < crossoverRate)
            {
                offspring = Genome.Crossover(parent1, parent2);
            }
            else
            {
                offspring = parent1.Clone();
            }

            offspring = Genome.Mutate(offspring, mutationStrength);

            nextGeneration.Add(offspring);
        }

        currentWarriors = nextGeneration;

        currentPoints.Clear();
        for (int i = 0; i < groupSize; i++)
        {
            currentPoints.Add(0f);
        }
    }

    public void RunOneTournament()
    {
        Console.WriteLine("New tournament starting!");
        InitializeQueue();
        Console.WriteLine($"There will be {matchQueue.Count} matches!");

        List<NNBot> tournamentPlayers = new List<NNBot>();

        for (int i = 0; i < groupSize; i++)
        {
            tournamentPlayers.Add(new NNBot(currentWarriors[i]));
            currentPoints[i] = 0f;
        }

        int currentMatchNumber = 1;

        while (matchQueue.Count > 0)
        {
            currentMatchNumber++;

            var top = matchQueue.Peek();
            matchQueue.Dequeue();

            int X = top.x;
            int Y = top.y;

            List<float> matchResult = ModelEvaluationFunctions.ModifiedOverallExperiment(
                tournamentPlayers[X], tournamentPlayers[Y]);

            currentPoints[X] += matchResult[0];
            currentPoints[Y] += matchResult[1];
        }

        CreateNewGeneration();
    }

    public void RunForever()
    {
        while (true)
        {
            RunOneTournament();
        }
    }
}

