using System;
using System.Collections.Generic;

public interface GamePlayerController
{
    //return a list of {x_input value [-1,1], y_input value [-1,1], boost {0,1}, shoot {0,1}}
    List<float> GetInputValues(GameMain gameInstance, int whoAmI);
}
