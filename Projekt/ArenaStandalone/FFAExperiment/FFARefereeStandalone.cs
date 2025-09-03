using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.IO.Enumeration;

/*
This is meant to be run in complete separation from Unity
*/

public class FFARefereeStandalone
{
    private List<int> midLayerSizes = new List<int> {24, 16, 8};

    private int maxWarriorsToDefeat = 10;

    Random RANDOM = new Random();

    private List<GamePlayerController> currentWarriors;

    private Genome currentBestGenome;

    private int currentTournamentID;

    public FFARefereeStandalone()
    {
        currentWarriors = new List<GamePlayerController>();

        TryLoadBestGenomes();
    }

    private void TryLoadBestGenomes()
    {
        string bestGenomesDir = "./FFAExperiment/BestGenomes";

        if (!Directory.Exists(bestGenomesDir))
            return;

        var files = Directory.GetFiles(bestGenomesDir, "Genome_*.json");

        if (files.Length == 0)
            return;

        // Sort files by the integer value after "Genome_"
        var topFiles = files
            .Select(f => new { File = f, Num = ExtractNumberFromFilename(f) })
            .OrderByDescending(f => f.Num)
            .ToList();

        currentWarriors.Clear();

        foreach (var file in topFiles)
            {
                if (currentBestGenome == null)
                {
                    currentBestGenome = Genome.Load(file.File);
                }
                currentWarriors.Add(new NNBot(Genome.Load(file.File)));
            }

        currentTournamentID = currentWarriors.Count + 1;
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

    private float currentMutationDeviation = 0.01f; // Start with your initial value
    private int stagnationCounter = 0;
    private const int StagnationThreshold = 500; // Number of failed attempts before increasing mutation
    private const float MutationIncreaseFactor = 0.01f; // How much to increase deviation
    private const float MinMutationDeviation = 0.01f; // Prevent deviation from becoming too small
    private const float MaxMutationDeviation = 0.01f;  // Prevent deviation from becoming too large


    private void RunOneExperiment()
    {
        Genome testedGenome;

        if (currentBestGenome == null)
        {
            testedGenome = Genome.CreateNew(midLayerSizes);
        }
        else
        {
            testedGenome = Genome.Mutate(currentBestGenome, currentMutationDeviation);
        }

        GamePlayerController nnbot = new NNBot(testedGenome);

        bool undefeatable = true;

        foreach (GamePlayerController opponent in currentWarriors)
        {
            List<float> performance = ModelEvaluationFunctions.OverallExperiment(nnbot, opponent);

            if (performance[0] <= performance[1])
            {
                undefeatable = false;
                break;
            }
        }

        if (undefeatable)
        {
            currentWarriors.Insert(0, nnbot);

            currentTournamentID++;

            currentMutationDeviation = MinMutationDeviation;
        }
        else
        {
            stagnationCounter++;
            if (stagnationCounter > StagnationThreshold)
            {
                currentMutationDeviation += MutationIncreaseFactor;
                currentMutationDeviation = Math.Min(currentMutationDeviation, MaxMutationDeviation);
                stagnationCounter = 0;
            }
        }
    }

    public void RunForever()
    {
        currentMutationDeviation = 0.01f;
        while (true)
        {
            RunOneExperiment();
        }
    }
}

