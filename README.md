# Capstone  
  
This project creates a deployable Hangman Challenge website using Python 3, the Django 4.2 framework, SQLite3 (via Django ORM) with three models, JavaScript, HTML, and CSS with Bootstrap5. It consitutes the submission for the final project (Capstone) for HarvardX's CS50W Web Programming online course, by student William Shearer, and was created July/August, 2023.  
  
This effectively complies with one of the project requirements, as stated in the specifications:  
  
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.  
  
### Video link  
  
The presentation video for the project can be viewed at this link: [Presentation Video](https://youtu.be/wNMjHQgKS6o)  
  
### Live demo
  
The demonstration of the application itself can be played here: [Deployed application](https://cygonparrot.pythonanywhere.com)
  
## The ethical question  
  
I want to get this point out of the way as soon as possible. Granted, I have seen some online comments and articles that attempt to target Hangman as an inappropriate game. It is, after all, a simulation of an execution. However, I must clarify that I do not consider Hangman, in any way, inappropriate. There are currently more than enough (none the less enjoyable and entertaining, I add) video games in existence of which the objective is mindless destruction and massive subtraction of digitally represented life to justify the continued existence of this educational classic. Furthermore, the objective of Hangman is to save the condemned victim's life by getting the word right, not to deliberately get the word wrong so that the, let us assume, unfairly sentenced "man" is, indeed, hanged. I think I have made my point.  
  
## Distinctiveness and Complexity  
  
### Overview  
  
Hangman is an ubiquitous game often played by youngsters and adults alike because it adds some entertainment value to the exercise of expanding vocabulary. It is frequently played with a dictionary on hand, both so that challengers can find unusual words to test the players, and also to check the existence, or validity, of words.  
  
This rendition of Hangman attempts to enrich the experience of the game by adding a competetive element, while at the same time it utilizes web technology to automate some of the processes. Some of the features will be summarized in the following list:  
  
- Players are required to log in so that their score and history are maintained persistently.
- Primary word selection utilizes a free third party word generation API to obtain words randomly.
- Backup systems are implemented to word selection to cover the event of external API failure.
- Repetition of words is controlled.
- Censoring of inappropriate language is implemented, as far as possible.
- A scoring system is implemented, including levels, so that players can compete fairly.
- The game utilizes buttons for selecting letters so that use of the keyboard is eliminated.
- The button letters also make the game conveniently mobile device playable.
- A graphic representation of the hanged man is presented in order that progress be visualized.
- A historical record of all words attempted by players is maintained.
- The historic data for each player can be viewed.
- To add some educational value, the history view adds a definition for the word from another third party API.
  
### Motivation  
  
Why Hangman, particularly? And why do I consider this an appropriate submission for CS50W?  
  
The inspiration to create a web based, competitive Hangman application was born from a previous and much smaller scale project that I created with the object of practicing and improving my general Python 3 programming. Said project can be viewed **[here](https://github.com/William-Shearer/HangManWS)**. Creating an interactive game utilizing Django seemed a logical next step.  
  
I consider this a suitable submission for the final project, primarily, based on these terms of the project specifications, which state:  
  
- Your web application must be sufficiently distinct from the other projects in this course (and, in addition, may not be based on the old CS50W Pizza project), and more complex than those.  
  
- A project that appears to be a social network is a priori deemed by the staff to be indistinct from Project 4, and should not be submitted; it will be rejected.  
  
- A project that appears to be an e-commerce site is strongly suspected to be indistinct from Project 2, and your README.md file should be very clear as to why it’s not. Failing that, it should not be submitted; it will be rejected.  
  
In creating an online game application, I am creating something completely unrelated to previous coursework. This project aims to be highly interactive and contains varied programming challenges that are very different from eCommerce and social media platforms. Therefore, I do not need to entertain explanations of what I think sets this project apart from the previous coursework subjects.  
  
By so doing there are some trade offs, as far as programming for the web is concerned, in the complexity of the work required. Some objective requirements are considerably simpler than those encountered in the coursework. For example, in this project there is little need for posting composite URLs to the Django views, singling out specific posts, creating edit boxes, like buttons, following users, sorting price ranges of products, and determining when products are no longer available. These subjects have already been covered, and the conclusions drawn from the lessons have been absorbed, thanks to the coursework.  
  
The complexity of this project lies in the "nuts and bolts" implementations behind the scenes, mostly accomplished with some more advanced Python 3 programming techniques, that enable words to be selected and filtered, as outlined above in the list of features, and then visually presented to the player in the form of a game. Also, the focus is on a persistent and interactive gameplay experience, which permits a player to sign out and return to the game at a later date where they left off, something for which the features of the Django/SQLite3 ORM interface and the JavaScript fetching of internal and external resources proved invaluable.  
  
## The AI dilemma  
  
There is another point of some contemporary controversy that I wish to issue some assurance on, regarding the current "threat" Artificial Intelligence poses to effective, hands on learning. I would be pleased to guarantee that in the creation of this project, absolutely no active assistive AI resources were utilized to generate code, solve coding problems, offer formatting or content assistance, or any other form of intervention that might have supplemented my work and interfered with the process of the acquisition of skills and knowledge. Furthermore, I am positive that upon reviewing the code there will be little doubt that AI was not used.
  
Stated here in writing. For the record.  
  
## The Hangman application  
  
### Front end
  
The application is composed of six main pages.  
  
- Home page, with a logged in and logged out representation.
- Game page, accessible only if logged in.
- History page, accessible only if logged in.
- Log in page, accessible only if logged out.
- Registration page, accessible only if logged out.
- Change password page, accessible only if logged in.
  
The application has been designed, with the features of Bootstrap5 and CSS, to be responsive on mobile devices, in accordance with the specifications, as follows:  
  
- Your web application must be mobile-responsive.  
  
The screen layout for the Home page and the Game page will shift from columns to rows on narrow screens, and some text will vary in size at different breakpoints, in order to maintain readability.   

All the pages have a navbar along the top that contains hyperlinks to the different application pages or functions. The navbar changes its options depending on whether the player is logged in or not (logged in player options are suppressed if logged out).  
  
From the Home page, a logged in user may additionally view a modal window that explains the scoring system. The Home page contains an introduction / welcome text if logged out. If logged in, it displays summary of the players performance, a button to begin playing the game, and a hyperlink to the History page. Regardless of whether the user is logged in or not, a Leaderboard is visible. This leaderboard is divided into the five levels of attainment that the game employs, and displays the first three places of each level category. More information on scoring is included later in this text.  
  
The Game page displays a visual representation of the gallows, a section that contains the buttons of the alphabet characters, and a section below that contains the required number of spaces (blanks represented as underlines) for the word to be guessed. The visual representation was implemented using HTML canvas, controlled via JavaScript. This is an area I have some limited previous experience with, and therefore did not go overboard with it. In any case, the rough and simple graphics are ideally suited to the game, as it is usually played on a piece of paper or a chalkboard, hand drawn. The game implementation is very simple to understand; click on the desired letter and, if it is in the word, the corresponding blanks are filled. Once a letter has been clicked, the applicable letter button will be disabled to avoid repeat, wasted guesses.  
  
The player is not obliged to finish a word once they start. They may quit out at any time, and even log out. The next time they play, the game will resume at the point they left off. If the player wins (gets the word with a maximum of six missed letters), they will get a message presenting their word score. The word score is based on how many letters were asserted over the total number of letters tried. The word score is only applicable if the user wins the round. 
  
All the JavaScript code that controls the game is located in the game.js file, in the static directory. It includes a couple of fetch asynchronous functions to trigger the back end functions to either provide or store game progress in the models.  
    
The History page shows all the words the user has ever attempted, ordered from the most recent, descending. For this reason, the page is paginated, containing data for five words at a time. Detailed information of the player's performance in completing (or not) each word is displayed, which includes the the word score (if the player won) or how much of the word they completed (if they lost). Which letters were asserted and which were missed are also displayed, in the order they were played.  
  
One of my personal objectives for this project was to explore the usage of external websites, via API calls, to supply data to an application. I wanted to try this both from the back end and the front end, with Python and JavaScript, respectively. For this reason, I implemented a pane that contains a definition of the word. The definition is obtained by a JavaScript fetch call to **[Free Dictionary API](https://dictionaryapi.dev/)**. Apart from satisfying my curiosity about the programming subject, this feature also adds some educational value to the application.  
  
The JavaScript code that controls the access to the third party site and processes the responses is located in the dictionary.js file, in the static directory.  
  
The Register, Login, and Change password pages can assumed to be fairly self explanatory and familiar enough to everyone to not warrant an expanded explanation. Suffice to say, they are there.  
  
### Back end  
  
Most of the time invested in this project was spent developing the back end with Python 3. As already mentioned, there was ample opportunity to explore gameplay control with the language. Python proved to be more than up to providing solutions to the problems, and certainly extended and reinforced my own understanding.  
  
Many of the functions required to enable the game play were large, and were moved to a separate functions.py file in the Django application directory structure. This avoided cluttering the views.py file and enhances code readability.  
  
The most important part of the back end, as far as the game is concerned, is the remote selection of words to present to the player. As with the History page on the front end, I wanted to explore the possibility of using a third party, free random word generation API. For this purpose, I used the **[random-word-api](https://random-word-api.vercel.app/)**. This entailed utilizing the Python [requests](https://pypi.org/project/requests/) module in the project. This API is the primary source for words to be used in the game.  
  
Consideration was also given to the fact that, using an external API to provide words, some inappropriate language might sneak in every so often. Therefore, a filter was implemented. Several text lists of words to be excluded can be found with a search, and I used one of these as a template in the filter.  
  
Following this, failure of the external API was also considered, and some error trapping was implemented for this event. In fact, two alternate methods for word selection were incorporated. The first uses a text file of over 1,000 words, bundled in with the back end and stored in the wordbank directory. It is accessed by the program after being loaded from this location. If this file is missing, or is damaged, a last, hard coded list of words is included in the functions.py file.  
  
## File summary  
  
The following files have been created and/or modified to enable the functionailty of this application:
  
### Project level:
  
- settings.py: Various configurations for included supporting apps, directories, and deployment options.
- urls.py: Preliminary configuration of routes for admin and application.
- requirements.txt: Python pacjages used during the development of the application.
- LICENSE: MIT license standard from GitHub.
- README.md: This file.
  
### Application level:
  
At the application level, 
  
- admin.py: Registration of models to be accessible on the Django Admin page.
- forms.py: Created file, includes the forms for log in, registration and change password.
- functions.py: An important file created for the application. Contains all the external API and local word search, selection, and filtering functions used by the application, as well as the score formatting for the leaderboard and word saving/sorting routines.
- models: Contains the three models utilized by the application to save users, maintain user word histories, and store player's scores persistently.
- urls.py: Contains all the routes needed to allow the application to function.
- views.py: Contains all the views needed by the application to enable functionality on server. A limited amount of calculations are performed in some of the functions, but most important functions are imported from functions.py.
  
Additionally, three directories were created at application level:
  
- static: The static directory contains a sub directory for the application (according to Django best practices), which in turn contains the following files:
  
    - Four SVG graphics of arrows, downloaded from Bootstrap, used to enhance the appearance of the pagination buttons on the History page of the application.
    - One favicon.png, created with paint.net.
    - game.js: The main JavaScript file of the application. The code that runs the hangman game is in this file, and performs word formatting, canvas drawing routines, letter button enabling and disabling, and fetch operations that save and update the data base during gameplay.
    - dictionary.js: This JavaScript file is associated with the History page of the application and performs the calls to the external API with fetch, and formats the results for display on screen.
    - gamestyles.css: Additional CSS style definitions and customizations that could not be handled by Bootstrap are included in this file.

- templates: The directory that contains the sub directory for the application, which in turn contains the HTML templates:
  
    - changepwd.html: The Change Password page. Displays the Change Password Form.
    - game.html: The application Game page. Specifically, imports game.js for functionality of the game.
    - history.html: The player word History page. Imports dictionary.js for functionality of the word definitions.
    - home.html: The opening page of the application, where the leaderboard is displayed.
    - layout.html: The basic starting point format for all the pages. Includes the navbar.
    - login.html: The log in page for the application. Displays the Log In Form.
    - register.html: The new user registration page. Displays the Register Form.
  
- wordbank: The directory contains text files that are loaded by the Python back end.
  
    - censor.txt: Used by one of the word filtering functions in functions.py. It contains a list of inappropriate language that the program matches to words obtained from the external API, and filters the words out if they coincide. WARNING: This file contains a list of VERY offensive words. Do not open and read it if you are a sensitive and easily perturbed individual.
    - nouns_en.txt: A list of over 1,000 words in English that serve as a backup to provide game words in the event of a failure of the external random word generator API. 
  
## Conclusion  
  
There is little more to say regarding the application. The code itself is extensively commented, mostly for my own reference. However, it may prove of some value during the evaluation process.  
  
One additional point that I clarified during this project was Django's pagination functionality. Indeed, it was utilized in the last project, but understanding of it was superficial, at best. I delved deeper into its inner workings on this project, and am satisfied that my understanding of it is nearer to being complete than it was at the outset.  
  
Thank you for your kind attention.  
  
William Shearer, Quito, Ecuador, August 2023  
  
