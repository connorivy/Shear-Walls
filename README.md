# Shear-Walls

### The problem being solved:
My current company uses a very complex spreadsheet to design shear walls. There are several issues with doing that.
1. The formulas are very complicated and references other sheets, so it is extremely time consuming to find out what the program is actually doing.
2. There is no testing whatsoever, so we could potentially have been using an incorrect spreadsheet to design buildings for the last 30 years.
3. The input cells are spread out between dozens of sheets (one sheet per wall designed) so it takes forever to adapt to a new project.

This is a simple program to simplify the user input, add some unittesting, and make the program more readable.

As a bonus, you can import the designed values directly into Revit instead of individually changing hundreds (or sometimes thousands) of shear wall annotations in a Revit model. This function alone saves each project probably a week of labor for each project.

I would like to spend more time on developing this program because it is actually used to design important systems, however I don't get paid to write programs so it's hard to find the time. Right now, all project information is hard coded in shear_wall_classes, so that needs to be edited when apply the program to new projects.

### Using the program:
#### Step 1 - Clone and Install Dependencies:
`git clone https://github.com/connorivy/Shear-Walls.git`

** Optional - create virtual environment `py -3.9 -m venv venv` `venv\Scripts\activate.bat` **

`pip install -r requirements.txt`

#### Step 2 - Create Master Input:
Label every shearwall that you want to design. Here is an example from one of my projects (this is the 'KEY' table in the shear_wall_input spreadsheet)
![image](https://user-images.githubusercontent.com/43247197/165406168-8493fc05-00da-466d-b383-82da99f46297.png)

Next, fill in the corrosponding cells in the data input tab of the excel spreadsheet (Greater Wall length is when two walls are basically in-line and are assumed to be acting as one wall)

![image](https://user-images.githubusercontent.com/43247197/165406377-b3325997-552c-4ceb-9e5a-2523ea832c02.png)

The X0, Y0, and Z0 values are the Revit coordinates of endPoint(0) for the 'Shear Wall Plan' detail component (dashed yellow line) that signifies a wall is a shear wall. These can be obtained from the [Revit Python Shell](https://github.com/architecture-building-systems/revitpythonshell) with `el.Location.Curve.GetEndPoint(0)` assuming that "el" is a selected shear wall.

#### Step 3 - Design Walls:
Run `python shear_walls.py --start "start_letter" --end "end_letter"` where start and end letter are the values in the A column of the spreadsheet. When you're dealing with over 200 unique wall designs, you don't always want to design them all every time. For example, `python shear_walls.py --start A --end BL` will run all wall designs labeled A-Z, AA-AZ, BA-BL and then stop. It will generate a shear_wall_output excel file that has all the design values you're interested in as shown below.

![image](https://user-images.githubusercontent.com/43247197/165408375-2dd91471-966f-4166-8bc5-27d8e403f06a.png)

#### Step 4 - Update Shear Wall Detail Components in Revit:
Assuming that the detail component has not moved, you can change thousand of shear wall labels to match your calcs in a matter of seconds. 
This is a bit hacky but it works. First, save the output file as a .txt file, then update the location of the shear_wall_output.txt file in the "utils.py" file. Lastly, copy the entire "utils.py" file into the Revit Python Shell. Run it ask your company for a 10% cut of the amount of money you just saved them. See below to illustrate this last step. (2 gifs because of the length of the video)

![revit_output_1](https://user-images.githubusercontent.com/43247197/165410864-de94f7b0-d867-4fa7-9f76-f1765e076323.gif)



![revit_output_2](https://user-images.githubusercontent.com/43247197/165411037-ca9ebd7d-4208-41d1-b2e0-8c4d35ef9e2b.gif)




