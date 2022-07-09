// Wait for the DOM to finish loading before running the script

document.addEventListener("DOMContentLoaded", function() {
    
    // Get the current time in year, month, day, hour and minute
    
    let today = new Date();

    // Increase by 12 hours, because Events cannot be created more
    // than 12 hours before they take place
    let future = new Date(today.getTime() + 12*3600000);
    
    // Day
    let day = future.getDate();
    
    // For month, January is actually 0, so increment by 1
    let month = future.getMonth() + 1; 
    
    // Year
    let year = future.getFullYear();
    
    // Hour
    let hours = future.getHours()
    
    // Minutes
    let min = future.getMinutes()

    // If the numbers are less than 10, add a 0 before it
    // otherwise the date will not be in the right format
    // This needs to be done for day, month, hour and minutes
    if (day < 10) {
        day = '0' + day;
    }

    if (month < 10) {
        month = '0' + month;
    } 

    if (hours < 10) {
        hours = '0' + hours;
    } 

    if (min < 10) {
        min = '0' + min;
    } 

    // Build the correct Datestring to inject as max value
    // into the Inpute Datetimefield
    futurestring = year + '-' + month + '-' + day + 'T' + hours + ':' + min;
    
    // The actual injection into the format field
    document.getElementById("id_location_time").setAttribute("min", futurestring);
});