# Alice in Music Maze
#
Creator:

guanghuai477 - Su Minghan
CollinsVan - Fan Yuyue

Game description:

On an ordinary afternoon, Alice follows a strange white rabbit and unknowingly falls into a mysterious cave. When she comes back to her senses, she finds herself in a strange musical maze. Please help Alice find her way home!
#
Game Objective:

Use “A”, “S”, “D”, “W” on the keyboard to control Alice out of the maze. The props on the map may help you!
#
How to download the game:

Browsers copy the link below to access our project repository. You can choose to fork our project code to your repository.

Open your programming software, PyCharm or VScode is recommended, and use “Git-clone” to paste the above link to the “URL”.

Now you have all the files of our project.

https://github.com/CollinsVan/final-project.git
#
Game Over Method:

Click the “X” in the upper right corner to exit the game.


#
#
Update Log

Update 11.08:

Here's the notes:
The top left is the starting point, the bottom right is the end point, the player moves via ASDW, note that the keyboard is adjusted to “English Mode” in advance.
The maze is 15 rows, 20 columns, note that the programming default is to start counting from “0”. Each grid has corresponding coordinates, annotated on the right side of the maze array.
The blue dots are the locations of the shrinking potions, which get smaller when the player bumps into them.
The (11, 9) and (13, 9) squares are special squares that are only allowed to be passed when the player is detected to be smaller. These two squares need to be separated from the normal road grid when adding image material, to show that this is a narrow road that needs to be made smaller by drinking a potion to pass through. (For example, if the normal grid is grass material, this is vine material)

11.14 Update:

Added green guide blobs (i.e. Mr. Bunny) to guide players to the end of the maze.
Added the white color effect of the grids that the player walks through (can be replaced by the animation of flower growth later).
Added a dialog box at the beginning of the game, which is convenient for adding storyline and newbie guidance.
The grid size is standardized to 40 pixels * 40 pixels, try to lay the grass material, the material name is grass2.gif.

11.18 Update:

Merged the material images.
Added background music.
Tried to add the text box for game start, stay for 4 seconds and it will disappear. (Later can follow your code I'm making extra stuff again orz)

11.24 Update:

Added shrinking potion sound effect.
Added parcel sound effect, but it's hard to hear TAT.
Added Mr. Bunny.
Added dialog at the beginning of the game and when the player hits the wall.

11.27 Updated:

Added game start screen.
Fixed the bug that the rabbit is shaking.
Fixed the bug that the rabbit will reappear after the second dialog box display ends.

11.28 Updated content:

Added end of game music and pictures.
Tested that the game works fine.
