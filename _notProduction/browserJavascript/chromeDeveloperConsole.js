// Ability to add all Youtube videos from a playlist to one of your playlists
//append &disable_polymer=true to the end of the url of Youtube to use the old playlist layout


// increase YouTube playback speed

var speed = prompt("How fast do you want to play the video?")
document.getElementsByTagName("video")[0].playbackRate = speed


document.getElementsByTagName("video")[0].playbackRate = 3









// stop following all friends on Facebook


// I have been struggling with something similar and here is the step by step solution.
// 	1. Go to Home.
// 	2. Click on markdown button, which is at rightmost part of same bar.
// 	3.
// 3. Click on News Feed Preferences. (or google it).
// 4. Click on “Unfollow people to hide their posts” and then select friends from the option. Important: Scroll down all the list of friends on the same page. (Otherwise you will not be able to unfollow all of them, but only those which are present on that page).
// 5. Open inspect element and go to console.
// 6. Paste the following code:




var a = document.getElementsByClassName("_5u3n");
for (var i = 0; i < a.length; i++){
    a[i].click();
}



// 6. Now finally click Done.
// Yureka, you have successfully unfollowed all of your friends :)
// Note: Facebook bot may temporarily block you from using same method. So use at your own risk.
// Edit : You can use above script for pages and groups also. All you need is just change the choice in Unfollow portion.
// Alternatively you can also use a slower script.




var a = document.getElementsByClassName("_5u3n");
var x = 0;
var time = 1000;
function amol(){
    a[x].click();
   if(x++ < a.length){
        setTimeout(amol, time);
   }
}
amol();





// This one will take 1 sec for each friend/page/group. You can speed it up by decreasing the value of “time” in line 3.

