const alphabet = "abcdefghijklmnopqrstuvwxyz".split("");


document.addEventListener("DOMContentLoaded",
    function()
    {
        fGameInitiate();
    }
);


async function fGameInitiate()
{
    /* 
    The game loop start by getting the word with fetch from Django.
    Go look at fetchword for this process. 
    This is for the timeOut signal processing.
    */
    const controller = new AbortController();
    const url = "fetchword";
    // The timeOut function. If this fails, the game fails...
    const timeOut = setTimeout(
        function ()
        {
            controller.abort();
        },
        7000 // Seven seconds maxed out.
    );

    try
    {
        const response = await fetch(url,
            {
                method: "GET",
                signal: controller.signal
            }
        );
        if (response.ok)
        {
            /* 
            Here the program gets the word and data back.
            What should come back: the user ID, the username, and the word.
            I'm calling the receive variable much the same name as that sent from Django
            so that I don't stupidly confuse myself later... data_word, dataWord.
            */
            const dataWord = await response.json();
            /* 
            Test word debug.
            document.querySelector("h1").innerText = dataWord.word.join(" ");
            */
            const userId = dataWord.userId;
            const userName = dataWord.userName;
            const word = dataWord.word;
            // let hits = 0;
            // let misses = 0;
            // Debug test them.
            // console.log(userId, userName, word.join(""));

            // This is the blank word. It is not a const on purpose, as it will be altered.
            let playerWord = Array(dataWord.word.length).fill("_");

            // The game can now start...
            fGameLoop(word, playerWord, userId, userName); //, hits, misses);
            
        }
        else
        {
            console.log(`RESPONSE ERROR: ${response.status}`)
        };
    }
    catch (error)
    {
        console.log(`NETWORK ERROR: ${error}`);
    }
    finally
    {
        clearTimeout(timeOut);
    };
};

/*
Take note: The application must be protected against the user reloading the browser.
That means up in the DOMContentLoaded, the word should be fetched from the Django model,
if it is incomplete. Else, a new word should be generated. This will have the effect
of saving a session, too. If the player leaves the game before finishing a word, when
they come back the same word will be presented for them to resume and complete.
*/

function fGameLoop(word, pWord, uid, uName) //, h, m)
{
    fDisplayPlayerWord(pWord);
    let h = 0;
    let m = 0;
    const btnFrame = document.querySelector(".btnFrame");
    alphabet.forEach(
        function(letter)
        {
            const btn = document.createElement("button");
            btn.style.width = "35px";
            btn.style.fontweight = "bold";
            btn.style.fontSize = "25px";
            btn.style.margin = "5px";
            const btnText = document.createTextNode(letter);
            btn.addEventListener("click",
                function ()
                {
                    if (fCheckLetter(this, letter, word, pWord))
                    {
                        h++;
                        /* 
                        A fetch put must go here...
                        It should PUT the player word and increase the hits in the Django History model.
                        */

                    }
                    else
                    {
                        m++;
                        /* A fetch put must go here...
                        It should PUT a miss in the Django History model.
                        */
                    };
                    // Game screen updates go here...
                    console.log(word.join(""), pWord.join(" "), letter, h, m);
                    fDisplayPlayerWord(pWord);
                    if (fCheckWordComplete(pWord))
                    {
                        const WinFrame = document.querySelector("h1");
                        WinFrame.innerHTML = "WON!";
                    };
                }
            );
            btn.appendChild(btnText);
            btnFrame.appendChild(btn);
        }
    );
};


function fCheckLetter(btn, letter, word, pWord)
{
    // Ghost the button and disable it. Letter is used.
    btn.style.fontWeight = "normal";
    btn.disabled = true;
    let contains = false;
    // Search through the word to find out if the letters in it match.
    for (let i = 0; i < word.length; i++)
    {
        if (word[i] === letter)
        {
            // That is, the word contains the letter, and it is placed into the playerWord,
            // at the appropriate place.
            pWord[i] = letter;
            contains = true;
        };
        // Otherwise, nothing changes. Now, the reason the above conditional does NOT break
        // out and return a true immediately it finds a letter is because that letter might happen
        // more than once in a word.
        // There is no need to worry about clicking a letter (validly) twice because the button is
        // disabled for already clicked letters, as seen above.
        // That has to be catered for, also, in the DOMContentLoaded bit up there.
    };
    // When all the places are checked, return true or false, as corresponds contains variable.
    // console.log(fCheckWordComplete(pWord)); // Ha-haaa! Works...
    return contains;
};


function fCheckWordComplete(pWord)
{
    // Hehe. Exapnded so I know what the devil is going on.
    // That ES6 hash rocket is so damned confusing!
    
    return pWord.every(
        function (c)
        {
            return c != "_";
        }
    );
    
    // This is what it would look like...
    // return pWord.every(c => c != "_");
    // I don't find that easier to read. Old school / old guy.
    // I will take my own time getting used to that. Here is the reference, anyhows.
    
};


function fDisplayPlayerWord(pWord)
{
    const pWordFrame = document.querySelector(".pWordFrame");
    let pWordString = pWord.join(" ");
    // let pWordText = document.createTextNode(pWordString);
    pWordFrame.innerHTML = `<h2>${pWordString}</h2>`;
};