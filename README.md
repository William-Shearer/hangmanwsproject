# Capstone  
  
This project creates a deployable Hangman Challenge website using Python 3, the Django 4.2 framework, SQLite3 (via Django ORM) with three models, JavaScript, HTML, and CSS with Bootstrap5. It consitutes the submission for the final project (Capstone) for HarvardX's CS50W Web Programming online course, by student William Shearer, and was created July/August, 2023.  
  
This effectively complies with one of the project requirements, as stated in the specifications:  
  
- Your web application must utilize Django (including at least one model) on the back-end and JavaScript on the front-end.  
  
## The ethical question  
  
I want to get this out of the way as soon as possible. Granted, I have seen some online comments and articles that attempt to target Hangman as an inappropriate game. It is, after all, a simulation of an execution. However, I must clarify that I do not consider Hangman, in any way, inappropriate. There are currently more than enough (none the less enjoyable and entertaining, I add) video games in existence of which the objective is mindless destruction and massive subtraction of digitally represented life to justify the continued existence of this educational classic. Furthermore, the objective of Hangman is to save the condemned victim's life by getting the word right, not to deliberately get the word wrong so that the, let us assume, unfairly sentenced "man" is, indeed, hanged. I think I have made my point.  
  
## Overview  
  
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
  
## Motivation  
  
Why Hangman, particularly? And why do I consider this an appropriate submission for CS50W?  
  
The inspiration to create a web based, competitive Hangman application was born from a previous and much smaller scale project that I created with the object of practicing and improving my general Python 3 programming. Said project can be viewed [here](https://github.com/William-Shearer/HangManWS). Creating an interactive game utilizing Django seemed a logical next step.  
  
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
  
The Game page displays a visual representation of the gallows, a section that contains the buttons of the alphabet characters, and a section below that contains the required number of spaces (blanks represented as underlines) for the word to be guessed. The game implementation is very simple to understand; click on the desired letter and, if it is in the word, the corresponding blanks are filled. Once a letter has been clicked, the letter button will be disabled.  
  
The player is not obliged to finish a word once they start. They may quit out at any time, and even log out. The next time they play, the game will resume at the point they left off. If the player wins (gets the word with a maximum of six missed letters), they will get a message presenting their word score. The word score is based on how many letters were asserted over the total number of letters tried. The word score is only applicable if the user wins the round. 
  
The History page shows all the words the user has ever attempted, ordered from the most recent, descending. For this reason, the page is paginated, containing data for five words at a time. Detailed information of the player's performance in completing (or not) each word is displayed, which includes the the word score (if the player won) or how much of the word they completed (if they lost). Which letters were asserted and which were missed are also displayed, in the order they were played.
  
One of my personal objectives for this project was to explore the usage of external websites, via API calls, to supply data to an application. I wanted to try this both from the back end and the front end, with Python and JavaScript, respectively. For this reason, I implemented a pane that contains a definition of the word. The definition is obtained by a JavaScript fetch call to **[Free Dictionary API](https://dictionaryapi.dev/)**. Apart from satisfying my curiosity about the programming subject, this feature also adds some educational value to the application.