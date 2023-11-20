var div = document.getElementById('profile-picture');
var display = 1;

function hideShow()
{
    if (display == 1)
    {
        div.style.display = 'block';
        display = 0;
        document.getElementById("showButton").innerText = "Click to Hide";
    }
    else
    {
        div.style.display = 'none';
        display = 1;
        document.getElementById("showButton").innerText = "Choose Profile Picture";
    }
}