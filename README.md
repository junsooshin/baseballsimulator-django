# Baseball Game Simulator in Django

**Run 500 simulations between two lineups and estimate the winning percentages.**

[Try the simulator at the Heroku app](https://baseballsimulator.herokuapp.com).

Name: Junsoo Derek Shin

Date: 26 February 2018

## Note:

- This is an extension project from [the one I wrote before](https://github.com/junsooshin/baseballsimulator). 
  Almost the same code from the previous project was used for the file that 
  runs the simulations.

- The main focus for this project was to learn Django and speed up the 
  simulator by storing data in the database.

## Using the simulator:

- Type in the player names for both lineups. The names have to be capitalized and
  exist in the FanGraphs database. If the names don't exactly match, the warning
  messages will show up at the top of the page, specifying which player's name
  was misspelled.

- The webpage takes about 15 seconds to load only at first and about 5 seconds
  to run the simulations.

## Data sources:

- 2017 Batting (2017FanGraphsBatting.csv)
	
	<http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=0&season=2017&month=0&season1=2017&ind=0&team=0&rost=0&age=0&filter=&players=0>

- 2017 Pitching (2017FanGraphsPitching.csv)
	
	<http://www.fangraphs.com/leaderssplits.aspx?splitArr=&strgroup=season&statgroup=1&startDate=2017-3-1&endDate=2017-10-1&filter=IP%7Cgt%7C0&position=P&statType=player&autoPt=true&sort=19,-1&pg=0>

- 2017 League (2017FanGraphsLeague.csv)
	
	<http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=0&season=2017&month=0&season1=2017&ind=0&team=0,ss&rost=0&age=0&filter=&players=0>

- 2017 Play-by-play and Retrosheet BEVENT software
	
	<http://www.retrosheet.org/game.htm>
	<http://www.retrosheet.org/tools.htm>
	<http://www.retrosheet.org/datause.txt>

## Sources:

- Overall guide and inspiration

   <http://www.hardballtimes.com/10-lessons-i-learned-from-creating-a-baseball-simulator/>

- The Odds Ratio Method

   <http://www.insidethebook.com/ee/index.php/site/comments/the_odds_ratio_method/>

- Help on Django (This is mainly for me to look back on later)
	
   [Django Tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
   
   [Django Crash Course YouTube Video](https://www.youtube.com/watch?v=D6esTdOLXh4)
   
   [Virtualenv Documentation](https://virtualenv.pypa.io/en/stable/userguide/)

   
   [How to activate virtual environment](https://stackoverflow.com/questions/46896093/how-to-activate-virtual-environment-from-windows-10-command-prompt)
   
   [Setting django up to use mysql](https://stackoverflow.com/questions/19189813/setting-django-up-to-use-mysql)
   
   [Trying to run django script as standalone models error](https://stackoverflow.com/questions/34757353/trying-to-run-django-script-as-standalone-models-error)
   
   [Django revert last migration](https://stackoverflow.com/questions/32123477/django-revert-last-migration)
   
   [How to reset migrations in django 1.7](https://stackoverflow.com/questions/29253399/how-to-reset-migrations-in-django-1-7)
   
   [How to use external python script in django views](https://stackoverflow.com/questions/44759589/how-to-use-external-python-script-in-django-views)

   [How to style django forms with bootstrap](https://www.techinfected.net/2016/11/style-django-forms-with-bootstrap.html)
   
   [BootStrap forms](https://getbootstrap.com/docs/4.0/components/forms/#form-grid)
   
   [Django set field value after a form is initialized](https://stackoverflow.com/questions/813418/django-set-field-value-after-a-form-is-initialized)


   [Deploying Django to production](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment)
   
   [Deploying Django on Heroku](https://devcenter.heroku.com/articles/django-app-configuration)
   
   [getting started with postgresql on mac osx](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)


- Help on Python and Pandas (For future references as well)
   
   [Import error no module named pandas indexes](https://stackoverflow.com/questions/37371451/importerror-no-module-named-pandas-indexes)
   
   [Combine multiple text files into one text file using python](https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python)
   
   [How to get full path of current files directory in python](https://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python)
   
   [Pandas dataframe performance](https://stackoverflow.com/questions/22084338/pandas-dataframe-performance)
   
   [How to store a dataframe using pandas](https://stackoverflow.com/questions/17098654/how-to-store-a-dataframe-using-pandas)
   
   [What is pickle in python](https://pythontips.com/2013/08/02/what-is-pickle-in-python/)
   
   [Guide to python profiling cprofile concrete case](https://julien.danjou.info/guide-to-python-profiling-cprofile-concrete-case-carbonara/)

## Things to be implemented in the future:

- There are a lot of things to be implemented to refine the baseball simualtor
  itself, including pitcher management, using multiple season data, and using
  projection data to list a few.

- To test how well this simulator simulates baseball matches, I will run the
  matches from the 2017 season using the 2017 data and see if the results 
  match well.

