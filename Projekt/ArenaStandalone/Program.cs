class Program
{
    static void Main(string[] args)
    {
        if (args.Length > 0)
        {
            Console.WriteLine(args[0].ToLower());

            switch (args[0].ToLower())
            {
                case "arena":
                    ArenaRefereeStandalone arena = new ArenaRefereeStandalone();
                    arena.RunForever();
                    break;
                case "ffa":
                    FFARefereeStandalone ffa = new FFARefereeStandalone();
                    ffa.RunForever();
                    break;
                default:
                    break;
            }
        }
    }
}
