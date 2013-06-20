//Edited by Feng Yi on 04/04/2008
//read values for Start_step and Stop_Step
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "FemDefinitions.h"
#include "FemGlobals.h"
#include "FemSim.h"



int ReadParameters(FILE *f) {

  char s[1024];

  if(!GetLine(f, s)) {
    proglog("Parameters file terminated prematurely.  Exiting.\n");
    exit(0);
  }
  sscanf(s, "%f %f %d", &K_mini, &K_scal, &K_step);

  if(!GetLine(f, s)) {
    proglog("Parameters file terminated prematurely.  Exiting.\n");
    exit(0);
  }
  sscanf(s, "%f", &Q_aperture);

  if(!GetLine(f, s)) {
    proglog("Parameters file terminated prematurely.  Exiting.\n");
    exit(0);
  }
  //sscanf(s, "%d %f", &Angl_step, &Thet_ofst);
  sscanf(s, "%d %d %d", &Angl_step, &Start_Step, &Stop_Step); //Edited by Feng Yi on 04/04/2008
  Thet_ofst=0;
  if(Angl_step) {
    Do_rotations = 1;
  }
  else {
    Do_rotations = 0;
    phi_step = 1;
    theta_step = 1;
    psi_step = 1;
  }

  if(!GetLine(f, s)) {
    proglog("Parameters file terminated prematurely.  Exiting.\n");
    exit(0);
  }
  Imag_mesh_x = atoi(s); // check if the line starts with a number
  if(Imag_mesh_x) {
    sscanf(s, "%d %d", &Imag_mesh_x, &Imag_mesh_y);
    PixelMode = 1; // square mesh
  } else {
    sscanf(s, "%s ", PixelFile);
    PixelMode = 2; // read file
  }

  if(!GetLine(f, s)) {
    proglog("Parameters file terminated prematurely.  Exiting.\n");
    exit(0);
  }
  sscanf(s, "%d", &Algorithm);
  switch(Algorithm) {
  case 1: // sum
    break;
  case 2: // g2
    if(!GetLine(f, s)) {
      proglog("Parameters file terminated prematurely.  Exiting.\n");
      exit(0);
    }
    sscanf(s, "%f", &Delta_r);
    R_step = (int)ceil(0.61/(Q_aperture*Delta_r));
    break;
  case 3: // multslice
    proglog("This algorithm is not yet implemented.  Exiting.\n");
    exit(0);
    break;
  default:
    sprintf(tolog, "Algorithm %d is not a choice.  Exiting.\n", Algorithm);
    proglog(tolog);
    exit(0);
  }
  
  return 1;
}

int GetLine(FILE *f, char *s) {

  int i=0;

  while(1) {
    fgets(s, 1024, f);
    if(!s) return 0;

    while(1) {
      if(s[i] == '#') {
	s[i] = '\0';
	break;
      }
      if(s[i] == '\0')
	break;
      i++;
    }
    if(strlen(s)) break;
  }

  return 1;
}
