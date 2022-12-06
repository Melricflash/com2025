// AJAX functionality for the ADD TO MY GAMES BUTTON


async function toggleGame(gameID) {
    $.ajax({
        url: 'add', // send request to this url
        type: 'get', // send via get request
        data: {
            gameID: gameID, // send gameID data to the view
        },

        success: function(response) { // stuff to do when a json response is recieved from the view

            // if we get a success message from the view, reload the button. use function() unwrap to stop buttons from being overlayed
            // ontop of eachother
            if (response.libraryUpdated) {
                $("#myGamesButton").load(" #myGamesButton", function(){$(this).children().unwrap()});
                
            }

        }


    })
}