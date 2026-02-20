# AutoIcy
Automated Capstone IC tool

# What it is
Filling out an IC for every sprint is an annoying and time consuming process. This tool help you identify your contributions as well as automatically extracting the correct links and compiling everything in a format that can be paste directly into your IC form.

# Instructions
1. Get the data about your commits
 - In github select the commits page from your repo's home page
 - ![img_2.png](img_2.png)
 - filter out your other teammate's commits but selecting your username
 - ![img_3.png](img_3.png)
 - Save the page as html only.
   - It **MUST** be the only `.html` file in the same directory as `AutoIcy.py`
2. Get the data about your tasks
 - In Tiaga export your project info at settings > Project > Export 
 - Save it to your AutoIcy repo folder.
   - It **MUST** be the only `.json` file in the same directory as `AutoIcy.py`
 - ![img_1.png](img_1.png)
3. Run AutoIcy
 - The commits and tasks will load automatically
 - Filter out tasks done by others by clicking the `Filter tasks` button and entering the email address used as your taiga username
5. Join Tasks with commits
 - Select the task name on the left
 - Select the matching commit on the right
 - Push `Join Task with Commit` to create an entry in your contributions listbox on the bottom of the screen.
 - Repeat Step 5 until you have identified all your contributions for this IC
6. Export your IC data
 - Push `Export to CSV`
 - Open *export.csv* in your spreadsheet program
 - Copy the first block into columns A & B of your IC report. This is you task link and task number.
 - Copy the second block into columns E & F of your IC report. This is your github commit link and the date it was committed.
 - Manually fill in columns C (complete?), D (coding task?), and G (% of work committed)
7. Check it over
