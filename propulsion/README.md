# DBF 2026-2027 Propulsion Model

This directory contains the MATLAB/Simulink propulsion model for the 2026-2027 DBF aircraft.

## MATLAB Project

The propulsion model is managed as a MATLAB Project.

Open:

`DBF_Propulsion.prj`

Opening the project ensures that everyone is working from the same project environment and makes MATLAB source-control tools available.

## Main Model

`singleprop.slx`

## First-Time Setup

1. Open MATLAB.
2. Clone the DBF repository from GitHub:
   `https://github.com/cbtharin/DBF-2026-2027.git`
3. Choose a local folder where the repository should be saved.
4. Open:
   `propulsion/DBF_Propulsion.prj`

## Running the Model

1. Clone or pull the latest version of the DBF repository before beginning work.
2. Open MATLAB.
3. Open `propulsion/DBF_Propulsion.prj`.
4. Run `initialize_propulsion.m`.
5. Open `singleprop.slx`.
6. Run the simulation.

Shared model parameters should gradually be moved into `initialize_propulsion.m` or other external data files rather than being hardcoded directly into the Simulink model.

## Git Workflow

Do not make propulsion changes directly on `main`.

Before beginning work:

1. Pull the latest version of `main`.
2. Create a new branch for your task from the branch manager.
3. Make and save your changes.
4. Commit the changes to your branch.
5. Push the branch to GitHub.
6. Create a pull request into `main`.

Example branch names:

- `propulsion/motor-model`
- `propulsion/propeller-model`
- `propulsion/battery-model`
- `propulsion/aero-update`

### Using MATLAB

MATLAB can be used for most Git operations without using the Terminal.

From the MATLAB Source Control interface:

1. Switch to `main`.
2. Pull the latest changes.
3. Create or switch to your task branch.
4. Edit and save the Simulink/MATLAB files.
5. Review the changed files in Source Control.
6. Commit the changes with a descriptive message.
7. Push the branch to GitHub.
8. Create a pull request on GitHub.

Example commit message:

`Update propeller torque model`

### Using Terminal

If you prefer the command line:

```bash
git checkout main
git pull origin main
git checkout -b propulsion/<task-name>
