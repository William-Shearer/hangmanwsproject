// Hmmmm. How the heck do I do this, now?
document.addEventListener("DOMContentLoaded",
    function (event)
    {
        /*
        What needs to happen here? Objective, in other words...
        When the page has finished loading, get all the history frames on the page.
        Send the frame, in turn (forEach), to the fGetDefinitions function.
        fGetDefinitions, it turn, will call a fetch to retrieve definitions from
        an online dictionary API (look in fetch, it is there).
        When the fetch returns data, the fGetDefinition function will build a string
        from the data and insert it into the textarea. 
        */
        event.preventDefault();
        const recordFrames = document.querySelectorAll("[name='recordFrame']");
                
        recordFrames.forEach(
            function(frame)
            {
                fGetDefinitions(frame);                    
            }
        );
    }
);


async function fGetDefinitions(frame)
{
    /*
    Here, the function is now dealing with the single frame that was sent to it.
    First, the child frame named wordFrame must be obtained. From that, the innerText extracts the word.
    */
    const children = frame.childNodes;
    
    // children[5].innerHTML = "<h1>BOOOH!</h1>";
    // console.log(children[1].innerText);
    // console.log(children[5].innerText);
    /*
    children[1] is the word frame.
    children[5] is the definition frame.
    */
    const word = children[1].innerText;
    const textArea = children[5].childNodes[3];
    // Default message...
    textArea.textContent = "Very sorry. No definition for this word was available online.";
    // Fetch the definitions from the dictionary API.
    const dictionary_response = await fFetchDefinitions(word);

    // The string that is eventually going into the definition textarea.
    let textAreaString = "";

    if (dictionary_response != 404)
    {
        // The dictionary API object is a horrendous mess...
        // Here is some reference.
        // const unorderedList = children[5].createElement("ul");
        // console.log(dictionary_response);
        // console.log(dictionary_response[0].word);
        //console.log(dictionary_response[0]);
        // console.log(dictionary_response[0].meanings);
        // console.log(dictionary_response[0].meanings[0].partOfSpeech);
        // console.log(dictionary_response[0].meanings[0].definitions[0].definition);
        // console.log(dictionary_response[0].word);
        
        for (let pos in dictionary_response[0].meanings)
        {
            //console.log(dictionary_response[0].meanings[pos].partOfSpeech);
            textAreaString += `${dictionary_response[0].meanings[pos].partOfSpeech.toUpperCase()}\r\n`;
            for (let defs in dictionary_response[0].meanings[pos].definitions)
            {
                textAreaString += `- ${dictionary_response[0].meanings[pos].definitions[defs].definition}\r\n`;
                //console.log(dictionary_response[0].meanings[pos].definitions[defs].definition);
            }
        }
        // console.log(textAreaString);
        textArea.value = textAreaString;
    }
    else
    {
        console.log("ERROR: Fetch returned false.");
    }
};


async function fFetchDefinitions(word)
{
    const url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word;
    // console.log(url);
    const controller = new AbortController();
    const timeOut = setTimeout(
        function()
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
            const definition = await response.json();
            // console.log(definition);
            // console.log(definition[0].meanings[0].definitions[0].definition);
            return definition;
        }
        else
        {
            if (response.status === 404)
            {
                console.log("Definition data was not found.");
                return 404;
            }
            console.log(`RESPONSE ERROR: ${response.status}`);
            return false // Make a dummy here.
        };
    }
    catch (error)
    {
        console.log(`NETWORK ERROR: ${error.name}`);
        return false; // dummy return.
    }
    finally
    {
        clearTimeout(timeOut);
    };
};
