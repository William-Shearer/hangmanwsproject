const alphabet = "abcdefghijklmnopqrstuvwxyz".split("");


document.addEventListener("DOMContentLoaded",
    function()
    {
        fGameInitiate();
    }
);


async function fGameInitiate()
{
    const controller = new AbortController();
    const url = "fetchword";
    const timeOut = setTimeout(
        function ()
        {
            controller.abort();
        },
        7000
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
            console.log(response.status);
            const dataWord = await response.json();
            fGameLoop(dataWord);
        }
        else
        {
            console.log(`RESPONSE ERROR: ${response.status}`);
        };
    }
    catch (error)
    {
        console.log(`NETWORK ERROR: ${error.name}`);
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


// function fGameLoop(word, pWord, uid, uName) //, h, m)
function fGameLoop(wObj)
{
    fDisplayPlayerWord(wObj);
    console.log(`In Game Loop with word: ${wObj.word}`);
    const btnFrame = document.querySelector(".btnFrame");
    alphabet.forEach(
        function(letter)
        {
            const btn = document.createElement("button");
            btn.style.width = "35px";
            btn.style.fontweight = "bold";
            btn.style.fontSize = "25px";
            btn.style.margin = "5px";
            if (wObj.usedLetters.includes(letter))
            {
                btn.style.backgroundColor = "red";
            };
            const btnText = document.createTextNode(letter);
            btn.addEventListener("click",
                function ()
                {
                    // Ternary operator a la JavaScript, don't get confused!
                    // This will alter the pWord if there are hits, incidentally.
                    fCheckLetter(this, letter, wObj) ? wObj.hits++ : wObj.misses++;
                    console.log(`Hits: ${wObj.hits}`);
                    console.log(`Missess: ${wObj.misses}`);

                    if (fCheckWordComplete(wObj))
                    {
                        const WinFrame = document.querySelector("h1");
                        WinFrame.innerHTML = "WON!";
                        wObj.complete = true;
                    };

                    console.log(`Is word complete? ${wObj.complete}`);

                    // Object to pass to Django.
                    // Make an object to pass...
                    // const dataObject = {playerWord : pWord.join(""), misses: m, hits: h,};
                    // Don't forget, playerWord must yet be converted to a string. DONE.
                    fPutWordHistory(wObj, wObj.id);

                    // Game screen updates go here...
                    // console.log(word.join(""), pWord.join(" "), letter, h, m);
                    fDisplayPlayerWord(wObj);
                    /*
                    This is the win conditon.
                    fCheckWordComplete is a function that returns true if all
                    the blanks of pWord are filled.
                    At this point, the application should also provide an option to
                    play again or leave.
                    */
                   
                    
                   
                    // console.log(fCheckWordComplete(wObj));
                }
            );
            // Make the buttons here.
            btn.appendChild(btnText);
            btnFrame.appendChild(btn);
        }
    );
};


function fButtonDisabled()
{

};


function fCheckLetter(btn, letter, wObj)
{
    // Ghost the button and disable it. Letter is used.
    btn.style.fontWeight = "normal";
    btn.disabled = true;
    let contains = false;
    // Search through the word to find out if the letters in it match.
    // Local variable of word and pWord, broken up into array...
    let word = wObj.word.split("");
    let pWord = wObj.playerWord.split("");
    // console.log(typeof letter);
    console.log(typeof wObj.usedLetters);
    console.log(letter);
    // console.log(alphabet);
    for (let i = 0; i < word.length; i++)
    {
        if (word[i] === letter)
        {
            // That is, the word contains the letter, and it is placed into the playerWord,
            // at the appropriate place.
            pWord[i] = letter;
            contains = true;
            // console.log(`Contains ${letter}`);
        };
        // Otherwise, nothing changes. Now, the reason the above conditional does NOT break
        // out and return a true immediately it finds a letter is because that letter might happen
        // more than once in a word.
        // There is no need to worry about clicking a letter (validly) twice because the button is
        // disabled for already clicked letters, as seen above.
        // That has to be catered for, also, in the DOMContentLoaded bit up there.
    };
    // Save the used letter to the string of wObj.usedLetters
    const savedLetters = wObj.usedLetters + letter;
    wObj.usedLetters = savedLetters;
    console.log(wObj.usedLetters);
    
    /* When all the places are checked, merge the playerWord back into a string and
    assing it back to the object (which is here, present, and can be changed by reference).
    Then return true or false, as corresponds contains variable.
    */
    wObj.playerWord = pWord.join("");
    // console.log(fCheckWordComplete(pWord)); // Ha-haaa! Works...
    return contains;
    // That is, true or false.
};


function fCheckWordComplete(wObj)
{
    // Okay, same story of breaking the pWord into an array...
    let pWord = wObj.playerWord.split("");
    // Hehe. Exapnded so I know what the devil is going on.
    // That ES6 hash rocket is so damned confusing!
    // console.log(`In Check Word Complete ${pWord}`);

    return pWord.every(
        function (c)
        {
            return c != "_";
        }
    );
    
    /*
    This is what it would look like...
    return pWord.every(c => c != "_");
    I don't find that easier to read. Old school / old guy.
    I will take my own time getting used to that. Here is the reference, anyhows.
    But what is it doing?
    This function returns true if every characteer (c) in pWord is NOT "_".
    Otherwise, it returns false (meaning, there is still a blank in pWord).
    */
};


function fDisplayPlayerWord(wObj)
{
    console.log(wObj.playerWord);
    const pWordFrame = document.querySelector(".pWordFrame");
    pWordFrame.innerHTML = "";
    const pWordString = wObj.playerWord.split("").join(" ");
    const pWordText = document.createTextNode(pWordString);
    const pWordElement = document.createElement("h1");
    pWordElement.appendChild(pWordText);
    pWordFrame.appendChild(pWordElement);
};


async function fPutWordHistory(wObj, word_id)
{
    const controller = new AbortController();
    const url = "puthistory/" + word_id;
    console.log(url);
    const timeOut = setTimeout(
        function ()
        {
            controller.abort();
        },
        7000
    );

    try
    {
        const response = await fetch(url,
            {
                method: "PUT",
                body: JSON.stringify(wObj), // No need to use await here.
                singal: controller.signal
            }
        );

        if (response.ok)
        {
            console.log("Edited");
        }
        else
        {
            console.log(`RESPONSE ERROR: ${response.status}`)
        };
    }
    catch (error)
    {
        console.log(`NETWORK ERROR: ${error.name}`);
    }
    finally
    {
        clearTimeout(timeOut);
    };
};
