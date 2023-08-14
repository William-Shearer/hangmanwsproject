const alphabet = "abcdefghijklmnopqrstuvwxyz".split("");

document.addEventListener("DOMContentLoaded",
    async function()
    {
        let wObj = await fGameInitiate();
        if (wObj === false)
        {
            console.log("FAILED");
        }
        else
        {
            console.log("SUCCEEDED");
            console.log(`Word is: ${wObj.word}`);
            fGameLoop(wObj);
        };
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
            return dataWord;
        }
        else
        {
            console.log(`RESPONSE ERROR: ${response.status}`);
            return false;
        };
    }
    catch (error)
    {
        console.log(`NETWORK ERROR: ${error.name}`);
        return false;
    }
    finally
    {
        clearTimeout(timeOut);
    };
    
};

function fGameLoop(wObj)
{
    fDisplayPlayerWord(wObj);
    fDrawCanvas(wObj.misses);
    // console.log(`In Game Loop with word: ${wObj.word}`);
    const btnFrame = document.querySelector("#btnFrame");
    alphabet.forEach(
        function(letter)
        {
            const btn = document.createElement("button");
            btn.style.width = "35px";
            btn.style.color = "blue";
            // btn.style.fontweight = "bold";
            btn.style.fontSize = "25px";
            btn.style.margin = "5px";
            btn.style.background = "rgb(139,211,230)";
            btn.setAttribute("name", "letterButton");
            if (wObj.usedLetters.includes(letter))
            {
                fButtonDisabled(btn);
            };
            const btnText = document.createTextNode(letter);
            btn.addEventListener("click",
                function ()
                {
                    fCheckLetter(this, letter, wObj) ? wObj.hits++ : wObj.misses++;

                    if (fCheckWon(wObj))
                    {
                        // The player got yhe word (true)
                        fEndRound(wObj, true);
                    }
                    else if (wObj.misses == 6)
                    {
                        // The plater ran out of tries (false)
                        fEndRound(wObj, false);
                    };

                    fPutWordHistory(wObj);
                    fDisplayPlayerWord(wObj);
                    fDrawCanvas(wObj.misses);
                }
            );
            btn.appendChild(btnText);
            btnFrame.appendChild(btn);
        }
    );
};


function fButtonDisabled(btn)
{
    // btn.style.fontWeight = "normal";
    btn.style.color = "rgb(120,190,190)";
    btn.style.background = "rgb(160,230,230)";
    btn.disabled = true;
};

function fDisableAllButtons()
{
    const buttons = document.querySelectorAll('button[name="letterButton"]');
    for (let i = 0; i < buttons.length; i++)
    {
        // buttons[i].style.fontWeight = "normal";
        buttons[i].style.color = "rgb(120,190,190)";
        buttons[i].style.background = "rgb(160,230,230)";
        buttons[i].disabled = true;
    };
};

function fCheckLetter(btn, letter, wObj)
{
    fButtonDisabled(btn);
    let contains = false;
    let word = wObj.word.split("");
    let pWord = wObj.playerWord.split("");
    for (let i = 0; i < word.length; i++)
    {
        if (word[i] === letter)
        {
            pWord[i] = letter;
            contains = true;
        };
    };
    const savedLetters = wObj.usedLetters + letter;
    wObj.usedLetters = savedLetters;
    console.log(wObj.usedLetters);
    wObj.playerWord = pWord.join("");
    return contains;
};

// This returns true if the word contains no blanks (ie; won).
function fCheckWon(wObj)
{
    let pWord = wObj.playerWord.split("");
    return pWord.every(c => c != "_");
    /*
    // Expanded, so I know what it is going up there.
    // I did it this way first, then rewrote in arrow format, which is confusing the heck out of me.
    return pWord.every(
        function (c)
        {
            return c != "_";
        }
    );
    */
};

function fEndRound(wObj, won)
{
    // const WinFrame = document.querySelector("h1");
    if (won)
    {
        // WinFrame.innerHTML = "WON!";
        wObj.won = true;
    }
    else
    {
        // WinFrame.innerHTML = "LOST!";
    };
    wObj.complete = true;
    fDisableAllButtons();
};


function fDisplayPlayerWord(wObj)
{
    console.log(wObj.playerWord);
    const pWordFrame = document.querySelector("#pWordFrame");
    pWordFrame.innerHTML = "";
    const pWordString = wObj.playerWord.split("").join(" ");
    pWordFrame.innerHTML = pWordString;
    // const pWordText = document.createTextNode(pWordString);
    // const pWordElement = document.createElement("h1");
    // pWordElement.appendChild(pWordText);
    // pWordFrame.appendChild(pWordElement);
};


async function fPutWordHistory(wObj)
{
    const controller = new AbortController();
    const url = "puthistory";
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


function fDrawCanvas(misses)
{
    console.log("Drawing canvas");
    const canvas = document.querySelector("#gameCanvas");
    const cWidth = canvas.scrollWidth;
    const cHeight = canvas.scrollHeight;
    console.log(`Canvas W H: ${cWidth}, ${cHeight}`);
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, cWidth, cHeight);
    // ctx.fillStyle = "rgb(250, 235, 215)";
    ctx.strokeStyle = "black";
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.moveTo(10, 310);
    ctx.lineTo(10, 10);
    ctx.lineTo(145, 10);
    ctx.lineTo(145, 15);
    ctx.lineTo(50, 15);
    ctx.lineTo(15, 50);
    ctx.lineTo(15, 310);
    ctx.moveTo(14, 15);
    ctx.lineTo(43, 15);
    ctx.lineTo(15,43);
    ctx.lineTo(15, 14);
    ctx.moveTo(135, 15);
    ctx.lineTo(135, 40);
    ctx.moveTo(2, 310);
    ctx.lineTo(230, 310);
    ctx.stroke();
    
    switch(misses)
    {
        case 6:
            ctx.beginPath();
            ctx.moveTo(135, 180);
            ctx.lineTo(173, 295);
            ctx.stroke();
        case 5:
            ctx.beginPath();
            ctx.moveTo(135, 180);
            ctx.lineTo(97, 295);
            ctx.stroke();
        case 4:
            ctx.beginPath();
            ctx.moveTo(135, 100);
            ctx.lineTo(186, 170);
            ctx.stroke();
        case 3:
            ctx.beginPath();
            ctx.moveTo(135, 100);
            ctx.lineTo(89, 170);
            ctx.stroke();
        case 2:
            ctx.beginPath();
            ctx.moveTo(135, 90);
            ctx.lineTo(135, 180);
            ctx.stroke();
        case 1:
            ctx.beginPath();
            ctx.arc(135, 65, 25, 0, Math.PI * 2);
            ctx.stroke();
            if (misses < 6)
            { 
                ctx.strokeRect(124, 58, 2, 2);
                ctx.strokeRect(145, 58, 2, 2);
                ctx.beginPath();
                ctx.moveTo(123, 78);
                ctx.lineTo(147, 78);
                ctx.stroke();
            }
            else
            {
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(120, 54);
                ctx.lineTo(128, 62)
                ctx.moveTo(120, 62);
                ctx.lineTo(128, 54);
                ctx.moveTo(141, 54);
                ctx.lineTo(150, 62);
                ctx.moveTo(141, 62);
                ctx.lineTo(150, 54);
                ctx.stroke();
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(129, 78, 6, Math.PI, 0);
                ctx.arc(141, 78, 6, Math.PI, 0, true);
                ctx.stroke();
            }
            break;

        default:
            break;
    };
};