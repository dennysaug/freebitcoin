var startValue = '0.00000002', // Don't lower the decimal point more than 4x of current balance
        stopPercentage = 0.001, // In %. I wouldn't recommend going past 0.08
        maxWait = 500, // In milliseconds
        stopped = false,
        stopBefore = 3; // In minutes

        // implementar o calculo startValue 1% do balance e profit 10% do balance
 
var $loButton = $('#double_your_btc_bet_lo_button'),
                $hiButton = $('#double_your_btc_bet_hi_button');


var inicial = parseFloat($('#balance').text());
var profit = 0.00000080;
//var profit = parseFloat((inicial * 0.07).toFixed(8));
//var startValue = parseFloat(profit * 0.004).toFixed(8).toString();


//////////////////////////////////

function multiply(){
        var current = $('#double_your_btc_stake').val();
        var multiply = (current * 2).toFixed(8);

        $('#double_your_btc_stake').val(multiply);

}
 
function getRandomWait(){
        var wait = Math.floor(Math.random() * maxWait ) + 100;
 
        console.log('Waiting for ' + wait + 'ms before next bet.');
 
        return wait ;
}
 
function startGame(){
        console.log('Game started!');
        reset();
        $loButton.trigger('click');
}
 
function stopGame(){
        console.log('Game will stop soon! Let me finish.');
        stopped = true;
}
 
function reset(){
        $('#double_your_btc_stake').val(startValue);
}
 
// quick and dirty hack if you have very little bitcoins like 0.0000001
function deexponentize(number){
        return number * 1000000;
}
 
function iHaveEnoughMoni(){
        var balance = deexponentize(parseFloat($('#balance').text()));
        var current = deexponentize($('#double_your_btc_stake').val());
 
        return ((balance*2)/100) * (current*2) > stopPercentage/100;
}
 
function stopBeforeRedirect(){
        var minutes = parseInt($('title').text());
 
        if( minutes < stopBefore )
        {
                console.log('Approaching redirect! Stop the game so we don\'t get redirected while loosing.');
                stopGame();
 
                return true;
        }
 
        return false;
}
 
// Unbind old shit
$('#double_your_btc_bet_lose').unbind();
$('#double_your_btc_bet_win').unbind();
 
// Loser
$('#double_your_btc_bet_lose').bind("DOMSubtreeModified",function(event){
        if( $(event.currentTarget).is(':contains("lose")') )
        {
                console.log('You LOST! Multiplying your bet and betting again.');
               
                multiply();
 
                setTimeout(function(){
                        $loButton.trigger('click');
                }, getRandomWait());
 
                //$loButton.trigger('click');
        }
});
 
// Winner
$('#double_your_btc_bet_win').bind("DOMSubtreeModified",function(event){

	// console.log('COMPARACAO', inicial + ' >= ' + parseFloat(inicial + ((inicial * meta)/100)).toFixed(8));
	balance = parseFloat($('#balance').text());

	
	// if(balance >= parseFloat(inicial + ((inicial * meta)/100)).toFixed(8)) {
        if(balance >= parseFloat(inicial + profit).toFixed(8)) {
	 stopGame();
	 console.log('Parabéns! Você atingiu sua meta de ' + (inicial + profit).toFixed(8) + ' BTC');	
			
	}
	
        if( $(event.currentTarget).is(':contains("win")') )
        {
                if( stopBeforeRedirect() )
                {
                        return;
                }
 
                if( iHaveEnoughMoni() )
                {
                        console.log('You WON! But don\'t be greedy. Restarting!');
 
                        reset();
 
                        if( stopped )
                        {
                                stopped = false;
                                return false;
                        }
                }
                else
                {
                        console.log('You WON! Betting again');
                }
 
                setTimeout(function(){
                        $loButton.trigger('click');
                }, getRandomWait());
        }
});

startGame();
