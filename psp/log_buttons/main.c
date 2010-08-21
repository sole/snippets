// Soledad Penades http://soledadpenades.com
#include <stdlib.h>
#include "SDL.h"
#include "SDL_main.h"

#ifdef PSP
	#include <pspdebug.h>
	#define printf pspDebugScreenPrintf
#else
	#include <stdio.h>
#endif

#define W 480
#define H 272

SDL_Surface *screen;

void printJoystickInfo(SDL_Joystick *joystick)
{
	int index;

	index = SDL_JoystickIndex(joystick);

	printf(	"JOYSTICK INFO\n\n"
			"Index: %d\n"
			"Name: %s\n"
			"Num axes: %d\n"
			"Num balls: %d\n"
			"Num hats: %d\n"
			"Num buttons: %d\n",
			index,
			SDL_JoystickName(index),
			SDL_JoystickNumAxes(joystick),
			SDL_JoystickNumBalls(joystick),
			SDL_JoystickNumHats(joystick),
			SDL_JoystickNumButtons(joystick)
	);
}

int main(int argc, char *argv[])
{
	SDL_Joystick *joystick = NULL;
	SDL_Event event;
	int done = 0;

	if(SDL_Init(SDL_INIT_VIDEO | SDL_INIT_JOYSTICK) < 0)
	{
		printf("init error: %s\n", SDL_GetError());
		return 1;
	}

	if((screen = SDL_SetVideoMode(W, H, 32, 0)) == NULL)
	{
		printf("SetVideoMode: %s\n", SDL_GetError());
		return 1;
	}

	SDL_Delay(1000);

	if(SDL_NumJoysticks())
	{
		joystick = SDL_JoystickOpen(0);
		printJoystickInfo(joystick);
	}
	else
	{
		printf("No joystick detected\n");
	}

	done = 0;
	while(!done)
	{
		while(SDL_PollEvent(&event))
		{
			switch(event.type)
			{
			case SDL_JOYBUTTONDOWN:
				printf("Pressed button %d\n", event.jbutton.button);
				break;
			case SDL_JOYAXISMOTION:
				printf("Axis motion: j index = %d axis = %d value = %d\n", event.jaxis.which, event.jaxis.axis, event.jaxis.value);
				break;
			case SDL_QUIT:
				done = 1;
				break;
			}
		}
	}

	if(joystick)
	{
		SDL_JoystickClose(joystick);
	}

	SDL_Quit();

	return(0);
}
